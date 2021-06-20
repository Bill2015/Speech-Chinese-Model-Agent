

## 羅馬拼音模組 ##
from typing import Dict, List
from pypinyin import lazy_pinyin


# 指令類別，用來存放每一個指令的資訊
class Command():
    def __init__(self, data:dict ) -> None:
        self._jsonData          = data

        self._chineseName:str           = self._jsonData['名稱']
        self._englishName:str           = self._jsonData['英文名稱']
        self._similarWords:List[str]    = self._jsonData['相似詞']
        self._status:Dict[str, str]     = self._jsonData['狀態']
        self._romaPinyin:str            = "-".join( lazy_pinyin( self._chineseName ) )# 取得羅馬拼音
        # PPRINT.pprint( self._status )
        pass
    
    # 加入新的相似字
    def addSimilarWord( self, word:str ):
        """加入新的相似字

        Args:
            word (str): 欲加入的字
        """
        self._similarWords.append( word )

    # 取得中文名稱
    def getChineseName( self ) -> str:
        """取得指令中文名稱"""
        return self._chineseName

    # 取得英文名稱
    def getEnglishName( self ) -> str:
        """取得指令英文名稱"""
        return self._englishName
  
    # 取得相近詞
    def getSimilarNames( self ) -> List[str]:
        """取得指令英文名稱"""
        return self._similarWords

    # 取得羅馬拼音
    def getRomaPinyin( self ) -> str:
        """取得羅馬拼音"""
        return self._romaPinyin

    # 取得狀態表
    def getStatus( self ) -> Dict[str, str]:
        """取得狀態表"""
        return self._status