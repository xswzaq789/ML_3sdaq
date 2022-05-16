import re
import pandas as pd
import numpy as np
from collections import Counter

from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, Dense, GRU
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
import pkg_resources
import os
import subprocess
import platform
print("platform.system() : ", platform.system())
if(platform.system() == "Linux"):
  print("konlpy install..........!!!")
  os.system("pip install konlpy")
#pip install konlpy
#pip install JPype1-1.3.0-cp39-cp39-win_amd64.whl
from konlpy.tag import Okt
# 형태소 처리 라이브러리 정의
okt =  Okt()
# 불용어 : 추가시 리스트에 추가
stopwords = ['도', '는', '다', '의', '가', '이', '은', '한', '에', '하', '고', '을', '를', '인', '듯', '과', '와', '네', '들', '듯', '지', '임', '게']

# 기존 X_train csv 파일 전환 후 로드시 X_train.csv 파일로 틀어짐 전처리
print("getcwd : ", os.getcwd())
print("__name__ : ", __name__)
print("file 위치 : ", os.path.dirname(__file__))
stream = pkg_resources.resource_stream(__name__, 'X_train.csv')
X_train = pd.read_csv(stream)
X_train = X_train.drop('Unnamed: 0' , axis=1)
X_train2 = X_train["tokenized"].squeeze()
X_train3 = X_train2.values
X_train4 = []
for str in X_train3:
    str = str.replace("[", "").replace("]", "").replace(" '", "").replace("'", "")
    X_train4.append(str.split(","))
X_train = X_train4.copy()

tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_train)

## 재 토큰화  # vocab_szie 1756
tokenizer = Tokenizer(1756, oov_token = 'OOV')
tokenizer.fit_on_texts(X_train)
X_train = tokenizer.texts_to_sequences(X_train)

# 리뷰길이 25으로 패딩 , max_len = 25 확인
X_train = pad_sequences(X_train, maxlen=25)

# 모델로드
#loaded_model = load_model('ml_model.h5')
model_dir = os.path.join(os.path.dirname(__file__), "ml_model.h5")
loaded_model = load_model(model_dir)

## 리뷰예측하기
def sentiment_predict(new_sentence):
  keep_sentence = new_sentence
  new_sentence = new_sentence.replace("↑", "상승").replace("↓", "하락")
  new_sentence = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]','', new_sentence)
  new_sentence = okt.morphs(new_sentence)
  new_sentence = [word for word in new_sentence if not word in stopwords]
  encoded = tokenizer.texts_to_sequences([new_sentence])
  pad_new = pad_sequences(encoded, maxlen = 25)

  score = float(loaded_model.predict(pad_new))
  if(score > 0.5):
    print(keep_sentence, " {:.2f}% 확률로 긍정 리뷰입니다.".format(score * 100))
  else:
    print(keep_sentence, " {:.2f}% 확률로 부정 리뷰입니다.".format((1 - score) * 100))
  return score

