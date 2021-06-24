from typing         import List
from PyQt5          import QtWidgets
import socket       as SOCKET   ## socket連線模組 ##

import json.encoder
import threading    as THREAD   ## 多執行緒模組 ##
import os           as OS       ## 調用操作系統命令，來達成建立文件，刪除文件，查詢文件的模組 ##
import sys          as SYS
import time         as TIME
import pprint       as PPRINT
import jieba_fast   as JIEBA
from pypinyin.core  import lazy_pinyin
## 語音轉文字模組 ##
import speech_recognition   as SPEECH_RECOGNIZE
from Util.command           import ActionCommand, ActionParameter, Command
from Util.condition         import Condition, PinyionCondition, SimilarCondition, SimpleCondition, SynonymCondition, TranslateCondition
from Util.model             import Model  
from Interface.mainGame     import GameMainUi
from google_trans_new       import google_translator  

class SpeechSensor():
    def __init__(self) -> None:
        pass

    def speechToText(self):

        recorder = SPEECH_RECOGNIZE.Recognizer()
        recorder.energy_threshold = 2200

        with SPEECH_RECOGNIZE.Microphone() as source:
            print('請說話：')
            #r.adjust_for_ambient_noise(source, duration=0.5)
            recorder.dynamic_energy_threshold = False

            try:
                audio = recorder.listen( source, timeout=1, phrase_time_limit=2)
                #audio = r.listen(source)
                text = recorder.recognize_google(audio, language='zh-tw')
                flag = 0
                temp = ''

                """for i in range(len(text)):
                    if(i >= 1):
                        if(is_number(text[i]) and not(is_number(text[i-1])) and text[i-1] != ' ' and flag == 0):
                            temp += ' '
                            flag = 1
                    temp += text[i]"""

                # print("Transcription:"+temp)
                return text
            except SPEECH_RECOGNIZE.UnknownValueError:
                print("無法辨識")
                return None
            except SPEECH_RECOGNIZE.WaitTimeoutError:
                print("超過時間")
                return None

    
class SpeechRecognizeAgent():
    def __init__(self) -> None:
        self._model                         = Model()
        self._conditions:List[Condition]    = [SimpleCondition(), SynonymCondition(), SimilarCondition(), PinyionCondition(), TranslateCondition()]
        self._sensor                        = SpeechSensor()
        self._status                        = "隨時"
        

        
        self.doAction()


    def doAction( self ):
        pinyinToken:List[str]   = None
        englishToken:List[str]  = None

        textSpeech = self._sensor.speechToText()
        if( textSpeech == None ):
            return
        print( "語音輸入：" + textSpeech )
    
        # 載入自訂義詞庫
        JIEBA.set_dictionary( "resources/dict.txt.big" )
        JIEBA.load_userdict( "resources/customDict.txt" )
        tokenTexts = JIEBA.lcut(textSpeech, cut_all=False, HMM=False)
        print( "結疤分詞：", str(tokenTexts) )

        # 移除停止詞
        for token in tokenTexts:
            if( token in self._model.getStopwordSet() ):
                tokenTexts.remove( token )

        print( "停止詞移除後：" + str(tokenTexts) )
        # 初始化 Command
        command     = None
        parameter   = None
        # # ========================================================================================================
        # 每種判斷取出
        for condition in self._conditions:
            # ------------------------------------------------------
            # 拼音判斷
            if( isinstance(condition, PinyionCondition) ):
                pinyinToken = PinyionCondition.GeneratePinyinList( tokenTexts )
                index, command = condition.execute( self._model.getCommandsByStatus( self._status ), tokenTexts,  pinyinToken )
                # 加入至相似詞裡
                if( isinstance( command, ActionCommand ) ):
                    command.addSimilarWord( tokenTexts[index] )
            # ------------------------------------------------------
            # 翻譯判斷
            elif( isinstance(condition, TranslateCondition) ):
                englishToken = TranslateCondition.GenerateEnglishList( tokenTexts )
                index, command = condition.execute( self._model.getCommandsByStatus( self._status ), tokenTexts,  englishToken )
                # 加入至同義詞裡
                if( isinstance( command, ActionCommand ) ):
                    command.addSynonymWord( tokenTexts[index] )
            # ------------------------------------------------------
            # 其他
            else:
                _, command = condition.execute( self._model.getCommandsByStatus( self._status ),  tokenTexts )
            # ------------------------------------------------------   
            # 有找到指令
            if( command != None ):
                print( "搜尋結果： (" + condition.getConditionName() + ") 最相近的字串: ", command.getChineseName() )
                break
        
        # ========================================================================================================
        # 參數判斷
        # for condition in self._conditions:
        #     # ------------------------------------------------------
        #     # 拼音判斷
        #     if( isinstance(condition, PinyionCondition) ):
        #         # 確保已經產生 Pinyin 串列
        #         if( pinyinToken == None ):
        #             pinyinToken = PinyionCondition.GeneratePinyinList( tokenTexts )

        #         index, parameter = condition.execute( self._model.getParameterByStatus( self._status ), tokenTexts,  pinyinToken )
        #         # 加入至相似詞裡
        #         if( parameter != None ):
        #             parameter.addSimilarWord( tokenTexts[index] )
        #     # ------------------------------------------------------
        #     # 翻譯判斷
        #     elif( isinstance(condition, TranslateCondition) ):
        #         # 確保已經產生 Translate 串列
        #         if( englishToken == None ):
        #             englishToken = TranslateCondition.GenerateEnglishList( tokenTexts )
                
        #         index, parameter = condition.execute( self._model.getParameterByStatus( self._status ), tokenTexts,  englishToken )
        #         # 加入至同義詞裡
        #         if( parameter != None ):
        #             parameter.addSynonymWord( tokenTexts[index] )
        #     # ------------------------------------------------------
        #     # 其他
        #     else:
        #         _, parameter = condition.execute( self._model.getParameterByStatus( self._status ),  tokenTexts )
        #     # ------------------------------------------------------   
        #     # 有找到指令
        #     if( parameter != None ):
        #         print( "搜尋結果： (" + condition.getConditionName() + ") 最相近的字串: ", parameter.getChineseName() )
        #         break

        self._model.saveDataToFile()
        

if __name__ == "__main__":
    def run_app():

       # for synset in WORD_NET.synsets("car"):
       #     print(synset.definition())
        # Initial

        agent       = SpeechRecognizeAgent()
      #  app         = QtWidgets.QApplication( SYS.argv )
      #  window      = GameMainUi()
      #  window.show()
      #  app.exec_()

    try:
        run_app()
    except Exception as e: 
        print("main crashed. Error: %s", e.with_traceback())


