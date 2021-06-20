## 羅馬拼音模組 ##
from pypinyin import lazy_pinyin

## 中翻英函式 ##
romma = lazy_pinyin("你好")
print( romma )

print ('hello world')

# =============================
import jieba_fast as jieba
text = '韓國瑜來到北京清華大學'
print('預設:', '|'.join(jieba.cut(text, cut_all=True, HMM=True)))

