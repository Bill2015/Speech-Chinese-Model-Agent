
from PyQt5                      import QtCore, QtWidgets, uic
from PyQt5.QtGui                import QPalette, QPixmap
from PyQt5.QtWidgets            import (QCheckBox, QDialog, QFileDialog, QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QSizePolicy, QSpinBox, QVBoxLayout, QWidget)

import os                       as OS
import random                   as RANDOM
from Interface.util             import Utility



class GameBox(QFrame):

    def __init__(self, parent=None, index=0, size=32 ) -> None:
        QFrame.__init__( self, parent=parent )

        self.setObjectName( "gameBox" + str(index) )
        self.setFixedSize(size, size)
        self.setGeometry(0, 0, size, size)
        self.setSizePolicy( QSizePolicy.Fixed, QSizePolicy.Fixed )
        self.setAutoFillBackground( True )
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet( "background-color: rgb(198, 255, 198);" )
        
        self._gameLayout = QHBoxLayout()
        self._gameLayout.setContentsMargins(0, 0, 0, 0)
        self._gameLayout.setSpacing( 0 )
        self.setLayout( self._gameLayout )

        self._isObstruction = False
        self._emenyOn       = False
        self._playerOn      = False



    def removeContent( self ):
        self._isObstruction = False
        self._playerOn      = False
        self._emenyOn       = False
        #self.setStyleSheet( "background-color: rgb(198, 255, 198);;" )
        
    def addObject( self, entity ):
        #self.setStyleSheet( "background-color: red;" )
        self._gameLayout.addWidget( entity )
        self._isObstruction = True

        from Interface.entity           import EnemyLabel, PlayerLabel
        if( isinstance( entity, PlayerLabel ) ):
            self._playerOn = True
        elif( isinstance( entity, EnemyLabel ) ):
            self._emenyOn = True
      #  elif( isinstance( entity, StoneObject ) ):
       #     self.setStyleSheet( "background-color: rgb(167, 167, 175);" )

    def getObject( self ):
        if( len( self.children() ) >= 2 ):
            return self.children()[1]
        return None

    def isObstruction( self ):
        return self._isObstruction

    def isPlayerOn( self ):
        return self._playerOn

    def isEnemyOn( self ):
        return self._emenyOn
    
