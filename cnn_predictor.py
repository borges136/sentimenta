import numpy as np
import pandas as pd
import librosa
from tensorflow import keras


class Config:
    def __init__(self, n_mfcc=26, n_feat=13, n_fft=552, sr=22050, window=0.4, test_shift=0.1):
        self.n_mfcc = n_mfcc
        self.n_feat = n_feat
        self.n_fft = n_fft
        self.sr = sr
        self.window = window
        self.step = int(sr * window)
        self.test_shift = test_shift
        self.shift = int(sr * test_shift)


class EmotionRecognitionAudioPredictor():
    def __init__(self):
        self.model = keras.models.load_model("saved_model")
        self.config = Config()


    def predict_for_file(self, filename):
        # Initialize a local results list
        local_results = []
        config = self.config

        # Initialize min and max values for each file for scaling
        _min, _max = float('inf'), -float('inf')

        # Load the file
        wav, sr = librosa.load(filename)

        # Clean the file
        wav = self.envelope(wav, sr, 0.001)  # originally 0.0005!!!

        # Create an array to hold features for each window
        X = []

        # Iterate over sliding 0.4s windows of the audio file
        for i in range(int((wav.shape[0] / sr - config.window) / config.test_shift)):
            X_sample = wav[i * config.shift: i * config.shift + config.step]  # slice out 0.4s window
            X_mfccs = librosa.feature.mfcc(X_sample, sr, n_mfcc=config.n_mfcc, n_fft=config.n_fft,
                                           hop_length=config.n_fft)[1:config.n_feat + 1]  # generate mfccs from sample

            _min = min(np.amin(X_mfccs), _min)
            _max = max(np.amax(X_mfccs), _max)  # check min and max values
            X.append(X_mfccs)  # add features of window to X

        # Put window data into array, scale, then reshape
        X = np.array(X)
        X = (X - _min) / (_max - _min)
        X = X.reshape(X.shape[0], X.shape[1], X.shape[2], 1)

        # Feed data for each window into saved_model for prediction
        for i in range(X.shape[0]):
            window = X[i].reshape(1, X.shape[1], X.shape[2], 1)
            local_results.append(self.model.predict(window))

        # Aggregate predictions for file into one then append to all_results
        local_results = (np.sum(np.array(local_results), axis=0) / len(local_results))[0]
        local_results = local_results.tolist()
        prediction = np.argmax(local_results)

        keys = ['neutral', 'happy', 'sad', 'angry', 'fearful', 'disgusted', 'surprised', 'prediction']
        prediction_str = keys[prediction]

        local_results.append(prediction_str)
        #local_results.append(filename)
        # df_cols = keys
        #print(f'local_results: {local_results}')
        # local_results = pd.DataFrame(np.reshape(local_results, (-1, len(df_cols))), columns=df_cols)
        # return local_results
        results = dict(zip(keys, local_results))
        return results

    def envelope(self, y, sr, threshold):
        mask = []
        y_abs = pd.Series(y).apply(np.abs)
        y_mean = y_abs.rolling(window=int(sr / 10), min_periods=1, center=True).mean()
        for mean in y_mean:
            if mean > threshold:
                mask.append(True)
            else:
                mask.append(False)
        return np.array(y[mask])

