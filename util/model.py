import json         as JSON

import os           as OS       ## 調用操作系統命令，來達成建立文件，刪除文件，查詢文件的模組 ##
import pprint       as PPRINT
from typing         import Dict, List, Set
from Util.command   import ActionCommand, ActionParameter, Command   # 用來 Print 出好看得 Map

# 模型建立
class Model():
    COMMAND_FILE_PATH = OS.getcwd() + "\\model\\command.json"
    PARAMETER_FLIE_PATH = OS.getcwd() + "\\model\\parameter.json"

    def __init__( self ) -> None:
        self._commands:Dict[str, ActionCommand]                 = {}     # 存放 "指令" 的類別
        self._commandStatus:Dict[Dict[str, ActionCommand]]      = {}     # 依照狀態來將 "指令" 分類的 Hash
        self._parameters:Dict[str, ActionParameter]             = {}     # 存放 "參數"
        self._parameterStatus:Dict[Dict[str, ActionParameter]]  = {}     # 依照狀態來將 "參數" 分類的 Hash


        with open( Model.COMMAND_FILE_PATH, encoding='utf-8', mode='r+') as file:
            jsonData = JSON.load( file )
        # -----------------------------------
            self._commandStatus = {}      # 依照狀態來將指令分類的 Hash

            # 讀取所有指令
            for jcommand in jsonData['指令集']:
                command = ActionCommand( jcommand )
                self._commands[ command.getChineseName() ] = command

                # 依狀態將指令分類
                for statusKey in jcommand['狀態'].keys():
                    # 判斷 Key 值是否已存在於狀態表裡 (因為我們要以輸入的狀態幫指令分類，以減少搜尋的時間複雜度)
                    if( statusKey not in self._commandStatus ):
                        self._commandStatus[ statusKey ] = {}
                    # 判斷此狀態是否已經存在此 物件
                    if( command not in self._commandStatus[ statusKey ] ):
                        self._commandStatus[ statusKey ][ command.getChineseName() ] = command

        # PPRINT.pprint( self._status )

        # -----------------------------------
        with open( Model.PARAMETER_FLIE_PATH, encoding='utf-8', mode='r+') as file:
            jsonData = JSON.load( file )

            for jpermeter in jsonData['參數集']:
                parameter = ActionParameter( jpermeter )
                self._parameters[ parameter.getChineseName() ] = parameter
    
                # 依狀態將指令分類
                for statusKey in jpermeter['狀態'].keys():
                    # 判斷 Key 值是否已存在於狀態表裡 (因為我們要以輸入的狀態幫指令分類，以減少搜尋的時間複雜度)
                    if( statusKey not in self._parameterStatus ):
                        self._parameterStatus[ statusKey ] = {}
                    # 判斷此狀態是否已經存在此 物件
                    if( parameter not in self._parameterStatus[ statusKey ] ):
                        self._parameterStatus[ statusKey ][ parameter.getChineseName() ] = parameter

        # --------------------------------
        # 載入停止詞
        self._stopwordSet = set()
        with open('resources/stopwords.txt','r', encoding='utf-8') as stopwords:
            for stopword in stopwords:
                 self._stopwordSet.add(stopword.strip('\n'))

    def getStopwordSet( self ) -> Set[str]:
        return self._stopwordSet

    # 取得指令集
    def getCommands( self ) -> Dict[str,  ActionCommand]:
        """取得指令集"""
        return self._commands

    # 依狀態取得指令表 
    def getCommandsByStatus( self, status:str ) -> Dict[str, ActionCommand]:
        """依狀態取得指令表 """
        return self._commandStatus[ status ]

    # 儲存新的資訊至檔案內
    def saveDataToFile( self ):
        """ 儲存新的資訊至檔案內 """
        # ----------------------------------------------------
        # 將指令資料寫入
        commandData = {}
        commandData['指令集'] = []
        for command in self._commands.values():
            data = {}
            data['名稱']         = command.getChineseName()
            data['可量化']       = command.countable()
            data['同義詞']       = command.getSynonymDict()
            data['相似詞']       = command.getSimilarNames()
            data['狀態']         = command.getStatus()
            commandData['指令集'].append( data )    

        # ----------------------------------------------------
        # 將參數資料寫入
        parameterData = {}
        parameterData['參數集'] = []
        for parameterSet in self._parameters.values():
            data = {}
            data['名稱']         = parameterSet.getChineseName()
            data['可量化']       = parameterSet.countable()
            data['狀態']         = parameterSet.getStatus()
            data['詞集']         = {}
            # 取出內參數
            for key, parameter in parameterSet.getParameters().items():
                pData = {}
                pData[ key ] = {}
                pData[ key ]['同義詞']      = parameter.getSynonymDicts()
                pData[ key ]['相似詞']      = parameter.getSimilarNames()
            
                data['詞集'] = pData    
            parameterData['參數集'].append( data ) 

        # 寫入檔案
        with open( Model.COMMAND_FILE_PATH, encoding='utf-8', mode="w") as file:
            JSON.dump( commandData, file,  ensure_ascii=False)
        pass

        # 寫入檔案
        with open( Model.PARAMETER_FLIE_PATH, encoding='utf-8', mode="w") as file:
            JSON.dump( parameterData, file,  ensure_ascii=False)
        pass