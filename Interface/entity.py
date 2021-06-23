from math import fabs
from Interface.gameBox import GameBox
from typing                     import List, Tuple
from PyQt5                      import QtCore, QtWidgets, uic
from PyQt5.QtGui                import QCursor, QPalette, QPixmap
from PyQt5.QtWidgets            import (QAction, QCheckBox, QDialog, QFileDialog, QFrame, QHBoxLayout, QLabel, QLineEdit, QMenu, QProgressBar, QPushButton, QScrollArea, QSizePolicy, QSpinBox, QVBoxLayout, QWidget)
from Interface.util             import Utility
import random                   as RANDOM
import abc                      as ABC

# ========================================================================
class GameObject( QWidget ):
    def __init__( self, iniX=0, iniY=0, imagePath="" ):
        QWidget.__init__( self )
        self._icon:QLabel   = QLabel()
        self._preX:int      = iniX
        self._preY:int      = iniY 
        self._posX:int      = iniX 
        self._posY:int      = iniY
        self._initialImage( imagePath )
        self._vlayout       = QVBoxLayout()
        self._vlayout.setContentsMargins( 3, 5, 3, 0 )
        self._vlayout.setSpacing( 0 )
        self.setLayout( self._vlayout )
        self._vlayout.addWidget( self._icon )

    def _initialImage( self, imagePath ):
        self._icon.setScaledContents( True )
        pixmap = QPixmap()
        if( pixmap.load( Utility.IMAGE_RESOURCE_PATH + imagePath )):
            pixmap.scaled( self.size(),  QtCore.Qt.KeepAspectRatio)      
            self._icon.setPixmap( pixmap )
        else:
            print( "圖片讀取錯誤！" )
# ========================================================================
class StaticObject( GameObject ):
    IMAGE_PATH_STONE    = "stone-{index}.png"
    def __init__( self, iniX=0, iniY=0, imagePath="" ):
        GameObject.__init__( self, iniX, iniY, imagePath )

# ========================================================================
class StoneObject( StaticObject ):
    def __init__( self, iniX=0, iniY=0 ):
        StaticObject.__init__( self, iniX, iniY, StaticObject.IMAGE_PATH_STONE.format( index=RANDOM.randint(0, 8) ) )

# ========================================================================
class EntityLabel( GameObject ):
    IMAGE_PATH_PLAYER = "player-stand.png"
    IMAGE_PATH_SLIME  = "enemy-slime.png"
    def __init__( self, iniX=0, iniY=0, imagePath="" ):
        GameObject.__init__( self, iniX, iniY, imagePath )
        self._health = 100

    def moveTo( self, x, y ):
        self._preX   =   self._posX
        self._preY   =   self._posY 
        self._posX = min( max( 0, x ), Utility.GAME_BOX_GRID[0] - 1)
        self._posY = min( max( 0, y ), Utility.GAME_BOX_GRID[1] - 1)

    def move( self, dx, dy ):
        self._preX   =   self._posX
        self._preY   =   self._posY 
        self._posX = min( max( 0, self._posX + dx ), Utility.GAME_BOX_GRID[0] - 1)
        self._posY = min( max( 0, self._posY + dy ), Utility.GAME_BOX_GRID[1] - 1)


    def getPosition( self ) -> Tuple[int, int]:
        return (self._posX, self._posY)

    def getPrePosition( self ) -> Tuple[int, int]:
        return (self._preX, self._preY)



    def updateAI( self, maze:List[List[GameBox]] ):
        if( (self._posX != self._preX) or (self._posY != self._preY) ):
            maze[ self._preX ][ self._preY ].removeContent()
            maze[ self._posX ][ self._posY ].addObject( self )
            self._preX   =   self._posX
            self._preY   =   self._posY 
        return NotImplemented


    def damage( self, damage:int, attacker:GameObject ):
        self._health -= damage

    

# ========================================================================
class PlayerLabel( EntityLabel ):
    def __init__(self, iniX=0, iniY=0):
        EntityLabel.__init__( self, iniX, iniY, EntityLabel.IMAGE_PATH_PLAYER  )

        self.setObjectName( "playerLabel")

    def updateAI(self, maze:List[List[QFrame]]):
        return super().updateAI( maze=maze )
        

# ========================================================================
# ==========================  敵人的類別  =================================

class EnemyLabel( EntityLabel ):
    def __init__(self, iniX=0, iniY=0, imagePath="" ):
        EntityLabel.__init__( self, iniX, iniY, imagePath  )
        from Interface.Ai import AStarPathFinding 
        self._pathFindingAI     = AStarPathFinding()
        self._healthBar         = QProgressBar()
        self._healthBar.setValue( 80 )
        self._healthBar.setMaximum( 100 )
        self._healthBar.setMaximumHeight( 3 )
        self._healthBar.setSizePolicy( QSizePolicy.Preferred, QSizePolicy.Maximum )
        self._healthBar.setAlignment( QtCore.Qt.AlignmentFlag.AlignCenter )
        styleText = """QProgressBar#healthBar{
                        background-color: rgb(191, 255, 187);
                        border-style: none;
                        border-color: rgb(131, 131, 131);
                        border-radius: 5px;
                    }
                    QProgressBar#healthBar::chunk:horizontal {
                        background: red;
                        border-style: none;
                        border-color: white;
                        border-radius: 5px;
                    }"""
        self._healthBar.setObjectName( "healthBar" )
        self._healthBar.setStyleSheet( styleText )
        self._vlayout.addWidget( self._healthBar )
        self._vlayout.addWidget( self._icon )

    def pathFinding( self ):
        return self._pathFindingAI
    
    def updateAI(self, maze:List[List[GameBox]]):
        return super().updateAI( maze=maze )

# ========================================================================
class SlimeLabel( EnemyLabel ):
    def __init__(self, iniX=0, iniY=0):
        EnemyLabel.__init__( self, iniX, iniY, EntityLabel.IMAGE_PATH_SLIME  )


    def updateAI(self, maze:List[List[GameBox]]):
        # for direct in Utility.MOVE_DIRECTION: # Adjacent squares

        #     newPos = (self._posX + direct[0], self._posY + direct[1])
        #     # Make sure within range
        #     if newPos[0] > (Utility.GAME_BOX_GRID[0] - 1) or newPos[0] < 0 or newPos[1] > (Utility.GAME_BOX_GRID[1] - 1) or newPos[1] < 0:
        #         continue

        #     if( maze[ newPos[0] ][ newPos[1] ].isPlayerOn() == True ):
        #         playerLabel = maze[ newPos[0] ][ newPos[1] ].getObject()
        #         if( isinstance( playerLabel, PlayerLabel ) ):
        #             playerLabel.damage( 20, self )
    
        return super().updateAI( maze=maze )
