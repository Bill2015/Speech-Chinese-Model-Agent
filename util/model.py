import json         as JSON

import os           as OS       ## 調用操作系統命令，來達成建立文件，刪除文件，查詢文件的模組 ##
import pprint       as PPRINT
from typing         import Dict, List
from util.command   import Command   # 用來 Print 出好看得 Map

# 模型建立
class Model():
    DATA_FILE_PATH = OS.getcwd() + "\\model\\command.json"
    def __init__( self ) -> None:
        self._commands:Dict[str, Command] = {}     # 存放指令的類別

        with open( Model.DATA_FILE_PATH, encoding='utf-8', mode='r+') as file:
            jsonData = JSON.load( file )
        # -----------------------------------

        self._status = {}      # 依照狀態來將指令分類的 Hash
        # 讀取所有指令
        for jcommand in jsonData['指令集']:
            command = Command( jcommand )
            self._commands[ command.getChineseName() ] = command

            # 依狀態將指令分類
            for statusKey in jcommand['狀態'].keys():
                # 判斷 Key 值是否已存在於狀態表裡 (因為我們要以輸入的狀態幫指令分類，以減少搜尋的時間複雜度)
                if( statusKey not in self._status ):
                    self._status[ statusKey ] = {}
                # 判斷此狀態是否已經存在此 物件
                if( command not in self._status[ statusKey ] ):
                    self._status[ statusKey ][ command.getChineseName() ] = command

        # PPRINT.pprint( self._status )

    # 取得指令集
    def getCommands( self ) -> Dict[str, Command]:
        """取得指令集"""
        return self._commands

    # 取得狀態表 
    def getStatusHash( self ) -> Dict[str, Dict[str,Command]]:
        """取得狀態表 """
        return self._commands

    # 依狀態取得指令表 
    def getCommandsByStatus( self, status:str ) -> Dict[str,Command]:
        """依狀態取得指令表 """
        return self._status[ status ]

    # 儲存新的資訊至檔案內
    def saveDataToFile( self ):
        """ 儲存新的資訊至檔案內 """
        data = {}
        data['指令集'] = []
        for command in self._commands.values():
            commandData = {}
            commandData['名稱']         = command.getChineseName()
            commandData['英文名稱']     = command.getEnglishName()
            commandData['可量化']       = command.countable()
            commandData['同義詞']       = command.getSynonymNames()
            commandData['相似詞']       = command.getSimilarNames()
            commandData['狀態']         = command.getStatus()
            data['指令集'].append( commandData )    

        # 寫入檔案
        with open( Model.DATA_FILE_PATH, encoding='utf-8', mode="w") as file:
            JSON.dump( data, file,  ensure_ascii=False)
        pass