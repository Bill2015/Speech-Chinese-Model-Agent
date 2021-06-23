

import abc                  as ABC
from typing                 import Dict, List, Tuple, Tuple

from pypinyin               import lazy_pinyin
from Util.command           import ActionCommand, ActionParameter, Command
from google_trans_new       import google_translator  


class Condition():
    def __init__(self ) -> None:
        pass
    
    @ABC.abstractclassmethod
    def execute( self, commandMap:Dict[str, Command] , token:str  ) -> Tuple[int, Command]:
        return NotImplemented

    @ABC.abstractclassmethod
    def getConditionName( self ):
        return NotImplemented

# ==================================================================================================
class SimpleCondition( Condition ):
    def __init__(self) -> None:
        pass

    def execute(self, commandMap: Dict[str, Command], tokens: List[str]) -> Tuple[int, Command]:
        """以最簡單比對去做指令字串比對

        Args:
            model (Model): 模型
            tokens (List[str]): 分割後的自串

        Returns:
            Command: 回傳出指令
        """
        # 取得所有指令
        for i, token in enumerate(tokens):
            if( token in commandMap.keys() ):
                return (i, commandMap[ token ])
        return (-1, None)

    def getConditionName(self):
        return "一般判斷"
# ==================================================================================================
class SynonymCondition( Condition ):
    def __init__(self) -> None:
        pass

    # 只判斷是否與指令的同義詞一樣
    def execute( self, commandMap:Dict[str, Command] , tokens:List[str] ) -> Tuple[int, Command]:
        """以最簡單比對去做指令字串比對 同義詞

        Args:
            model (Model): 模型
            tokens (List[str]): 分割後的自串

        Returns:
            Command: 回傳出指令
        """
        # 取得所有指令
        for i, token in enumerate(tokens):
            for key in commandMap.keys():
                if( isinstance(commandMap[ key ], ActionCommand) and token in commandMap[ key ].getSynonymNames() ):
                    return (i, commandMap[ key ])
        return (-1, None)
    
    def getConditionName(self):
        return "同義字判斷"
# ==================================================================================================
class SimilarCondition( Condition ):
    def __init__(self) -> None:
        pass
    
    # 只判斷是否與指令的相似詞的一樣名稱
    def execute( self, commandMap:Dict[str, Command] , tokens:List[str] ) -> Tuple[int, Command]:
        """以最簡單比對去做指令字串比對 相似詞

        Args:
            model (Model): 模型
            tokens (List[str]): 分割後的自串

        Returns:
            Command: 回傳出指令
        """
        # 取得所有指令
        for i, token in enumerate(tokens):
            for key in commandMap.keys():
                if( isinstance(commandMap[ key ], ActionCommand) and token in commandMap[ key ].getSimilarNames() ):
                    return (i, commandMap[ key ])
        return (-1, None)

    def getConditionName(self):
        return "相似字判斷"
# ==================================================================================================
class PinyionCondition( Condition ):
    VOWEL = "aeiou "
    def __init__(self) -> None:
        pass

    def GeneratePinyinList( tokens: List[str] ) -> List[str]:
        pinyinList:List[str]       = []
        for token in tokens:
            pinyinList.append( "-".join( lazy_pinyin( token ) ) )
        return pinyinList

    def GeneratePinyin( token:str ):
        return  "-".join( lazy_pinyin( token ) )

    # 拼音比對
    def execute( self, commandMap:Dict[str, Command], originToken:List[str], pinyinTokens:List[str] )  -> Tuple[int, Command]:
        maximumRate = 99
        minimumKey = ""
        tokenKey   = 0
        # 拼音取出
        for i, pinToken in enumerate(pinyinTokens):
            pinyinLength = len( pinToken )
            # 將每個指令取出
            for key in commandMap.keys():
                
                # 只判斷 ActionCommand
                if( isinstance(  commandMap[ key ], ActionCommand ) ):
                    # 取得指令拼音 (原本的詞拼音 + 同義字拼音)
                    for commandRoma in [ commandMap[ key ].getRomaPinyin() ] + commandMap[ key ].getSynonymRomas():
                        commandLength = len( commandRoma )
                        # 假如兩者字串長度差距過大就略過，以節省運算時間
                        if( abs( pinyinLength - commandLength ) > 5 or abs( pinyinLength * 2 - commandLength * 2 ) > 5 ):
                            continue
                        
                        distance = 0
                        if( pinyinLength < 5 or commandLength < 5 ):
                            distance = self._levenshteinDistance( pinToken + pinToken, commandRoma + commandRoma )
                        else:
                            distance = self._levenshteinDistance( pinToken, commandRoma )
                        print( "(拼音判斷) 字串A：{token}({roma}), 字串B:{key}({roma2}), 距離為：{distance}".format( token=originToken[i], roma=pinToken, key=key, roma2=commandRoma, distance=distance ) )
                        if( distance < maximumRate ):
                            maximumRate     = distance
                            minimumKey      = key
                            tokenKey        = i
            
        if( maximumRate >= 5 ):
            return (-1, None)
        else:
            return (i, commandMap[ minimumKey ])

    
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

                if str1[ i - 1 ] == str2[ j - 1 ]:
                    d = 0
                else:
                    if( (str1[ i - 1 ] in PinyionCondition.VOWEL) != (str2[ j - 2 ] in PinyionCondition.VOWEL)  ):
                        d = 2
                    else:
                        d = 1
                    
                matrix[i][j] = min( matrix[ i - 1 ][ j ] + 1, matrix[ i ][ j- 1 ] + 1, matrix[ i - 1 ][ j - 1 ] + d)
        return matrix[ len(str1) ][ len(str2) ]

    

    def getConditionName(self):
        return "拼音判斷"

# ==================================================================================================
class TranslateCondition( Condition ):
    TRANSLATOR = google_translator()  
    def __init__(self) -> None:
        pass

    def GenerateEnglishList( tokens: List[str] ) -> List[str]:
        engList:List[str]       = []
        for token in tokens:
            engList.append( TranslateCondition.TRANSLATOR.translate( token ).lower().replace(" ", "") )
        return engList

    def GenerateEnglish( token:str ):
        return TranslateCondition.TRANSLATOR.translate( token )

    def execute(self, commandMap: Dict[str, Command], originToken:List[str], engTokens: List[str]) -> Tuple[int, Command]:
        """經由 Google 翻譯去判斷兩者詞彙是否接近
        Args:
            commandMap (Dict[str, Command]): 指令表
            engTokens (List[str]): 英文字串 List
        Returns:
            Command: 指令
        """
        for i, engToken in enumerate( engTokens ):
            # 將每個指令取出
            for key in commandMap.keys():
                # 只判斷 ActionCommand
                if( isinstance(  commandMap[ key ], ActionCommand ) ):
                    # 取得指令拼音 (原本的詞拼音 + 同義字拼音)
                    for engCommand in commandMap[ key ].getEnglishName():

                        print( "(翻譯判斷) 字串A：{token}({eng}), 字串B:{key}({eng2})".format( token=originToken[i], eng=engToken, key=commandMap[ key ].getChineseName(), eng2=engCommand ) )
                        # 判斷是否英文字一樣
                        if( engCommand.lower().strip() == engToken ):
                            return (i, commandMap[ key ])
        return (-1, None)

    def getConditionName(self):
        return "翻譯判斷"