from typing         import List
import json.encoder
import threading    as THREAD   ## 多執行緒模組 ##
import os           as OS       ## 調用操作系統命令，來達成建立文件，刪除文件，查詢文件的模組 ##
import time         as TIME
import pprint       as PPRINT
import jieba_fast   as JIEBA
import keyboard     as KEYBOARD
import msvcrt       as MSVCRT
import sys          as SYS
## 語音轉文字模組 ##
import speech_recognition   as SPEECH_RECOGNIZE
from PyQt5                  import QtWidgets
from Util.command           import Command
from Util.condition         import Condition, NumberCondition, PinyionCondition, SimilarCondition, SimpleCondition, SynonymCondition, TranslateCondition
from Util.model             import Model  
from Interface.mainGame     import GameMainUi

class CommandActivater():
    def __init__(self, command:Command, executeTime=1) -> None:
        self._command       = command
        self._executeTime   = executeTime
        pass
    def command( self ) -> Command:
        return self._command
    def executeTime( self ) -> int:
        return self._executeTime
    def setTimes( self, times ):
        self._executeTime = times


class SpeechSensor():
    def __init__(self):
        pass
        

    def speechToText(self):

        recorder = SPEECH_RECOGNIZE.Recognizer()
        recorder.energy_threshold = 500

        with SPEECH_RECOGNIZE.Microphone() as source:
            print('請說話：')
            #r.adjust_for_ambient_noise(source, duration=0.5)
            recorder.dynamic_energy_threshold = True

            try:
                audio = recorder.listen( source, timeout=2, phrase_time_limit=2)
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


