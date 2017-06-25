import sys
import timer2
import appdelegate
import time
import threading
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtWidgets.QMenu(parent)
        self.notiform = timer2.Form(appdelegate.ValueDelegate(self))
        #notifyAction = menu.addAction("Force show")
        #notifyAction.triggered.connect(self.showNotificationForm)
        self.thkill = threading.Event()
        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(self.trayexit)
        self.setContextMenu(menu)
        self.thtimer = QtCore.QTimer()
        self.thtimer.timeout.connect(self.countTime2)
        self.default_time_sec = 2*60*60
        self.current_time_sec = 60
        self.tick()
    def getFormattedString(self,mTimeSec):
        return str(int(int(mTimeSec)//3600))+":"+str(int(int(mTimeSec)//60))+":"+str((int(mTimeSec)%60))
    def getCurrentTimeSec(self):
        return self.current_time_sec
    def getDefaultTimeSec(self):
        return self.default_time_sec
    def getForceStopThreadState(self):
        try:
            return self.__force_stop
        except :
            self.__force_stop = False
            return self.getForceStopThreadState()
    def toggleForceStopThread(self):
        self.__force_stop= not getForceStopThreadState()
    def getCountCondi(self,tmren):
        if(tmren is True):
            time.sleep(1)
        return self.getForceStopThreadState() 
    def setCurrentTimeSec(self,tm):
        self.current_time_sec = tm
    def setDefaultTimeSec(self,tm):
        self.default_time_sec = tm
    def getTimeGap(self):
        return self.getDefaultTimeSec()-self.getCurrentTimeSec()
    def countTime(self):
        while( not self.thkill.wait(1)):
            if(self.default_time_sec-self.current_time_sec>=0):
                self.current_time_sec = self.current_time_sec+60
            else:
                self.showNotificationForm()
                break
    def countTime2(self):
        print("call countTime2",self.getFormattedString(self.current_time_sec))
        if(not self.getCountCondi(False)):
            if(self.default_time_sec-self.current_time_sec-self.notiform.getRemainTime()>0):
                self.current_time_sec = self.current_time_sec+60
            else:
                self.thtimer.stop()
                self.showNotificationForm()
        else:
            self.thtimer.stop()
    def tick(self):
        self.setCurrentTimeSec(60)
        self.thtimer.start(60*1000)
    def showNotificationForm(self):
        self.notiform.showFormDialog()
    def trayexit(self):
        try:
            self.thtimer.stop()
        except:
            print("can't stop timer before exit")
        QtCore.QCoreApplication.exit()
def runTray():
    print("call runTray")
    w = QtWidgets.QWidget()
    trayIcon = SystemTrayIcon(QtGui.QIcon("tmricon.png"), w)
    trayIcon.show()
def traymain():
    app = QtWidgets.QApplication(sys.argv)
    runTray()
    sys.exit(app.exec_())

if __name__ == '__main__':
    traymain()