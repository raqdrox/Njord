import NjordMailHandler as mail_hldr
import NjordStreamLabHandler as strlb_hldr
import os
import pickle
from apiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import Error
import time
import requests
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QGridLayout
import json
import sys

#-----GLOBALS-----
procRun=0


class Ui_MainWindow(object):
    def __init__(self):
        super().__init__()
        self.workerThread = WorkerThread()  # no parent!
        self.thread = QThread()  # no parent!
        self.workerThread.errThrow.connect(self.errExit)
        self.workerThread.moveToThread(self.thread)
        self.workerThread.finished.connect(self.thread.quit)
        self.thread.started.connect(self.workerThread.run)
        self.workerThread.progBar.connect(self.updProg)

    def errExit(self,errorStr):
        self.constats.setText(QtCore.QCoreApplication.translate("MainWindow", errorStr))
        global procRun
        procRun=0
        self.startproc.setText(QtCore.QCoreApplication.translate("MainWindow", "Start Njord"))

    def updProg(self,val):
        self.progressBar.setProperty("value", val)

    def setupUi(self, MainWindow):
        global progBarptr
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(583, 319)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.configFrame = QtWidgets.QFrame(self.centralwidget)
        self.configFrame.setEnabled(True)
        self.configFrame.setGeometry(QtCore.QRect(290, 0, 291, 301))
        self.configFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.configFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.configFrame.setObjectName("configFrame")
        self.clientIdTB = QtWidgets.QPlainTextEdit(self.configFrame)
        self.clientIdTB.setGeometry(QtCore.QRect(20, 50, 251, 31))
        self.clientIdTB.setPlainText("")
        self.clientIdTB.setPlaceholderText("")
        self.clientIdTB.setObjectName("clientIdTB")
        self.sllabel1 = QtWidgets.QLabel(self.configFrame)
        self.sllabel1.setGeometry(QtCore.QRect(70, 20, 161, 31))
        font = QtGui.QFont()
        font.setFamily("Terminal")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.sllabel1.setFont(font)
        self.sllabel1.setTextFormat(QtCore.Qt.AutoText)
        self.sllabel1.setScaledContents(True)
        self.sllabel1.setAlignment(QtCore.Qt.AlignCenter)
        self.sllabel1.setIndent(-4)
        self.sllabel1.setObjectName("sllabel1")
        self.sllabel2 = QtWidgets.QLabel(self.configFrame)
        self.sllabel2.setGeometry(QtCore.QRect(70, 90, 161, 31))
        font = QtGui.QFont()
        font.setFamily("Terminal")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.sllabel2.setFont(font)
        self.sllabel2.setTextFormat(QtCore.Qt.AutoText)
        self.sllabel2.setScaledContents(True)
        self.sllabel2.setAlignment(QtCore.Qt.AlignCenter)
        self.sllabel2.setIndent(-4)
        self.sllabel2.setObjectName("sllabel2")
        self.oauthcodeTB = QtWidgets.QPlainTextEdit(self.configFrame)
        self.oauthcodeTB.setGeometry(QtCore.QRect(20, 210, 251, 31))
        self.oauthcodeTB.setObjectName("oauthcodeTB")
        self.sllabel3 = QtWidgets.QLabel(self.configFrame)
        self.sllabel3.setGeometry(QtCore.QRect(80, 180, 161, 31))
        font = QtGui.QFont()
        font.setFamily("Terminal")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.sllabel3.setFont(font)
        self.sllabel3.setTextFormat(QtCore.Qt.AutoText)
        self.sllabel3.setScaledContents(True)
        self.sllabel3.setAlignment(QtCore.Qt.AlignCenter)
        self.sllabel3.setIndent(-4)
        self.sllabel3.setObjectName("sllabel3")
        self.clientSecTB = QtWidgets.QPlainTextEdit(self.configFrame)
        self.clientSecTB.setGeometry(QtCore.QRect(20, 130, 251, 31))
        self.clientSecTB.setObjectName("clientSecTB")
        self.SaveBtn = QtWidgets.QPushButton(self.configFrame)
        self.SaveBtn.setGeometry(QtCore.QRect(20, 250, 101, 41))
        self.SaveBtn.setObjectName("SaveBtn")
        self.ClearBtn = QtWidgets.QPushButton(self.configFrame)
        self.ClearBtn.setGeometry(QtCore.QRect(160, 250, 101, 41))
        self.ClearBtn.setObjectName("ClearBtn")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 291, 301))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.startproc = QtWidgets.QPushButton(self.frame)
        self.startproc.setGeometry(QtCore.QRect(80, 150, 131, 51))
        self.startproc.setObjectName("startproc")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(60, 40, 101, 31))
        self.label.setObjectName("label")
        self.constats = QtWidgets.QLabel(self.frame)
        self.constats.setGeometry(QtCore.QRect(160, 40, 130, 31))
        self.constats.setObjectName("constats")
        self.progressBar = QtWidgets.QProgressBar(self.frame)
        self.progressBar.setGeometry(QtCore.QRect(20, 260, 281, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setFormat("")
        self.progressBar.setObjectName("progressBar")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setShortcutContext(QtCore.Qt.WindowShortcut)
        self.actionSave.setObjectName("actionSave")
        self.actionClear = QtWidgets.QAction(MainWindow)
        self.actionClear.setObjectName("actionClear")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.SaveBtn.clicked.connect(self.on_save)
        self.ClearBtn.clicked.connect(self.on_clear)
        self.startproc.clicked.connect(self.toggleThread)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.sllabel1.setText(_translate("MainWindow", "Client ID"))
        self.sllabel2.setText(_translate("MainWindow", "Client Secret"))
        self.sllabel3.setText(_translate("MainWindow", "OAuth Code"))
        self.SaveBtn.setText(_translate("MainWindow", "Save"))
        self.ClearBtn.setText(_translate("MainWindow", "Clear"))
        self.startproc.setText(_translate("MainWindow", "Start Njord"))
        self.label.setText(_translate("MainWindow", "Connection Status:"))
        self.constats.setText(_translate("MainWindow", "Not Connected"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionClear.setText(_translate("MainWindow", "Clear"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))

    def on_save(self):
        print("saved")
        data={
                "client_id": "",
                "client_secret": "",
                "redirect_uri": "https://operation-njord.blogspot.com/2020/12/auth.html",
                "code": "",
                "access_token": "",
                "refresh_token": ""
                }
        data['client_id']=self.clientIdTB.toPlainText()
        data['client_secret']=self.clientSecTB.toPlainText()
        data['code']=self.oauthcodeTB.toPlainText()

        with open('./tokens/SLauth.json','w') as f:
            json.dump(data,f,indent=4)
        self.on_clear()

    def on_clear(self):
        self.clientIdTB.clear()
        self.clientSecTB.clear()
        self.oauthcodeTB.clear()
        print("cleared")

    def toggleThread(self):
        global procRun
        if procRun==0:
            self.constats.setText(QtCore.QCoreApplication.translate("MainWindow", "Connected"))
            self.startproc.setText(QtCore.QCoreApplication.translate("MainWindow", "Stop Njord"))
            self.thread.start()
            print("started")
        else:
            self.constats.setText(QtCore.QCoreApplication.translate("MainWindow", "Not Connected"))
            self.startproc.setText(QtCore.QCoreApplication.translate("MainWindow", "Start Njord"))
            self.workerThread.quit()
            procRun=0
            print("terminated")

    def ProgBar(self):
        if self.progressBar.value()==100:
            self.progressBar.value=0
        self.progressBar.value+=10

class WorkerThread(QThread):
    finished = pyqtSignal()
    errThrow = pyqtSignal(str)
    progBar  = pyqtSignal(int)

    def isconnected(self):
        try:
            requests.get('https://www.google.com/').status_code
            return True
        except:
            return False
    @pyqtSlot()
    def run(self):
        global procRun
        procRun=1
        self.donationCount=0
        self.itertracker=0
        self.gmailSrv=self.startProcessGmail()
        self.strlabToken=strlb_hldr.getTokens()
        if self.strlabToken==0:
            self.errThrow.emit("Invalid StreamLabs Creds")
        else:
            mail_hldr.readAll(self.gmailSrv)
            self.updateLoop()
        self.stopThread()
    
    @pyqtSlot()
    def donationCheck(self): #check Gmail API for Mail Updates
        search_str='from:noreply@phonepe.com is:unread'
        msgids=mail_hldr.search_message(self.gmailSrv,'me',search_str)
        if len(msgids)>1:
            maiList=[]
            for ids in msgids:
                mailhtml=mail_hldr.get_message(self.gmailSrv, 'me', ids)
                data=mail_hldr.extractor(str(mailhtml['snippet']))
                maiList.append(data)
            return maiList
        if len(msgids)==1:
            mailhtml=mail_hldr.get_message(self.gmailSrv, 'me', msgids[0])
            data=mail_hldr.extractor(str(mailhtml['snippet']))
            return [data]
        else:
            print('No Donations')
            return []    
    @pyqtSlot()
    def strLabPut(self,donation): #send donation data to Streamlabs
        strlb_hldr.postDonations(donation,self.strlabToken)
        self.donationCount+=1

    @pyqtSlot()
    def startProcessGmail(self): #Returns Gmail Service Object
        creds = None
        service = None

        if os.path.exists('./tokens/token.pickle'):
            with open('./tokens/token.pickle', 'rb') as token:
                creds = pickle.load(token)
            
        if not creds or not creds.valid:
            retCode=mail_hldr.getToken(creds)
            if retCode==0:
                self.errThrow.emit("Gmail creds Invalid")
                self.stopThread()
            service = build('gmail', 'v1', credentials=creds)
            
        return service

    @pyqtSlot()
    def sleep(self, sec):

        for i in range(sec):
            self.progBar.emit(i*(100/sec))
            time.sleep(1)


    @pyqtSlot()        
    def updateLoop(self):   #mainloop
        global procRun
        while procRun==1:
            if not self.isconnected(): 
                self.errThrow.emit("No Internet Access")
                self.stopThread()
            donList=self.donationCheck()
            for donation in donList:
                self.strLabPut(donation)
                print(f'Donation {self.donationCount} :\n{donation}')
                time.sleep(2)
            self.sleep(20)
            self.itertracker+=1
            if self.itertracker==60:
                self.strlabToken=strlb_hldr.refreshTokens()
                self.itertracker=0
                
    @pyqtSlot()
    def stopThread(self):
        self.progBar.emit(0)
        self.finished.emit()

def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()