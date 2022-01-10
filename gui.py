from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog as fd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from emotion_analyzer import EmotionAnalyzer
import qdarkstyle
import json

class Ui_MainWindow(object):
    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(MainWindow, 'Open file', '.', 'Audio (*.wav)')
        if fname:
            analyzer = EmotionAnalyzer()
            results = analyzer.analyze(fname[0])
            print(f'total results: {results}')
            self.results.setText(str(results))

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1500, 1500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")


        self.start_rec = QtWidgets.QPushButton(self.centralwidget)
        self.start_rec.setGeometry(QtCore.QRect(170, 170, 75, 23))
        self.start_rec.setObjectName("start_rec")


        self.stop_rec = QtWidgets.QPushButton(self.centralwidget)
        self.stop_rec.setGeometry(QtCore.QRect(290, 170, 75, 23))
        self.stop_rec.setObjectName("stop_rec")

        self.save_Rec = QtWidgets.QPushButton(self.centralwidget)
        self.save_Rec.setGeometry(QtCore.QRect(390, 170, 75, 23))
        self.save_Rec.setObjectName("save_Rec")

        self.results = QtWidgets.QLabel(self.centralwidget)
        self.results.setGeometry(QtCore.QRect(96, 230, 1000, 1000))
        self.results.setSizeIncrement(QtCore.QSize(300, 300))
        self.results.setObjectName("results")
        self.results.setWordWrap(True)



        MainWindow.setCentralWidget(self.centralwidget)

        self.brows = QtWidgets.QPushButton(self.centralwidget)
        self.brows.setGeometry(QtCore.QRect(170, 80, 75, 23))
        self.brows.setObjectName("brows")
        self.brows.clicked.connect(self.browsefiles)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 840, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.start_rec.setText(_translate("MainWindow", "start rec"))
        self.stop_rec.setText(_translate("MainWindow", "stop rec"))
        self.save_Rec.setText(_translate("MainWindow", "save "))
        self.results.setText(_translate("MainWindow", "TextLabel"))
        self.brows.setText(_translate("MainWindow", "brows"))

        #*****************************************************************
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))


    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


