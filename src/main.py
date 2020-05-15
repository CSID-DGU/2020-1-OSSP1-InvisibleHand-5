import create
import preprocess
import result
import analyze
import math
import pandas as pd
from matplotlib import pyplot as plt

# 파일 입력
fileName = input("소설명 : ")
book = create.open_book(fileName)

# 전처리
context = preprocess.remove_etc(book)

# 문장 테이블 생성
df = create.create_sentence_table(context)
create.save_df(df, fileName)

# 변수 선언
charOfPage = 700
listOfEmotion = ['기쁨', '슬픔', '분노', '공포', '혐오', '놀람']
numOfEmotion = len(listOfEmotion)
numOfPage = math.ceil(len(context) / charOfPage)
numOfCharacter = int(input("등장인물 수 : "))
listOfCharacter = []

# 사용자 사전 생성
create.create_userdic(numOfCharacter, listOfCharacter)

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
