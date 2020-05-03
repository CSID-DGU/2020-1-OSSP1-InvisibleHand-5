import create
import preprocess
import result
import analyze
import math
import pandas as pd
import morphs
from matplotlib import pyplot as plt

# 파일 입력
fileName = input("소설명 : ")
book = create.open_book(fileName)

# 전처리
context = preprocess.remove_etc(book)

# 변수 선언
charOfPage = 700
listOfEmotion = ['기쁨', '슬픔', '분노', '공포', '혐오', '놀람']
numOfEmotion = len(listOfEmotion)
numOfPage = math.ceil(len(context) / charOfPage)
numOfCharacter = int(input("등장인물 수 : "))
listOfCharacter = []

# 문장 테이블 생성
df = create.create_sentence_table(context, listOfEmotion)
create.save_df(df, fileName)

# 사용자 사전 생성
create.create_userdic(numOfCharacter, listOfCharacter)

# 화자 분석
morphs.analyze_speaker(df, listOfCharacter)

# 감정 사전 생성
emotion_dictionary_lists = create.create_emotion_dictionary()

# 감정 벡터, 긍부정 벡터 생성
emotionVector = create.create_emotion_vector(numOfCharacter, numOfEmotion, numOfPage)
sentimentVector = create.create_sentiment_vector(numOfCharacter, numOfEmotion, numOfPage)

# 값 입력
analyzedEmotionVector = analyze.analyze_text(numOfPage, charOfPage, emotion_dictionary_lists, emotionVector,
                                             listOfCharacter)

# 그래프 설정
result.config_graph()

# 결과 1. 각 등장인물의 페이지별 감정 수준 그래프 생성 및 출력
result.display_emotion_graph(numOfCharacter, listOfCharacter, numOfPage, numOfEmotion, listOfEmotion,
                             analyzedEmotionVector)

# 결과 2. 모든 등장인물의 페이지별 감정 흐름 그래프 생성 및 출력
result.display_sentiment_graph(numOfCharacter, listOfCharacter, numOfPage, sentimentVector)

plt.show()
book.close()

# 전처리 모듈
import preprocessing
# 형태소 분석 모듈
# import module.morphs
# 구문 분석 모듈
# import module.syntax
from konlpy.tag import Komoran
from matplotlib import pyplot as plt
import numpy as np

numOfPage = 200
numOfEmotion = 6

# ---------- 1. 입력 데이터 설정 ----------
# 파일 입력
fileName = input() + ".txt"
book = open(f'../res/book/{fileName}', "rt", encoding='UTF8')
userDic = open("../user_dic.txt", "wt", encoding='UTF8')

# 감정을 추출할 등장인물 수
numOfCharacter = int(input())
listOfCharacter = []

# [등장인물][페이지][감정] 구조의 3차원 벡터 생성
v = np.empty(numOfCharacter * numOfPage * numOfEmotion)
vector = v.reshape(numOfCharacter, numOfPage, numOfEmotion)

# 사용자 사전에 등장인물 고유명사로 추가
for n in range(0, numOfCharacter):
    name = input()
    userDic.write(f"{name} nnp\n")
    listOfCharacter.append(name)


userDic.close()

# ---------- 2. 전처리 ----------
# 개행 문자 제거 , 꺽쇠 -> 따옴표 변환 ,
context = preprocessing.del_new_lines(book)

# 단위  1p? = 전체 글자수 / 200
unit = int(len(context) / numOfPage)

# ---------- 3. 감정 추출 ----------

# ---------- 4. 감정 분석 ----------

# ---------- 5. 결과 추출 ----------

x = np.arange(1, numOfPage)
y = x * 5

plt.plot(x, y)
plt.show()

book.close()
