from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog as fd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from emotion_analyzer import EmotionAnalyzer
import qdarkstyle
import json
import sounddevice as sd
from tkinter import *
import queue
import soundfile as sf
import threading

class Ui_MainWindow(object):
    def __init__(self):
        self.q = queue.Queue()
        # Declare variables and initialise them
        self.recording = False
        self.file_exists = False
        # Fit data into queue
    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(MainWindow, 'Open file', '.', 'Audio (*.wav)')
        if fname:
            analyzer = EmotionAnalyzer()
            results = analyzer.analyze(fname[0])
            print(f'total results: {results}')
            self.watson_results.setText(str(results))
#************************************************************************************

# Create a queue to contain the audio data
    def callback(self, indata, frames, time, status):
        self.q.put(indata.copy())
        # Functions to play, stop and record audio
        # The recording is done as a thread to prevent it being the main process
    def record_audio(self):             # Declare global variables
        # global recording            # Set to True to record
        recording = True
        # global file_exists          # Create a file to save the audio
        messagebox.showinfo(message="Recording Audio. Speak into the mic")
        with sf.SoundFile("trial.wav", mode='w', samplerate=44100,
                        channels=2) as file:
            # Create an input stream to record audio without a preset time
            with sd.InputStream(samplerate=44100, channels=2, callback=self.callback):
                while recording == True:
                    # Set the variable to True to allow playing the audio later
                    file_exists = True
                    # write into file
                    file.write(self.q.get())

    def threading_rec(self, x):
        if x == 1:             # If recording is selected, then the thread is activated
            t1 = threading.Thread(target=self.record_audio)
            t1.start()
            messagebox.showinfo(message="Recording...")
        elif x == 2:            # To stop, set the flag to false
            # global recording
            recording = False
            messagebox.showinfo(message="Recording finished")
        elif x == 3:           # To play a recording, it must exist.
            if self.file_exists:     # Read the recording if it exists and play it
                data, fs = sf.read("trial.wav", dtype='float32')
                sd.play(data, fs)
                sd.wait()
        else:                   # Display and error if none is found
            messagebox.showerror(message="Record something to play")
        # Recording function


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(497, 486)

        # Play button
        self.start_rec = QtWidgets.QPushButton(MainWindow)
        self.start_rec.setGeometry(QtCore.QRect(20, 220, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Black")
        font.setBold(True)
        font.setWeight(75)
        self.start_rec.setFont(font)
        self.start_rec.setObjectName("start_rec")
        self.start_rec.clicked.connect(lambda: self.threading_rec(1))

        # Stop button
        self.stop_rec = QtWidgets.QPushButton(MainWindow)
        self.stop_rec.setGeometry(QtCore.QRect(140, 220, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Black")
        font.setBold(True)
        font.setWeight(75)
        self.stop_rec.setFont(font)
        self.stop_rec.setObjectName("stop_rec")
        self.stop_rec.clicked.connect(lambda: self.threading_rec(2))

        self.play_rec = QtWidgets.QPushButton(MainWindow)
        self.play_rec.setGeometry(QtCore.QRect(250, 220, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Black")
        font.setBold(True)
        font.setWeight(75)
        self.play_rec.setFont(font)
        self.play_rec.setObjectName("play_rec")
        self.play_rec.clicked.connect(lambda: self.threading_rec(3))

        self.browse_rec = QtWidgets.QPushButton(MainWindow)
        self.browse_rec.setGeometry(QtCore.QRect(360, 220, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Black")
        font.setBold(True)
        font.setWeight(75)
        self.browse_rec.setFont(font)
        self.browse_rec.setObjectName("browse_rec")
        self.browse_rec.clicked.connect(self.browsefiles)

        # ********End Buttons to record audio ****************************************************************

        self.logo_sentimenta = QtWidgets.QLabel(MainWindow)
        self.logo_sentimenta.setGeometry(QtCore.QRect(-10, 0, 531, 201))
        self.logo_sentimenta.setStyleSheet("background-image: url(:/newPrefix/logo.gif);")
        self.logo_sentimenta.setText("")
        self.logo_sentimenta.setPixmap(QtGui.QPixmap(":/newPrefix/logo.gif"))
        self.logo_sentimenta.setScaledContents(True)
        self.logo_sentimenta.setObjectName("logo_sentimenta")

        self.watson_label = QtWidgets.QLabel(MainWindow)
        self.watson_label.setGeometry(QtCore.QRect(20, 370, 111, 16))
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Black")
        font.setBold(True)
        font.setWeight(75)
        self.watson_label.setFont(font)
        self.watson_label.setObjectName("watson_label")

        self.dl_model_label = QtWidgets.QLabel(MainWindow)
        self.dl_model_label.setGeometry(QtCore.QRect(20, 410, 151, 16))
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Black")
        font.setBold(True)
        font.setWeight(75)
        self.dl_model_label.setFont(font)
        self.dl_model_label.setObjectName("dl_model_label")

        self.vader_label = QtWidgets.QLabel(MainWindow)
        self.vader_label.setGeometry(QtCore.QRect(20, 450, 101, 16))
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Black")
        font.setBold(True)
        font.setWeight(75)
        self.vader_label.setFont(font)
        self.vader_label.setObjectName("vader_label")

        self.analysis_label = QtWidgets.QLabel(MainWindow)
        self.analysis_label.setGeometry(QtCore.QRect(210, 320, 171, 16))
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Black")
        font.setBold(True)
        font.setWeight(75)
        self.analysis_label.setFont(font)
        self.analysis_label.setObjectName("analysis_label")

        self.exit_btn = QtWidgets.QPushButton(MainWindow)
        self.exit_btn.setGeometry(QtCore.QRect(424, 450, 61, 23))
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Black")
        font.setBold(True)
        font.setWeight(75)
        self.exit_btn.setFont(font)
        self.exit_btn.setObjectName("exit_btn")

        self.save_results = QtWidgets.QPushButton(MainWindow)
        self.save_results.setGeometry(QtCore.QRect(390, 370, 101, 23))
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Black")
        font.setBold(True)
        font.setWeight(75)
        self.save_results.setFont(font)
        self.save_results.setObjectName("save_results")

        self.watson_results = QtWidgets.QPushButton(MainWindow)
        self.watson_results.setGeometry(QtCore.QRect(200, 370, 161, 23))
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Black")
        font.setBold(True)
        font.setWeight(75)
        self.watson_results.setFont(font)
        self.watson_results.setObjectName("watson_results")

        self.dl_results = QtWidgets.QPushButton(MainWindow)
        self.dl_results.setGeometry(QtCore.QRect(200, 410, 161, 23))
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Black")
        font.setBold(True)
        font.setWeight(75)
        self.dl_results.setFont(font)
        self.dl_results.setObjectName("dl_results")

        self.vader_results = QtWidgets.QPushButton(MainWindow)
        self.vader_results.setGeometry(QtCore.QRect(200, 450, 161, 23))
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Black")
        font.setBold(True)
        font.setWeight(75)
        self.vader_results.setFont(font)
        self.vader_results.setObjectName("vader_results")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Dialog"))
        self.start_rec.setText(_translate("MainWindow", "Start rec"))
        self.stop_rec.setText(_translate("MainWindow", "Stop Rec"))
        self.play_rec.setText(_translate("MainWindow", "Play Rec"))
        self.browse_rec.setText(_translate("MainWindow", "Browse"))
        self.watson_label.setText(_translate("MainWindow", "Watson:"))
        self.dl_model_label.setText(_translate("MainWindow", "Deep Learning model:"))
        self.vader_label.setText(_translate("MainWindow", "Vader:"))
        self.analysis_label.setText(_translate("MainWindow", "Sentimenta Analysis"))
        self.exit_btn.setText(_translate("MainWindow", "EXIT"))
        self.save_results.setText(_translate("MainWindow", "Save results"))
        self.watson_results.setText(_translate("MainWindow", "PushButton"))
        self.dl_results.setText(_translate("MainWindow", "PushButton"))
        self.vader_results.setText(_translate("MainWindow", "PushButton"))
        #*****************************************************************

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))

    MainWindow = QtWidgets.QDialog()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
