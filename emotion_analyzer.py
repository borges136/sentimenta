from player import Player
from stt_class import STT
from cnn_predictor import EmotionRecognitionAudioPredictor
from watson_analyzer import WatsonToneAnalyzer
from vader_analyzer import VaderAnalyzer
import threading
import json
import timeit

class EmotionAnalyzer():
    def __init__(self):
        self.parsed_text = []
        self.results = {}

    def stt(self, filename):
        stt = STT()
        # start = timeit.default_timer()
        text_from_speech = stt.recognize(stt.opensoundfile(filename)).results[0].alternatives[0].transcript
        # stop = timeit.default_timer()
        # print('Time for speech recognition: ', stop - start)
        print(f'speech recognition results: {text_from_speech}')
        self.results['stt'] = text_from_speech
        return text_from_speech

    def watsonAnalyzeTone(self, text):
        watson = WatsonToneAnalyzer()
        start = timeit.default_timer()
        # text = 'Team, I know that times are tough! Product ' \
        #        'sales have been disappointing for the past three ' \
        #        'quarters. We have a competitive product, but we ' \
        #        'need to do a better job of selling it!'

        watson_tone = watson.analyze(text)
        # stop = timeit.default_timer()
        # print('Time for watson API: ', stop - start)
        print(f'watson tone: {json.dumps(watson_tone)}')
        self.results['watson'] = watson_tone

    def vaderAnalyze(self, text):
        vader = VaderAnalyzer()
        # start = timeit.default_timer()
        # text = 'Team, I know that times are tough! Product ' \
        #        'sales have been disappointing for the past three ' \
        #        'quarters. We have a competitive product, but we ' \
        #        'need to do a better job of selling it!'

        vader_sentiment = vader.analyze(text)
        # stop = timeit.default_timer()

        # print('Time for vader: ', stop - start)
        print(f'vader sentiment: {json.dumps(vader_sentiment)}')
        self.results['vader'] = vader_sentiment

    def analyzeSentimentFromText(self, filename):
        text = self.stt(filename)

        wt = threading.Thread(target=self.watsonAnalyzeTone, args=(text,))
        wt.start()
        vt = threading.Thread(target=self.vaderAnalyze, args=(text,))
        vt.start()
        wt.join()
        vt.join()

    def predictEmotionFromAudio(self, filename):
        # start = timeit.default_timer()
        audio_predictor = EmotionRecognitionAudioPredictor()
        res = audio_predictor.predict_for_file(filename)

        # stop = timeit.default_timer()

        #print('Time for CNN prediction: ', stop - start)
        print(f'audio emotion detection results: {res}')
        self.results['cnn_from_audio'] = res

    def analyze(self, filename):
        start = timeit.default_timer()

        tasks = []

        tasks.append(threading.Thread(target=self.predictEmotionFromAudio, args=(filename,)))
        tasks[-1].start()
        tasks.append(threading.Thread(target=self.analyzeSentimentFromText, args=(filename,)))
        tasks[-1].start()

        for task in tasks:
            task.join()
        stop = timeit.default_timer()

        print('Total Time: ', stop - start)
        return self.results

if __name__ == '__main__':
    # filename = '/Users/b/Documents/stud/year 3/sem 1/voice/bonus task/submit/sad.wav'
    filename = '/Users/b/Documents/stud/year 3/sem 1/voice/bonus task/submit/happy.wav'
    # filename = '/Users/b/PycharmProjects/pocketsphinx-python/deps/sphinxbase/test/regression/chan3.2chan.wav'
    #filename = "/Users/b/Documents/stud/year 3/sem 1/voice/Hands-On 1 Sampling Signals/Al_page_13_78.wav"
    analyzer = EmotionAnalyzer()
    results = analyzer.analyze(filename)
    print(f'total results: {results}')
