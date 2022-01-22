import io
import os
import wave

import sys
sys.setrecursionlimit(1500)


# Imports the Google Cloud client library
from google.cloud import speech


credential_path = "google_api_credentials.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

class STT():
    def __init__(self):
        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=44100,
            language_code="en-US",
        )
        # 
            # encoding=speech.RecognitionConfig.AudioEncoding.MP3,
            # sample_rate_hertz=16000,
            # language_code='iw-IL',
            # enable_word_time_offsets=True) 
        # Instantiates a client
        self.client = speech.SpeechClient()
        

    def opensoundfile(self, file_name):        
        # Loads the audio into memory
        with wave.open(file_name, "rb") as audio_file:
            content = audio_file.readframes(audio_file.getnframes())
            frame_rate = audio_file.getframerate()
            num_of_channels = audio_file.getnchannels()
            audio = speech.RecognitionAudio(content=content)
        return audio, frame_rate, num_of_channels

    def recognize(self, audio, sr=44100, channel_count = 1):
        response = ''
        # Detects speech in the audio file and return results to caller
        try:
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=sr,
                language_code="en-US",
                audio_channel_count = channel_count
            )
            response = self.client.recognize(config= config, audio=audio)
        except Exception as e:
            print(f'Something wrong with recognition: {str(e)}')
        return response    

if __name__ == '__main__':
    file_name = "audio/03-01-02-02-01-02-02.wav"
    st= STT()
    audio, frame_rate, num_of_channels=st.opensoundfile(file_name)
    rz=st.recognize(audio, frame_rate, num_of_channels)
    for result in rz.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))
