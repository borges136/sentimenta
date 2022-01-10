# before running install the next python modules: sounddevice, soundfile, matplotlib 
# pip install sounddevice soundfile matplotlib

import soundfile as sf
import sounddevice as sd

filename = ''
plot_enable = True
AMP = 1.2  # Amplify data - increase Volume of sound
# Extract data and sampling rate from file
data, fs = sf.read(filename, dtype='float32')

if plot_enable:
    import matplotlib.pyplot as plt
    plt.plot(data)
    plt.show()
print('Starting playing')
sd.play(data*AMP, fs)
status = sd.wait()  # Wait until file is done playing
print('Stop playing')