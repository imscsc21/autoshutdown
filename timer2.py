# coding: utf-8
import sys
import threading
import subprocess

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Form(QtWidgets.QDialog):
    def __init__(self,delegate=None,parent=None):
        QtWidgets.QDialog.__init__(self,parent)
        
        self.setToDefaultDelayTime()
        self.setAppDelegate(delegate)
        self.__currentTime = 0
        self.__force_close = False
        self.setRemainTime(60)
        self.ui = uic.loadUi("timer.ui",self)
        self.tmlbl=self.ui.findChild(QLabel,"label_2")
        self.tmlbl.setText(self.getFormattedString(self.getRemainTime()- self.getCurrentTime()))
        self.procb = self.ui.findChild(QProgressBar,"progressBar")
        self.procb.setMaximum(self.getRemainTime())
        self.procb.setValue(self.__currentTime)
        self.thtimer = QtCore.QTimer()
        self.thtimer.timeout.connect(self.looptimer)
        self.setFixedSize(self.size())
        #self.ui.show()
        #self.looptimer(True)
    def setAppDelegate(self,dele):
        self.app_delegate = dele
    def getAppDelegate(self):
        return self.app_delegate
    def showFormDialog(self):
        self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)
        self.__currentTime = 0
        self.procb.setValue(self.__currentTime)
        self.tmlbl.setText(self.getFormattedString(self.getRemainTime()- self.getCurrentTime()))
        self.ui.show()
        self.tick()
        #self.looptimer(True)
        
    def refreshTimerUI(self):
        self.procb.setValue(self.getCurrentTime())
        self.tmlbl.setText(self.getFormattedString(self.getRemainTime()- self.getCurrentTime()))
    def looptimer(self):
        print("call looptimer"+str(self.getCurrentTime()))
        if(self.__force_close is not True):
            self.refreshTimerUI()
            if(self.getCurrentTime()<self.getRemainTime()):
                #print("chkinit:",chkinit,self.__force_close)
                self.setCurrentTime(self.getCurrentTime()+1)
                #threading.Timer(1,self.looptimer,args=[False]).start()
            else:
                self.forceShutdownNow()
        else:
            try:
                self.thtimer.stop()
            except:
                print("tick stop error")
    @pyqtSlot()
    def onBtnClk_postpone_shutdown(self):
        print("call onBtnClk_postpone_shutdown")
        self.showdialog()
    def getFormattedString(self,mTimeSec):
        return str(int(int(mTimeSec)//3600))+":"+str(int(int(mTimeSec)//60))+":"+str((int(mTimeSec)%60))
    def setCurrentTime(self,tm):
        self.__currentTime = tm
    def getCurrentTime(self):
        return self.__currentTime
    def setRemainTime(self,tm):
        self.__remain_time = tm
    def getRemainTime(self):
        return self.__remain_time
    def tick(self):
        self.__force_close = False
        self.thtimer.start(1000)
    @pyqtSlot()
    def onBtnClk_shutdown_now(self):
        self.shutdownNow()
        #print("call onBtnClk_shutdown_now")
        #self.close()
    def setToDefaultDelayTime(self):
        self.__innerSetDelayTimeWithIndex(3)
    @pyqtSlot()
    def loadDefaultDelayTime(self):
        print("call loadDefaultDelayTime")
        self.setToDefaultDelayTime()
    def shutdownNow(self):
        print("call shutdownNow")
        self.__force_close = True
        subprocess.call(["shutdown.exe", "/s","/t", "0"])
        self.close()
    def forceShutdownNow(self):
        print("call forceShutdownNow")
        self.__force_close = True
        subprocess.call(["shutdown.exe","/f", "/s","/t", "0"])
        #subprocess.call(["shutdown.exe","/r","/f","/t", "0"])
        
        self.close()
    def __innerSetDelayTimeWithIndex(self,index):
        print("call __innerSetDelayTimeWithIndex",index)
        if(index==0):
            self.nextdelaytime=5*60
        elif(index==1):
            self.nextdelaytime=10*60
        elif(index==2):
            self.nextdelaytime=15*60
        elif(index==3):
            self.nextdelaytime=30*60
        elif(index==4):
            self.nextdelaytime=60*60
        elif(index==5):
            self.nextdelaytime=30*3*60
        elif(index==6):
            self.nextdelaytime=2*60*60
        elif(index==7):
            self.nextdelaytime=3*60*60
        elif(index==8):
            self.nextdelaytime=4*60*60
        else:
            self.nextdelaytime=6*60*60
    @pyqtSlot(int)
    def setDelayTimeWithIndex(self,index):
        self.__innerSetDelayTimeWithIndex(index)
    def showdialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        #self.setWindowFlags(self.windowFlags()&(~QtCore.Qt.WindowStaysOnTopHint))
        msg.setText("현재 설정된 연기 시간은 "+str(self.nextdelaytime//60)+"분 입니다\n연기하시려면 ok를 아니면 cancle버튼을 누른뒤 콤보박스의 시간을 움직여주세요.")
        #msg.setInformativeText("This is additional information")
        msg.setWindowTitle("사전경고")
        #msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.buttonClicked.connect(self.msgbtn)
        msg.setWindowFlags(msg.windowFlags()|QtCore.Qt.WindowStaysOnTopHint)
        retval = msg.exec_()
        print ("value of pressed message box button:", retval)
    def delayshutdown(self):
        print("call delayshutdown")
        self.__force_close = True
        self.app_delegate.getTrayIconClassObj().setDefaultTimeSec(self.nextdelaytime)
        self.app_delegate.getTrayIconClassObj().tick()
        self.hide()
    def msgbtn(self,i):
        #self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowStaysOnTopHint)
        txt = i.text()
        if(txt=="OK" or txt=="oK" or txt=="ok" or txt=="Ok"):
            self.delayshutdown()
if( __name__ == '__main__'):
    app=QtWidgets.QApplication(sys.argv)
    w = Form()
    w.showFormDialog()
    sys.exit(app.exec())
