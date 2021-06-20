import json         as JSON
import json.encoder as JENOCODER
import socket       as SOCKET   ## socket連線模組 ##

import threading    as THREAD   ## 多執行緒模組 ##
import os           as OS       ## 調用操作系統命令，來達成建立文件，刪除文件，查詢文件的模組 ##
import sys          as SYS
import time         as TIME
import pprint       as PPRINT
from util.command import Command
from util.condition import Condition
from util.model     import Model   # 用來 Print 出好看得 Map


class FileConfig():
    CONFIG = None
    def __init__(self) -> None:
        pass

    def __init__() -> None:
        with open('dict/config.txt', 'r+') as file:
            FileConfig.CONFIG = eval( file.read() )  # 讀取的str轉換為字典
        pass


    
class SpeechRecognizeAgent():
    def __init__(self) -> None:
        self._model     = Model()
        self._condition = Condition()
        self._status   = "隨時"


        command = self._condition.similarCondition( self._model.getCommandsByStatus( self._status ),  ["今天","我","想要", "供給"] )
        if( command != None ):
            print( "(相似詞)最相近的字串: ", command.getChineseName() )

        command = self._condition.pinyinCondition( self._model.getCommandsByStatus( self._status ),  ["今天","我","想要", "供給"] )

        print( "(拼音法)最相近的字串: ", command.getChineseName() )


        self._model.saveDataToFile()
        

if __name__ == "__main__":
    agent = SpeechRecognizeAgent()


