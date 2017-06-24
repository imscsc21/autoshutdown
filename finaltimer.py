import qtTray
import timer2
import sys
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
def main():
    app=QtWidgets.QApplication(sys.argv)
    #w = timer2.Form()
    w = QtWidgets.QWidget()
    trayIcon = qtTray.SystemTrayIcon(QtGui.QIcon("tmricon.png"), w)
    trayIcon.show()
    print("start program")
    sys.exit(app.exec())
if(__name__=='__main__'):
    main()
    