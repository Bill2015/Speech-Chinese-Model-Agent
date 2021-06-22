

import abc          as ABC
from typing         import Dict, List

from pypinyin       import lazy_pinyin
from Util.command   import ActionCommand, ActionParameter, Command
from Util.model     import Model


class Condition():
    def __init__(self ) -> None:
        pass
    
    @ABC.abstractclassmethod
    def execute( self, commandMap:Dict[str, Command] , tokens:List[str]  ):
        return NotImplemented

    @ABC.abstractclassmethod
    def getConditionName( self ):
        return NotImplemented

# ==================================================================================================
class SimpleCondition( Condition ):
    def __init__(self) -> None:
        pass

    def execute(self, commandMap: Dict[str, Command], tokens: List[str]) -> Command:
        """以最簡單比對去做指令字串比對

        Args:
            model (Model): 模型
            tokens (List[str]): 分割後的自串

        Returns:
            Command: 回傳出指令
        """
        # 取得所有指令
        for token in tokens:
            if( token in commandMap.keys() ):
                return commandMap[ token ]
        return None

    def getConditionName(self):
        return "一般判斷"
# ==================================================================================================
class SynonymCondition( Condition ):
    def __init__(self) -> None:
        pass

    # 只判斷是否與指令的同義詞一樣
    def execute( self, commandMap:Dict[str, Command] , tokens:List[str] ) -> Command:
        """以最簡單比對去做指令字串比對 同義詞

        Args:
            model (Model): 模型
            tokens (List[str]): 分割後的自串

        Returns:
            Command: 回傳出指令
        """
        # 取得所有指令
        for token in tokens:
            for key in commandMap.keys():
                if( isinstance(commandMap[ key ], ActionCommand) and token in commandMap[ key ].getSynonymNames() ):
                    return commandMap[ key ]
        return None
    
    def getConditionName(self):
        return "同義字判斷"
# ==================================================================================================
class SimilarCondition( Condition ):
    def __init__(self) -> None:
        pass
    
    # 只判斷是否與指令的相似詞的一樣名稱
    def execute( self, commandMap:Dict[str, Command] , tokens:List[str] ) -> Command:
        """以最簡單比對去做指令字串比對 相似詞

        Args:
            model (Model): 模型
            tokens (List[str]): 分割後的自串

        Returns:
            Command: 回傳出指令
        """
        # 取得所有指令
        for token in tokens:
            for key in commandMap.keys():
                if( isinstance(commandMap[ key ], ActionCommand) and token in commandMap[ key ].getSimilarNames() ):
                    return commandMap[ key ]
        return None

    def getConditionName(self):
        return "相似字判斷"
# ==================================================================================================
class PinyionCondition( Condition ):
    def __init__(self) -> None:
        pass

    # 拼音比對
    def execute( self, commandMap:Dict[str, Command], tokens:List[str] ) -> Command:
        minimum = 99
        minimumKey = ""
        # 取得所有指令
        for token in tokens:
            # 取得目標字串拼音
            roma = "-".join( lazy_pinyin( token ) )
            # 將每個指令取出
            for key in commandMap.keys():
                
                # 只判斷 ActionCommand
                if( isinstance(  commandMap[ key ], ActionCommand ) ):
                    # 取得指令拼音 (原本的詞拼音 + 同義字拼音)
                    for commandRoma in [ commandMap[ key ].getRomaPinyin() ] + commandMap[ key ].getSynonymRomas():

                        # 假如兩者字串長度差距過大就略過，以節省運算時間
                        if( abs( len( roma ) - len( commandRoma ) ) > 5 ):
                            continue

                        distance = self._levenshteinDistance( roma, commandRoma )
                        print( "字串A：{token}({roma}), 字串B:{key}({roma2}), 距離為：{distance}".format( token=token, roma=roma, key=key, roma2=commandRoma, distance=distance ) )
                        if( distance < minimum ):
                            minimum = distance
                            minimumKey = key
        
        if( minimum > 5 ):
            return None
        else:
            return commandMap[ minimumKey ]

    
    # 編輯距離計算
    def _levenshteinDistance(self, str1:str, str2:str) -> int:
        """計算兩者字串的編輯距離

        Args:
            str1 ([str]): 字串 1
            str2 ([str]): 字串 2

        Returns:
            [int]: 距離，越大代表差距越大
        """
        matrix = [[ i + j for j in range(len(str2) + 1)] for i in range(len(str1) + 1)]
        for i in range(1, len(str1) + 1):
            for j in range(1, len(str2) + 1):
                d = 0 if str1[ i - 1 ] == str2[ j - 1 ] else 1
                matrix[i][j] = min( matrix[ i - 1 ][ j ] + 1, matrix[ i ][ j- 1 ] + 1, matrix[ i - 1 ][ j - 1 ] + d)
        return matrix[ len(str1) ][ len(str2) ]

    def getConditionName(self):
        return "拼音判斷"