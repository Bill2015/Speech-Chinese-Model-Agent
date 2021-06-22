from typing             import List
from PyQt5              import QtWidgets, uic
from PyQt5.QtWidgets    import (QCheckBox, QDialog, QFileDialog, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QSpinBox, QVBoxLayout, QWidget)
from PyQt5.QtGui        import *
from PyQt5.QtCore       import *
from PyQt5.uic.uiparser import QtCore 

import os               as OS
from Interface.gameBox  import GameBox
from Interface.util     import Utility, Worker
from Interface.entity   import EnemyLabel, EntityLabel, PlayerLabel, SlimeLabel


class GameMainUi(QtWidgets.QMainWindow):
    PLAYER_NO_MOVE      = 0
    PLAYER_MOVE_UP      = 1
    PLAYER_MOVE_DWON    = 2
    PLAYER_MOVE_LEFT    = 3
    PLAYER_MOVE_RIGHT   = 4

    def __init__(self) -> None:
        QtWidgets.QMainWindow.__init__(self)

        uic.loadUi( Utility.RESOURCE_PATH + "gameWidget.ui", self )

        # 主要遊戲網格
        self._mainGameWidget:QWidget        = self.findChild( QWidget, name='gameMainWidget' )
        self._mainLayout:QGridLayout        = self._mainGameWidget.layout()
        self._grid: List[List[GameBox]]     = []

        self._playerLabel:PlayerLabel            = PlayerLabel(7, 7)
        self._entityList:List[EntityLabel]       = []
        self._entityList.append( self._playerLabel )
        self._entityList.append( SlimeLabel(7, 10) )
        self._entityList.append( SlimeLabel(9, 13) )
        self._entityList.append( SlimeLabel(5, 7) )
        self._entityList.append( SlimeLabel(11, 2) )
        self._entityList.append( SlimeLabel(12, 6) )
        self._entityList.append( SlimeLabel(8, 2) )
        self._entityList.append( SlimeLabel(7, 2) )
        self._entityList.append( SlimeLabel(13, 5) )
        self._entityList.append( SlimeLabel(2, 2) )

        # 初始化遊戲網格
        self._initialGameGrid()

        # 建立新執行緒，將自定義訊號sinOut連線到slotAdd()槽函式
        self._monitorThread = Worker( timer=Utility.GAME_UPDATE_TIMER )
        self._monitorThread.getSignal().connect( self._updater )
        self._monitorThread.setWork( True )    
        self._monitorThread.start()

        for entity in self._entityList:
            [px, py] = entity.getPosition()
            self._grid[ px ][ py ].addEntity( entity )

    # ===========================================================
    # ====================== 初始化遊戲網格 ======================
    def _initialGameGrid( self ):
        for i in range( Utility.GAME_BOX_GRID[0]  ):
            tempList = []
            for j in range( Utility.GAME_BOX_GRID[1] ):
                gameBox = GameBox( index=i, size=Utility.GRIDE_SIZE )
                tempList.append( gameBox )
                self._mainLayout.addWidget( gameBox, j, i, Qt.AlignmentFlag.AlignCenter )

            self._grid.append( tempList )

    # ===========================================================
    # ======================== 遊戲更新器 ========================
    def _updater( self ):

        for entity in self._entityList:
            if( isinstance(entity, PlayerLabel) ):
                
                pass

            elif( isinstance(entity, EnemyLabel) ):
                path = entity.pathFinding().find( self._grid, entity.getPosition(), self._playerLabel.getPosition() )
                if( len( path ) >= 2 ):
                    entity.moveTo( path[1][0], path[1][1] )
                

            entity.updateAI( self._grid )



            
        print( "更新中！" )


    def playerMove( self, move=0 ):
        if( move == GameMainUi.PLAYER_NO_MOVE ):
            pass
        elif( move == GameMainUi.PLAYER_MOVE_UP ):
            self._playerLabel.move(0, -1)
        elif( move == GameMainUi.PLAYER_MOVE_DWON ):
            self._playerLabel.move(0, 1)
        elif( move == GameMainUi.PLAYER_MOVE_LEFT ):
            self._playerLabel.move(-1, 0)
        elif( move == GameMainUi.PLAYER_MOVE_RIGHT ):
            self._playerLabel.move(1, 0)