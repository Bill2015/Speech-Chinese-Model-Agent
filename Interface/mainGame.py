import sys
from typing             import List
from PyQt5              import QtWidgets, uic
from PyQt5.QtWidgets    import (QCheckBox, QDialog, QFileDialog, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QSpinBox, QVBoxLayout, QWidget)
from PyQt5.QtGui        import *
from PyQt5.QtCore       import *
from PyQt5.uic.uiparser import QtCore 

import os               as OS

from Interface.gameBox  import GameBox
from Interface.util     import Utility, Worker
from Interface.entity   import EnemyLabel, EntityLabel, PlayerLabel, SlimeLabel, StoneObject


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
        self._mainGameWidget:QWidget            = self.findChild( QWidget, name='gameMainWidget' )
        self._mainLayout:QGridLayout            = self._mainGameWidget.layout()
        self._grid: List[List[GameBox]]         = []

        self._playerLabel:PlayerLabel           = None
        self._entityList:List[EntityLabel]      = []


        # 初始化遊戲網格
        self._initialGameGrid()
        self._mapGenerator()

        # 建立新執行緒，將自定義訊號sinOut連線到slotAdd()槽函式
        #self._monitorThread = Worker( timer=Utility.GAME_UPDATE_TIMER )
        #self._monitorThread.getSignal().connect( self._updater )
        #self._monitorThread.setWork( True )    
        #self._monitorThread.start()

       # self._mainGameWidget.keyPressed.connect( self.onKey )
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
    # ======================== 地圖產生器 ========================
    def _mapGenerator( self ):
        dx, dy = Utility.generatePosition()
        self._playerLabel           = PlayerLabel( dx, dy )
        self._entityList.append( self._playerLabel )
        self._grid[ dx ][ dy ].addObject( self._playerLabel )

        # ----------------------------
        i = 0
        while i < 5:
            for pos in Utility.geteratePositionList( 3, 6 ):
                if( self._grid[ pos[0] ][ pos[1] ].isObstruction() == False ):
                    stone = StoneObject(pos[0], pos[1] )
                    self._grid[ pos[0] ][ pos[1] ].addObject( stone )
            i += 1
        # ----------------------------
        i = 0
        while i < 1:
            dx, dy = Utility.generatePosition()
            
            if( self._grid[ dx ][ dy ].isObstruction() == False ):
                slime = SlimeLabel( dx, dy )
                # 確保敵人與玩家之間有路徑
                path = slime.pathFinding().find( self._grid, slime.getPosition(), self._playerLabel.getPosition() )
                if( path != None and len( path ) >= 2 ):
                    self._grid[ dx ][ dy ].addObject( slime )
                    self._entityList.append( slime )
                    i += 1

    # ===========================================================
    # ======================== 遊戲更新器 ========================
    def _updater( self ):

        

        for entity in self._entityList:
            if( isinstance(entity, PlayerLabel) ):
                
                pass

            elif( isinstance(entity, EnemyLabel) ):
                path = entity.pathFinding().find( self._grid, entity.getPosition(), self._playerLabel.getPosition() )
                if( path != None and len( path ) >= 2 ):
                    entity.moveTo( path[1][0], path[1][1] )

            entity.updateAI( self._grid )



            
       # print( "更新中！" )
    def keyPressEvent(self, event):
        super(GameMainUi, self).keyPressEvent(event)
        self.onKey( event )
        self._updater()

    def onKey(self, event):
        if event.key() == Qt.Key_Up:
            self.playerMove( GameMainUi.PLAYER_MOVE_UP )
        elif event.key() == Qt.Key_Down:
            self.playerMove( GameMainUi.PLAYER_MOVE_DWON )
        elif event.key() == Qt.Key_Left:
            self.playerMove( GameMainUi.PLAYER_MOVE_LEFT )
        elif event.key() == Qt.Key_Right:
            self.playerMove( GameMainUi.PLAYER_MOVE_RIGHT )
        elif event.key() == Qt.Key_Q:
            sys.exit(0)



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