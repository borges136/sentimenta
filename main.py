from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import numpy as np
import tkinter as tk
import sounddevice as sd
import os
import soundfile as sf
import time
import queue
import threading
from PIL import ImageTk, Image
from emotion_analyzer import EmotionAnalyzer
from tkinter.filedialog import askopenfile


window = Tk()
window.geometry("700x620")
window.resizable(0, 0)
window.title("SENTIMENTA Emotion Recognition Assistant")
#
# canvas1 = tk.Canvas(window, width=300, height=300)
# canvas1.pack()
#
# def takeScreenshot():
#     myScreenshot = pyautogui.screenshot()
#     file_path = filedialog.asksaveasfilename(defaultextension='.png')
#     myScreenshot.save(file_path)
#
# myButton = tk.Button(text="Take Screenshot", command=takeScreenshot, bg='green', fg='white', font=10)
# canvas1.create_window(150, 150, window=myButton)
# window.mainloop()

def openFile():
    filepath = filedialog.askopenfilename(initialdir='C:\\Users\\tommy\\PycharmProjects\\Sentimenta_new',
                                          filetypes=(("audio files", "*.wav"),
                                                     ("all files", "*.*")))
    if filepath:
        analyzer = EmotionAnalyzer()
        results = analyzer.analyze(filepath)
        print(f'total results: {results}')
        show_results(results)

def close_window():
    window.destroy()
    exit()
#*************************************************************************************************
# #logo
window.title("Welcome to 'SENTIMENTA' Your Emotion Recognition Assistant")
window.configure(background="grey")
 ### psychologist ![](../gui_5/logo.gif)photo
photo1= PhotoImage(file="logo.gif")
photo1_Label=Label(window,image=photo1,bg="black").place(x=115, y=0)

#*************************************************************************************************
#####recorder
# Create a queue to contain the audio data
q = queue.Queue()
# Declare variables and initialise them
recording = False
file_exists = False

# Fit data into queue
def callback(indata, frames, time, status):
    q.put(indata.copy())

# Functions to play, stop and record audio
# The recording is done as a thread to prevent it being the main process
def threading_rec(x):
    if x == 1:
        # If recording is selected, then the thread is activated
        t1 = threading.Thread(target=record_audio)
        t1.start()
    elif x == 2:
        # To stop, set the flag to false
        global recording
        recording = False
        messagebox.showinfo(message="Recording finished")
    elif x == 3:
        # To play a recording, it must exist.
        if file_exists:
            # Read the recording if it exists and play it
            data, fs = sf.read("trial.wav", dtype='float32')
            sd.play(data, fs)
            sd.wait()
        else:
            # Display and error if none is found
            messagebox.showerror(message="Record something to play")

# Recording function
def record_audio():
    # Declare global variables
    global recording
    # Set to True to record
    recording = True
    global file_exists
    # Create a file to save the audio
    messagebox.showinfo(message="Recording Audio. Speak into the mic")
    with sf.SoundFile("trial.wav", mode='w', samplerate=44100,
                      channels=1) as file:
        # Create an input stream to record audio without a preset time
        with sd.InputStream(samplerate=44100, channels=1, callback=callback):
            while recording == True:
                # Set the variable to True to allow playing the audio later
                file_exists = True
                # write into file
                file.write(q.get())

# Button to record audio
record_btn = Button(window, text="Record Audio", command=lambda m=1: threading_rec(m))
record_btn.place(x=130, y=250)
# Stop button
stop_btn = Button(window, text="Stop Recording", command=lambda m=2: threading_rec(m))
stop_btn.place(x=250, y=250)
# Play button
play_btn = Button(window, text="Play Recording", command=lambda m=3: threading_rec(m))
play_btn.place(x=360, y=250)

#*************************************************************************************************
# Button to browse audio
browse_btn = Button(text="Browse record",command=openFile)
browse_btn.place(x=490, y=250)

#*************************************************************************************************
#analysis results labels - watson,dl model,vader

results_headline_1 = Label(window, text="Sentimenta Analysis", bg="white")
results_headline_1.place(x=300, y=300)

#************************************************************************************************
results_headline_model = Label(window, text="Emotion Recognition Model:", bg="white",fg="black")
results_headline_model.place(x=10, y=340)
results_headline_model_model = Label(window, text="Please apply an audio ...", bg="grey")
results_headline_model_model.place(x=300, y=340)
# results_headline_model_model.pack()

results_headline_watson = Label(window, text="Watson:",  bg="white",fg="black")
results_headline_watson.place(x=10, y=400)
results_headline_watson_watson = Label(window, text="Please apply an audio ...", bg="grey")
results_headline_watson_watson.place(x=300, y=400)

results_headline_vader = Label(window, text="Vader:",  bg="white",fg="black")
results_headline_vader.place(x=10, y=460)
results_headline_vader_vader = Label(window, text="Please apply an audio ...", bg="grey")
results_headline_vader_vader.place(x=300, y=460)

#*************************************************************************************************
#the text of the speech label
stt_label = Label(window, text="Speech to text:",  bg="white",fg="black")
stt_label.place(x=10, y=530)
text_of_audio = Label(window, text="", bg="grey")
text_of_audio.place(x=100, y=530)

#*************************************************************************************************

# #exit
#add a exit button
exit_btn=Button(window,text="EXIT",width=14,command=close_window)
exit_btn.place(x=570, y=570)

def show_results(results):
    short_cnn=highest_cnn_results(results['cnn_from_audio'])
    results_headline_model_model.config(text=short_cnn)
    short_watson = highest_watson_results(results['watson'])
    results_headline_watson_watson.config(text=short_watson)
    short_vader = highest_veder_results(results['vader'])
    results_headline_vader_vader.config(text=short_vader)
    text_of_audio.config(text=results['stt'])

def highest_cnn_results(cnn_results):
    prediction=cnn_results.pop("prediction")
    x = np.array(list(cnn_results.values()))
    y = x.astype(np.float)
    max_value = max(y)
    return f'{prediction}: {max_value}'

def highest_watson_results(watson_results):
    string_watson=''
    watson_short=watson_results["document_tone"]["tones"]
    for result in watson_short:
        string_watson+=result["tone_name"]+' '
        string_watson += str(result["score"])+"\n"
    return string_watson

def highest_veder_results(sentiment_dict):
    sentiment=''
    if sentiment_dict['compound'] >= 0.05:
       sentiment="Positive"
    elif sentiment_dict['compound'] <= - 0.05:
       sentiment = "Negative"
    else:
       sentiment = "Neutral"
    return sentiment


window.mainloop()



