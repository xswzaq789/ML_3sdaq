import re
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd

#pip install JPype1-1.3.0-cp39-cp39-win_amd64.whl
from konlpy.tag import Okt
print("###### X_train")
X_train = pd.read_csv('X_train.csv')
print(X_train.shape)
print(type(X_train))

print("###### X_train2")
X_train2 = X_train["tokenized"].squeeze()
print(type(X_train2))
print(X_train2.shape)

print("###### X_train3")
X_train3 = X_train2.values
print(X_train3[0])
print(type(X_train3[0]))
print(X_train3.shape)

print("###### X_train4")
X_train4 = []
print("#### Split 시작")
for str in X_train3:
    str = str.replace("[", "").replace("]", "").replace(" '", "").replace("'", "")
    X_train4.append(str.split(","))
print("#### Split 끝")
print(X_train4[0])
print(type(X_train4[0]))


X_train = X_train4.copy()
print("###### X_train")
print(X_train[0])

stopwords = ['도', '는', '다', '의', '가', '이', '은', '한', '에', '하', '고', '을', '를', '인', '듯', '과', '와', '네', '들', '듯', '지', '임', '게']

loaded_model = load_model('best_model.h5')
# 정수 인코딩
tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_train)

threshold = 2
total_cnt = len(tokenizer.word_index) # 단어의 수
rare_cnt = 0 # 등장 빈도수가 threshold보다 작은 단어의 개수를 카운트
total_freq = 0 # 훈련 데이터의 전체 단어 빈도수 총 합
rare_freq = 0 # 등장 빈도수가 threshold보다 작은 단어의 등장 빈도수의 총 합

# 단어와 빈도수의 쌍(pair)을 key와 value로 받는다.
for key, value in tokenizer.word_counts.items():
    total_freq = total_freq + value

    # 단어의 등장 빈도수가 threshold보다 작으면
    if(value < threshold):
        rare_cnt = rare_cnt + 1
        rare_freq = rare_freq + value

print('단어 집합(vocabulary)의 크기 :',total_cnt)
print('등장 빈도가 %s번 이하인 희귀 단어의 수: %s'%(threshold - 1, rare_cnt))
print("단어 집합에서 희귀 단어의 비율:", (rare_cnt / total_cnt)*100)
print("전체 등장 빈도에서 희귀 단어 등장 빈도 비율:", (rare_freq / total_freq)*100)

# 전체 단어 개수 중 빈도수 2이하인 단어 개수는 제거.
# 0번 패딩 토큰과 1번 OOV 토큰을 고려하여 +2
vocab_size = total_cnt - rare_cnt + 2
print('단어 집합의 크기 :',vocab_size)

## 재 토큰화
tokenizer = Tokenizer(vocab_size, oov_token = 'OOV')
tokenizer.fit_on_texts(X_train)
X_train = tokenizer.texts_to_sequences(X_train)
print("###### X_train tokenizer.texts_to_sequences(X_train) 후")
print(X_train[0])

X_train = pad_sequences(X_train, maxlen=80)
print("###### X_train pad_sequences(X_train, maxlen=80) 후")
print(X_train[0])
okt =  Okt()
def sentiment_predict(new_sentence):
    print('new_sentence1 : ', new_sentence)
    new_sentence = re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣 ]', '', new_sentence)
    print('new_sentence2: ', new_sentence)
    new_sentence = okt.morphs(new_sentence)
    print('new_sentence3 : ', new_sentence)
    new_sentence = [word for word in new_sentence if not word in stopwords]
    print('new_sentence4 : ', new_sentence)
    encoded = tokenizer.texts_to_sequences([new_sentence])
    print('encoded : ', encoded)
    pad_new = pad_sequences(encoded, maxlen=80)
    print('pad_new : ', pad_new)

    score = float(loaded_model.predict(pad_new))
    print('score : ', score)
    if (score > 0.5):
        print("{:.2f}% 확률로 긍정 리뷰입니다.".format(score * 100))
    else:
        print("{:.2f}% 확률로 부정 리뷰입니다.".format((1 - score) * 100))


sentiment_predict("굿굿 2조쇼핑몰 강추")
sentiment_predict("2조에서 만들었다고했는데 다른데서 만듬 사기꾼인가")
sentiment_predict("돈만은게 샀지요")
