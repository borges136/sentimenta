import io
import os
import sys
sys.setrecursionlimit(1500)
from google.cloud import speech

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
        with io.open(file_name, "rb") as audio_file:
            content = audio_file.read()
            audio = speech.RecognitionAudio(content=content)
        return audio

    def recognize(self,audio):
        response = ''
        # Detects speech in the audio file and return results to caller
        try:
            response = self.client.recognize(config=self.config, audio=audio)
        except Exception as e:
            print(f'Something wrong with recognition: {str(e)}')
        return response    

if __name__ == '__main__':
    # The name of the audio file to transcribe
    file_name = "happy.wav"
    #file_name = '/Users/b/PycharmProjects/pocketsphinx-python/deps/sphinxbase/test/regression/chan3.2chan.wav'
    st= STT()
    audio=st.opensoundfile(file_name)
    rz=st.recognize(audio)    
    for result in rz.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))
