

## 羅馬拼音模組 ##
from pprint import pprint
from typing import Dict, List, Set
from pypinyin import lazy_pinyin
from google_trans_new       import google_translator  

# ======================================================================
# 指令
class Command():
    TRANSLATOR = google_translator()  

    def __init___(self, data:dict, name:str, countable:bool, status:Dict[str, str] ) -> None:
        self._jsonData                  = data
        self._chineseName:str           = name
        self._englishName:Set[str]      = set()
        self._countable:bool            = countable
        self._status:Dict[str, str]     = status
        self._romaPinyin:str            = "-".join( lazy_pinyin( self._chineseName ) )# 取得羅馬拼音
        
        self._synonymDicts:dict         = self._jsonData['同義詞']
        self._similarWords:List[str]    = self._jsonData['相似詞']
        self._synonymWords:List[str]    = []
        self._synonymRomas:List[str]   = []

    def __init__(self,  data:dict ) -> None:
        self._jsonData                  = data
        self._chineseName:str           = self._jsonData['名稱']
        self._englishName:Set[str]      = set()
        self._countable:bool            = self._jsonData['可量化']
        self._status:Dict[str, str]     = self._jsonData['狀態']
        self._romaPinyin:str            = "-".join( lazy_pinyin( self._chineseName ) )# 取得羅馬拼音

        self._synonymDicts:dict         = self._jsonData['同義詞']
        self._similarWords:List[str]    = self._jsonData['相似詞']
        self._synonymWords:List[str]    = []
        self._synonymRomas:List[str]    = []
        pass
    
    # 取得中文名稱
    def getChineseName( self ) -> str:
        """取得指令中文名稱"""
        return self._chineseName

    # 取得英文名稱
    def getEnglishName( self ) -> Set[str]:
        """取得指令英文名稱"""
        return self._englishName

    # 取得狀態表
    def getStatus( self ) -> Dict[str, str]:
        """取得狀態表"""
        return self._status

    # 可數的，代表指令可以加數字，以執行多次
    def countable( self ) -> bool:
        """可數的，代表指令可以加數字，以執行多次"""
        return self._countable

    # 取得羅馬拼音
    def getRomaPinyin( self ) -> str:
        """取得羅馬拼音"""
        return self._romaPinyin

         # 加入新的相似字
    def addSimilarWord( self, word:str ):
        """加入新的相似字

        Args:
            word (str): 欲加入的字
        """
        self._similarWords.append( word )

    # 加入新的同義字
    def addSynonymWord( self, word:str ):
        """加入新的相似字
        Args:
            word (str): 欲加入的字
        """
        translateWord = Command.TRANSLATOR.translate( word ).lower().strip()    # 進行翻譯
        self._synonymDicts[ word ] = translateWord
        self._englishName.add( translateWord )

    # 取得同義詞的羅馬拼音
    def getSynonymRomas( self ) -> List[str]:
        """取得指令取得同義詞的羅馬拼音"""
        return self._synonymRomas     

    # 取得同義詞
    def getSynonymNames( self ) -> List[str]:
        """取得指令取得同義詞"""
        return self._synonymWords

    # 取得英文名稱
    def getEnglishName( self ) -> Set[str]:
        """取得指令英文名稱"""
        return self._englishName
    
    # 取得相近詞
    def getSimilarNames( self ) -> List[str]:
        """取得指令英文名稱"""
        return self._similarWords

    def getSynonymDicts( self ) -> dict:
        return self._synonymDicts


# ======================================================================
# 指令類別，用來存放每一個指令的資訊
class ActionCommand(Command):
    def __init__(self, data:dict ) -> None:
        Command.__init__( self, data )
   

        # PPRINT.pprint( self._status )
        # 新增原有的中文翻譯字
        if( self._chineseName not in self._synonymDicts.keys() ):
            translateWord = Command.TRANSLATOR.translate( self._chineseName ).lower().strip()
            self._synonymDicts[ self._chineseName ] = translateWord

        # 取出每個同義字
        for synKey in self._synonymDicts.keys():
            self._synonymWords.append( synKey )
            # 判斷是否還未幫同義字翻譯
            if( self._synonymDicts[ synKey ] == "" ):
                translateWord = Command.TRANSLATOR.translate( synKey ).lower().strip()    # 進行翻譯
                self._synonymDicts[ synKey ] = translateWord
                self._englishName.add( translateWord )
            # 已經有翻譯了
            else:
                self._englishName.add( self._synonymDicts[ synKey ] )

        self._synonymRomas:List[str]    = [ "-".join( lazy_pinyin( word ) ) for word in self._synonymWords ]
        pass
    



# ======================================================================
class ActionParameter(Command):
    
    def __init__(self, jsonData:dict, belongName:str, name:str, countable:bool, status:Dict[str, str]) -> None:
        Command.__init___( self, jsonData, name, countable, status )
        self._belongName:str                = belongName

        # PPRINT.pprint( self._status )
        # 新增原有的中文翻譯字
        if( name not in self._synonymDicts.keys() ):
            translateWord = Command.TRANSLATOR.translate( name ).lower().strip()
            self._synonymDicts[ name ] = translateWord
        
        # 取出每個同義字
        for synKey in self._synonymDicts.keys():
            self._synonymWords.append( synKey )
            # 判斷是否還未幫同義字翻譯
            if( self._synonymDicts[ synKey ] == "" ):
                translateWord = Command.TRANSLATOR.translate( synKey ).lower().strip()    # 進行翻譯
                self._synonymDicts[ synKey ] = translateWord
                self._englishName.add( translateWord )
            # 已經有翻譯了
            else:
                self._englishName.add( self._synonymDicts[ synKey ] )
        
        self._synonymRomas:List[str]    = [ "-".join( lazy_pinyin( word ) ) for word in self._synonymWords ]

   
    def getBelong( self ) -> str:
        return self._belongName
