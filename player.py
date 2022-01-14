# first install the next:
# pip install sounddevice, scipy, soundfile

import sounddevice as sd
from scipy.io.wavfile import write
import soundfile as sf
import time

class Player():

    def __init__(self):
        self.fs = 44100  # Sample rate
        self.seconds = 3  # Duration of recording
        self.AMP = 1  # Amplify data - increase Volume of sound        

    def record(self, recordfilepath):
        print(recordfilepath)
        try:                       
            print('Start recording') # TBD change record button color
            myrecording = sd.rec(int(self.seconds * self.fs), samplerate=self.fs, dtype='int16', channels=1)
            sd.wait()  # Wait until recording is finished
            #time.sleep(self.seconds)
            print('Stop recording')
            write(recordfilepath, self.fs, myrecording)  # Save as WAV file
        except:
            print('Failed in Record operation!')        

    def play(self, playfilepath):
        try:
            # Extract data and sampling rate from file
            data, fs = sf.read(playfilepath, dtype='float32')            
            print('Starting playing')
            sd.play(data*self.AMP, fs)
            sd.wait()  # Wait until file is done playing
            print('Stop playing')
        except:
            print('Failed in playfile operation!')

if __name__ == '__main__':
    pl = Player()
    pl.play('c_output.wav')
    pl.record('input44.wav')
    