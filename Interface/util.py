

from typing             import List, Tuple
from PyQt5.QtCore       import QThread, pyqtSignal
import os               as OS
import time             as TIME
import random           as RANDOM

class Utility():
    RESOURCE_PATH           = OS.getcwd() + "\\resources\\"
    IMAGE_RESOURCE_PATH     = OS.getcwd() + "\\resources\\image\\"
    GAME_BOX_GRID           = (20, 15)
    GRIDE_SIZE              = 48
    GAME_UPDATE_TIMER       = 0.25
    MOVE_DIRECTION          = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    MOVE_DIRECTION_8        = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]
    def __init__(self) -> None:
        pass

    def __init__() -> None:
        pass

    def generatePosition() -> Tuple[int, int]:
        rx = RANDOM.randint( 0, Utility.GAME_BOX_GRID[0] - 1 )
        ry = RANDOM.randint( 0, Utility.GAME_BOX_GRID[1] - 1 )
        return (rx, ry)

    def geteratePositionList( len:int, corner:int ) -> List[Tuple[int, int]]:
        posList:List[Tuple[int, int]]   = []
        rPos = ( RANDOM.randint( 0, Utility.GAME_BOX_GRID[0] - 1 ), RANDOM.randint( 0, Utility.GAME_BOX_GRID[1] - 1 ) )
        posList.append( rPos )

        # 轉角次數
        for i in range( corner + RANDOM.randint( 0, corner ) ):
            # 隨機產生方向
            direct = RANDOM.sample( Utility.MOVE_DIRECTION, 4 )[0]
            # 長度
            for j in range( len + RANDOM.randint( 0, len ) ):

                # 取得新節點
                newPos = (rPos[0] + direct[0], rPos[1] + direct[1])

                #判斷是否在範圍內
                if newPos[0] > (Utility.GAME_BOX_GRID[0] - 1) or newPos[0] < 0 or newPos[1] > (Utility.GAME_BOX_GRID[1] - 1) or newPos[1] < 0:
                    break

                posList.append( newPos )
                rPos = newPos

        return posList

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


