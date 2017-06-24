class ValueDelegate():
    def __init__(self,traycls=None):
        self.__initValues()
        self.setTrayIconClassObj(traycls)
    def __initValues(self):
        self.__tray_cls = None
        
    def setTrayIconClassObj(self,cls):
        self.__tray_cls = cls
    def getTrayIconClassObj():
        return self.__tray_cls