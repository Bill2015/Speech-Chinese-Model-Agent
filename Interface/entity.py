import abc                      as ABC
from typing                     import List, Tuple
from PyQt5                      import QtCore, QtWidgets, uic
from PyQt5.QtGui                import QPalette, QPixmap
from PyQt5.QtWidgets            import (QCheckBox, QDialog, QFileDialog, QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QSizePolicy, QSpinBox, QVBoxLayout, QWidget)
from Interface.util             import Utility


# ========================================================================
class EntityLabel( QLabel ):
    IMAGE_PATH_PLAYER = "player-stand.png"
    IMAGE_PATH_SLIME  = "enemy-slime.png"
    def __init__( self, iniX=0, iniY=0, imagePath="" ):
        QLabel.__init__( self )
        self._health = 100
        self._preX:int   = iniX
        self._preY:int   = iniY 
        self._posX:int   = iniX 
        self._posY:int   = iniY
        self._initialImage( imagePath )

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

    def _initialImage( self, imagePath ):
        self.setScaledContents( True )
        pixmap = QPixmap()
        if( pixmap.load( Utility.IMAGE_RESOURCE_PATH + imagePath )):
            pixmap.scaled( self.size(),  QtCore.Qt.KeepAspectRatio)      
            self.setPixmap( pixmap )
        else:
            print( "圖片讀取錯誤！" )

    @ABC.abstractclassmethod
    def updateAI( self, ):
        return NotImplemented

    def updatePosition( self, maze:List[List[QFrame]]  ):
        if( (self._posX != self._preX) or (self._posY != self._preY) ):
            maze[ self._preX ][ self._preY ].removeContent()
            maze[ self._posX ][ self._posY ].addEntity( self )

# ========================================================================
class PlayerLabel( EntityLabel ):
    def __init__(self, iniX=0, iniY=0):
        EntityLabel.__init__( self, iniX, iniY, EntityLabel.IMAGE_PATH_PLAYER  )

        self.setObjectName( "playerLabel")

    def updateAI(self, maze:List[List[QFrame]]):
        self.updatePosition( maze )

# ========================================================================
# ==========================  敵人的類別  =================================

class EnemyLabel( EntityLabel ):
    def __init__(self, iniX=0, iniY=0, imagePath="" ):
        EntityLabel.__init__( self, iniX, iniY, imagePath  )
        from Interface.Ai import AStarPathFinding 
        self._pathFindingAI = AStarPathFinding()


    def pathFinding( self ):
        return self._pathFindingAI
    
    def updateAI(self, maze:List[List[QFrame]]):
        self.updatePosition( maze )
# ========================================================================
class SlimeLabel( EnemyLabel ):
    def __init__(self, iniX=0, iniY=0):
        EnemyLabel.__init__( self, iniX, iniY, EntityLabel.IMAGE_PATH_SLIME  )

    def updateAI(self, maze:List[List[QFrame]]):
        self.updatePosition( maze )