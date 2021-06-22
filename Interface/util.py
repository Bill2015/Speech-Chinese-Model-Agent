
import os               as OS
import time             as TIME
from typing             import List
from PyQt5.QtCore       import QThread, pyqtSignal

class Utility():
    RESOURCE_PATH           = OS.getcwd() + "\\resources\\"
    IMAGE_RESOURCE_PATH     = OS.getcwd() + "\\resources\\image\\"
    GAME_BOX_GRID           = (15, 15)
    GRIDE_SIZE              = 48
    GAME_UPDATE_TIMER       = 0.25
    def __init__(self) -> None:
        pass

    def __init__() -> None:
        pass


# very testable class (hint: you can use mock.Mock for the signals)
class Worker(QThread):
    _signal = pyqtSignal()

    def __init__(self, parent=None, timer=1):
        super(Worker, self).__init__(parent)
        self._working = True
        self._await   = True
        self._timer   = timer

    def __del__(self):
        self._working = False
        self._await = True
        self.wait()

    def setWork( self, flag:bool ):
        self._working = flag

    def getSignal( self ):
        return self._signal


    def run(self):
        while self._await == True:
            TIME.sleep( 1 ) # a delay

            while self._working == True:
                # 發出訊號
                self._signal.emit()
                TIME.sleep( self._timer )