class SpeechRecognizeAgent(THREAD.Thread):
    def __init__(self) -> None:
        THREAD.Thread.__init__(self)
        self._working = True
        self._counter = 0

        self._model                         = Model()
        self._conditions:List[Condition]    = [NumberCondition(), SimpleCondition(), SynonymCondition(), SimilarCondition(), PinyionCondition(), TranslateCondition()]
        self._sensor                        = SpeechSensor()
        self._nowStatus                     = "隨時"
        
        # ------------- Jieba 載入自訂義詞庫 -------------
        JIEBA.set_dictionary( "resources/dict.txt.big" )
        JIEBA.load_userdict( "resources/customDict.txt" )
        for keyWord in self._model.getKeyWordSet():
            JIEBA.add_word( keyWord, Model.KEY_WORD_WEIGHT )


       # self.doAction()




    def run(self):
        # 判斷是否在工作
        while( self._working == True ):
            # 偵測是否結束
            if MSVCRT.kbhit() or KEYBOARD.is_pressed('q'):
                print("程式結束")
                return
            self.doAction()
            TIME.sleep(1)


    def doAction( self ):
        print( "目前狀態 -------------------------> " , self._nowStatus )
        # 取得語音指令
        textSpeech = "攻擊6次"
        if( textSpeech == None ):
            return
        print( "語音輸入：" + textSpeech )
     
        tokenTexts = JIEBA.lcut(textSpeech, cut_all=False, HMM=False)
        print( "結疤分詞：", str(tokenTexts) )

        # 移除停止詞
        self._model.removeStopWords( tokenTexts )

        print( "停止詞移除後：" + str(tokenTexts) )

        pinyinToken:List[str]   = PinyionCondition.GeneratePinyinList( tokenTexts )
        englishToken:List[str]  = TranslateCondition.GenerateEnglishList( tokenTexts )
        # 初始化 Command
        countable                               = False     # 可量化 Flag
        commandList: List[CommandActivater]     = []        # 指令串列
        tempActivator                           = None
        # ========================================================================================================
        for tokenIndex, token in enumerate(tokenTexts):
            command                                 = None      # 指令
            executeTime                             = 1         # 量詞
            # 每種判斷取出
            for condition in self._conditions:
                # 取出目前狀態可以判斷的指令
                statusCommand = self._model.getCommandsByStatus( self._nowStatus )
                if( statusCommand == None ):
                    print( "未知狀態" )
                    return
                # ------------------------------------------------------
                # 數字判斷
                if( isinstance(condition, NumberCondition) ):
                    if( countable == True ):
                        executeTime = condition.execute( token )
                # ------------------------------------------------------
                # 拼音判斷
                elif( isinstance(condition, PinyionCondition) ):
                    command = condition.execute( statusCommand, token,  pinyinToken[ tokenIndex ] )
                    # 加入至相似詞裡
                    if( command != None ):
                        command.addSimilarWord( token )
                        JIEBA.add_word( token, Model.KEY_WORD_WEIGHT )
                # ------------------------------------------------------
                # 翻譯判斷
                elif( isinstance(condition, TranslateCondition) ):
                    command = condition.execute( statusCommand, token,  englishToken[ tokenIndex ] )
                    # 加入至同義詞裡
                    if( command != None ):
                        command.addSynonymWord( token )
                        JIEBA.add_word( token, Model.KEY_WORD_WEIGHT )
                # ------------------------------------------------------
                # 其他
                else:
                    command = condition.execute( statusCommand,  token )
                # ------------------------------------------------------ 
                # 設定次數
                if( executeTime > 1 and tempActivator != None ):
                    tempActivator.setTimes( executeTime )
                    # tokenTexts.remove( token )              # 移除已經判斷過的字
                # 有找到指令
                elif( command != None ):
                    print( "搜尋結果： (" + condition.getConditionName() + ") 最相近的字串: ", command.getChineseName() )
                    tempActivator       = CommandActivater( command )           # 待執行指令暫存
                    commandList.append( tempActivator )                         # 待執行的指令串列
                    self._nowStatus     = command.nextStatus( self._nowStatus ) # 取出下個狀態
                    countable           = command.countable()                   # 判斷此指令是否可數
                     # tokenTexts.remove( token )                                  # 移除已經判斷過的字
                    break
        
        for cm in commandList:
            print( "指令：{command} 執行 {time} 次".format(command=cm.command().getChineseName(), time=cm.executeTime()) )


        # ========================================================================================================
        # countable                                   = False     # 可量化 Flag
        # parameterList: List[CommandActivater]       = []        # 指令串列
        # tempActivator                               = None
        # for tokenIndex, token in enumerate(tokenTexts):
        #     parameter                               = None
        #     executeTime                             = 1         # 量詞
        #     # 每種判斷取出
        #     for condition in self._conditions:
        #         # 取出目前狀態可以判斷的指令
        #         statusParameter = self._model.getParameterByStatus( self._nowStatus )
        #         if( statusParameter == None ):
        #             print( "未知狀態" )
        #             return
        #         # ------------------------------------------------------
        #         # 數字判斷
        #         if( isinstance(condition, NumberCondition) ):
        #             if( countable == True ):
        #                 executeTime = condition.execute( token )     
        #         # ------------------------------------------------------
        #         # 拼音判斷
        #         elif( isinstance(condition, PinyionCondition) ):
        #             parameter = condition.execute( statusParameter, token,  pinyinToken[ tokenIndex ] )
        #             # 加入至相似詞裡
        #             if( parameter != None ):
        #                 parameter.addSimilarWord( token )
        #                 JIEBA.add_word( token, Model.KEY_WORD_WEIGHT )
        #         # ------------------------------------------------------
        #         # 翻譯判斷
        #         elif( isinstance(condition, TranslateCondition) ):
        #             parameter = condition.execute( statusParameter, token,  englishToken[ tokenIndex ] )
        #             # 加入至同義詞裡
        #             if( parameter != None ):
        #                 parameter.addSynonymWord( token )
        #                 JIEBA.add_word( token, Model.KEY_WORD_WEIGHT )
        #         # ------------------------------------------------------
        #         # 其他
        #         else:
        #             parameter = condition.execute( statusParameter,  token )
        #         # ------------------------------------------------------ 
        #         # 設定次數
        #         if( executeTime > 1 and tempActivator != None ):
        #             tempActivator.setTimes( executeTime )
        #             # tokenTexts.remove( token )              # 移除已經判斷過的字
        #         # 有找到指令
        #         elif( parameter != None ):
        #             print( "搜尋結果： (" + condition.getConditionName() + ") 最相近的字串: ", parameter.getChineseName() )
        #             tempActivator       = CommandActivater( parameter )           # 待執行指令暫存
        #             parameterList.append( tempActivator )                         # 待執行的指令串列
        #             self._nowStatus     = parameter.nextStatus( self._nowStatus ) # 取出下個狀態
        #             countable           = parameter.countable()                   # 判斷此指令是否可數
        #              # tokenTexts.remove( token )                                  # 移除已經判斷過的字
        #             print( "目前狀態：" , self._nowStatus )
        #             break


        # for pm in parameterList:
        #     print( "參數：{command} 執行 {time} 次".format(command=pm.command().getChineseName(), time=pm.executeTime()) )
        # self._model.saveDataToFile()
        

if __name__ == "__main__":
    def run_app():

       # for synset in WORD_NET.synsets("car"):
       #     print(synset.definition())
        # Initial

        agent       = SpeechRecognizeAgent()
        agent.start()
        app         = QtWidgets.QApplication( SYS.argv )
        window      = GameMainUi()
        window.show()
        app.exec_()

    try:
        run_app()
    except Exception as e: 
        print("main crashed. Error: %s", e.with_traceback())


