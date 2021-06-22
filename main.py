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
## 語音轉文字模組 ##
import speech_recognition   as SPEECH_RECOGNIZE
from Util.command           import Command
from Util.condition         import Condition, PinyionCondition, SimilarCondition, SimpleCondition, SynonymCondition
from Util.model             import Model   # 用來 Print 出好看得 Map
from Interface.mainGame     import GameMainUi


class FileConfig():
    CONFIG = None
    def __init__(self) -> None:
        pass

    def __init__() -> None:
        with open('dict/config.txt', 'r+') as file:
            FileConfig.CONFIG = eval( file.read() )  # 讀取的str轉換為字典
        pass

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
                return "無法辨識"
            except SPEECH_RECOGNIZE.WaitTimeoutError:
                print("超過時間")
                return "超過時間"

    
class SpeechRecognizeAgent():
    def __init__(self) -> None:
        self._model                         = Model()
        self._conditions:List[Condition]    = [SimpleCondition(), SynonymCondition(), SimilarCondition(), PinyionCondition()]
        self._sensor                        = SpeechSensor()
        self._status                        = "隨時"
        

    #    self.doAction()
    

    def doAction( self ):
        textSpeech = "張壹智要公雞"
        print( textSpeech )
    

        jiebaText = JIEBA.lcut(textSpeech, cut_all=False, HMM=True)
        print( "結疤分詞：", jiebaText )

        for condition in self._conditions:
            command = condition.execute( self._model.getCommandsByStatus( self._status ),  jiebaText )
            if( command != None ):
                print( "( " + condition.getConditionName() + " )最相近的字串: ", command.getChineseName() )
                break
    #    self._model.saveDataToFile()
        

if __name__ == "__main__":
    def run_app():
        app         = QtWidgets.QApplication( SYS.argv )
        agent       = SpeechRecognizeAgent()
        window      = GameMainUi()
        window.show()
        app.exec_()

    try:
        run_app()
    except Exception as e: 
        print("main crashed. Error: %s", e.with_traceback())


