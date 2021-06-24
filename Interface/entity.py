
from PyQt5 import QtGui
from Interface.gameBox          import GameBox
from typing                     import List, Tuple
from PyQt5                      import QtCore, QtWidgets, uic
from PyQt5.QtGui                import QCursor, QPalette, QPixmap
from PyQt5.QtWidgets            import ( QGraphicsOpacityEffect, QHBoxLayout, QLabel, QProgressBar, QSizePolicy, QVBoxLayout, QWidget)
from Interface.util             import Utility
from Interface.obj              import InfoWidget
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
        self._maxHealth = 100
        self._health    = 100
        self._isMoved   = False
        self._healthBar         = QProgressBar()
        self._healthBar.setValue( self._health )
        self._healthBar.setMaximum( self._maxHealth )
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

        self._deathEffect = QGraphicsOpacityEffect( self )
        self._deathAnimation = QtCore.QPropertyAnimation( self._deathEffect, b"opacity" )
        self.setGraphicsEffect( self._deathEffect )
        self._deathAnimation.setKeyValueAt( 0, 1.0 )
        self._deathAnimation.setKeyValueAt( 0.5, 0 )
        self._deathAnimation.setKeyValueAt( 0.75, 1.0 )
        self._deathAnimation.setKeyValueAt( 0.85, 0 )
        self._deathAnimation.setKeyValueAt( 0.875, 1.0 )
        self._deathAnimation.setKeyValueAt( 0.900, 0.0 )
        self._deathAnimation.setKeyValueAt( 0.925, 1.0 )
        self._deathAnimation.setKeyValueAt( 0.950, 0.0 )
        self._deathAnimation.setKeyValueAt( 0.975, 1.0 )
        self._deathAnimation.setKeyValueAt( 1.000, 0.0 )
        self._deathAnimation.setDuration( 500 )
                
        self._infoWidget = InfoWidget( self )
        self._infoWidget.hide()
        self.layout().addWidget( self._infoWidget  )

    def moveTo( self, x, y ):
        self._preX   =   self._posX
        self._preY   =   self._posY 
        self._posX = min( max( 0, x ), Utility.GAME_BOX_GRID[0] - 1)
        self._posY = min( max( 0, y ), Utility.GAME_BOX_GRID[1] - 1)

    def move( self, dpos:Tuple[int, int], maze:List[List[GameBox]] ):
        self._preX   =   self._posX
        self._preY   =   self._posY
        self._posX = min( max( 0, self._posX + dpos[0] ), Utility.GAME_BOX_GRID[0] - 1)
        self._posY = min( max( 0, self._posY + dpos[1] ), Utility.GAME_BOX_GRID[1] - 1)
        #新增的部分
        if( maze[ self._posX ][ self._posY ].isObstruction() == True ):
            self._posX = self._preX
            self._posY = self._preY

    def getPosition( self ) -> Tuple[int, int]:
        return (self._posX, self._posY)

    def getPrePosition( self ) -> Tuple[int, int]:
        return (self._preX, self._preY)

    def isMoved( self ) -> bool:
        return ((self._posX != self._preX) or (self._posY != self._preY))

    def isDeath( self ):
        return (self._health <= 0)

    def updateAI( self, maze:List[List[GameBox]] ):
        if( self.isDeath() == True ):
            self._deathAnimation.finished.connect( lambda: self._destorySelf( maze ) )
            self._deathAnimation.start() 

        if( (self._posX != self._preX) or (self._posY != self._preY) ):
            maze[ self._preX ][ self._preY ].removeContent()
            maze[ self._posX ][ self._posY ].addObject( self )
            self._preX   =   self._posX
            self._preY   =   self._posY 



        return NotImplemented


    def _destorySelf( self, maze:List[List[GameBox]] ):
        """解建構，當敵人死去時
        Args:
            maze (List[List[GameBox]]): [description]
        """
        maze[ self._posX ][ self._posY ].removeContent()
        self.deleteLater()





    def damage( self, damage:int, attacker:GameObject ):
        self._health = max( 0,  self._health - damage )
        self._healthBar.setValue( self._health )
        self._infoWidget.setText( "-{damage}".format(damage=damage) )
        pos = self.mapToGlobal( QtCore.QPoint(0, 0) )
        self._infoWidget.showInfo( pos )

    

# ========================================================================
class PlayerLabel( EntityLabel ):
    def __init__(self, iniX=0, iniY=0):
        EntityLabel.__init__( self, iniX, iniY, EntityLabel.IMAGE_PATH_PLAYER  )

        self.setObjectName( "playerLabel")
        self._healthBar.deleteLater()
        self._maxHealth = 200
        self._health    = 200
        self._healthBar = None

    def setHealthBar( self, healthBar:QProgressBar ):
        self._healthBar = healthBar
        self._healthBar.setMaximum( self._maxHealth )
        self._healthBar.setValue( self._health )

    def updateAI(self, maze:List[List[GameBox]]):
     
        # 判斷附近是否有玩家
        for direct in Utility.MOVE_DIRECTION:
            newPos = (self._posX + direct[0], self._posY + direct[1])
            # Make sure within range
            if newPos[0] > (Utility.GAME_BOX_GRID[0] - 1) or newPos[0] < 0 or newPos[1] > (Utility.GAME_BOX_GRID[1] - 1) or newPos[1] < 0:
                continue

            if( maze[ newPos[0] ][ newPos[1] ].isEnemyOn() == True ):
                # 取得敵人物件
                enemy = maze[ newPos[0] ][ newPos[1] ].getObject()
                if( isinstance( enemy, EnemyLabel ) ):
                    self.damage( 10, enemy )
        super().updateAI( maze=maze )


    def attack( self, maze:List[List[GameBox]], direct:Tuple[int, int] ):
        newPos = (self._posX + direct[0], self._posY + direct[1])
        # Make sure within range
        if newPos[0] > (Utility.GAME_BOX_GRID[0] - 1) or newPos[0] < 0 or newPos[1] > (Utility.GAME_BOX_GRID[1] - 1) or newPos[1] < 0:
            return

        if( maze[ newPos[0] ][ newPos[1] ].isEnemyOn() == True ):
            # 取得敵人物件
            enemy = maze[ newPos[0] ][ newPos[1] ].getObject()
            if( isinstance( enemy, EnemyLabel ) ):
                enemy.damage( 10, self )

# ========================================================================
# ==========================  敵人的類別  =================================

class EnemyLabel( EntityLabel ):
    def __init__(self, iniX=0, iniY=0, imagePath="" ):
        EntityLabel.__init__( self, iniX, iniY, imagePath  )
        from Interface.Ai import AStarPathFinding 
        self._pathFindingAI     = AStarPathFinding()


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
