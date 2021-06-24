
from typing                     import List, Tuple
from PyQt5                      import QtCore, QtWidgets, uic
from PyQt5.QtGui                import QCursor, QFont, QPalette, QPixmap
from PyQt5.QtWidgets            import (QAction, QCheckBox, QDialog, QDockWidget, QFileDialog, QFrame, QGraphicsOpacityEffect, QHBoxLayout, QLabel, QLineEdit, QMenu, QProgressBar, QPushButton, QScrollArea, QSizePolicy, QSpinBox, QToolTip, QVBoxLayout, QWidget)
from Interface.util             import Utility
import random                   as RANDOM
import abc                      as ABC


class InfoWidget( QDockWidget ):
    def __init__(self, parent) -> None:
        QDockWidget.__init__(self, "", parent)
        
        self.setFeatures( QDockWidget.NoDockWidgetFeatures ) 
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setTitleBarWidget( QWidget( None ) )
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing( 0 )
        self._displayText = QLabel( self )
        self._displayText.setText( "" )
        self._displayText.setStyleSheet( 'color:red; font:75 11pt "微軟正黑體";background-color: transparent;' )
        self._displayText.setMaximumSize( 50, 20 )
        self._displayText.setSizePolicy( QSizePolicy.Maximum, QSizePolicy.Maximum )
        self.setWidget( self._displayText )
        self.setFloating( True )
        self.setObjectName("infoWidget")
        self.setStyleSheet(  """QDockWidget#infoWidget{
                        background-color: transparent;
                        border-style: none;
                        }""" )
        self.setBaseSize(0, 0)
        self.setMaximumSize( 50, 20 )
        self.setSizePolicy( QSizePolicy.Maximum, QSizePolicy.Maximum )

        self._fadeEffect = QGraphicsOpacityEffect( self )
        self._fadeAnimation = QtCore.QPropertyAnimation( self._fadeEffect, b"opacity" )
        self.setGraphicsEffect( self._fadeEffect )
        self._fadeAnimation.setStartValue( 1.0 )
        self._fadeAnimation.setEndValue( 0 )
        self._fadeAnimation.setDuration( 500 )
        self._fadeAnimation.finished.connect( self.hide )
        

    def getDisplayLabel( self ) -> QLabel:
        return self._displayText

    def showEvent(self, event):
        if( hasattr( self, '_fadeAnimation'  ) ):
            self._fadeAnimation.start()
        event.accept() 

    def setText( self, text:str ):
        self._displayText.setText( text )

    def showInfo( self, pos:QtCore.QPoint ):
        geomtry = self.geometry()
        self.setGeometry(pos.x() + 12, pos.y() - 16, geomtry.width(), geomtry.height() )
        self.show()

class HistoryLabel( QLabel ):
    def __init__(self, text, parent) -> None:
        QLabel.__init__(self, text, parent)
        self.setStyleSheet( 'color:white; font:75 11pt "微軟正黑體";background-color: transparent;' )
        self.setMaximumSize( 50, 20 )
        self.setSizePolicy( QSizePolicy.Maximum, QSizePolicy.Maximum )
