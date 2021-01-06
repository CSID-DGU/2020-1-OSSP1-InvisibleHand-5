import create
import preprocess
import result
import analyze
import emotion_word
import noun_ex
import os
import math
import pandas as pd

pd.set_option('mode.chained_assignment', None)

# 파일 입력
storyName = input("소설명 : ")
book = create.open_book(storyName)

# 결과 출력 디렉토리 생성
create.create_folder(f'../res/output/{storyName}')

# 전처리
context = preprocess.remove_etc(book)

# 변수 선언
charOfPage = len(context) / 20
listOfEmotion = ['기쁨', '슬픔', '분노', '공포', '혐오', '놀람']
numOfEmotion = len(listOfEmotion)
numOfCharacter = int(input("등장인물 수 : "))

# 사용자 사전 생성
listOfCharacter = create.create_userdic(numOfCharacter)
print("사용자 사전 생성 완료")

# 문장 데이터프레임 생성
df_sentence = create.create_sentence_dataframe(context, listOfEmotion)

# 구축되어 있는 감정 사전 데이터 프레임 열기
df_emotion = emotion_word.open_emotion_dataframe()

# 문장 분석
df_sentence, numOfPage = analyze.analyze_sentence(df_sentence, listOfCharacter, df_emotion, charOfPage)
create.save_df(df_sentence, storyName, "문장")
print("문장 분석 및 데이터프레임 생성 완료")

# 등장인물 별 페이지 감정 점수 합산하여 등장인물 데이터프레임 생성
df_list_character = analyze.merge_character(storyName, df_sentence, listOfEmotion, listOfCharacter)
df_list_character_by_page = analyze.merge_character_page(storyName, df_sentence, numOfPage, listOfEmotion, listOfCharacter)
print("등장인물 데이터프레임 생성 완료")

# 그래프 설정
result.config_graph()

# 결과 1. 각 등장인물의 페이지별 감정 수준 그래프 생성 및 출력
result.display_emotion_graph(storyName, df_list_character, listOfCharacter, numOfCharacter, listOfEmotion)
print("문장 별 감정 그래프 생성 완료")

result.display_emotion_graph_page(storyName, df_list_character_by_page, listOfCharacter, numOfCharacter, listOfEmotion)
print("페이지 별 감정 그래프 생성 완료")

# 결과 2. 각 등장인물의 주요 감정
emo_list = result.display_main_emo(df_list_character_by_page, numOfCharacter, listOfEmotion)
for num in range(0, numOfCharacter):
    print(f'{listOfCharacter[num]}의 주요 감정 : {emo_list[num]}')

# 결과 3. 각 등장인물의 감정 비율
ratio_list = result.display_emo_ratio(df_sentence, listOfCharacter, listOfEmotion)
for num in range(0, numOfCharacter):
    print(f'{listOfCharacter[num]}의 감정 비율 : {ratio_list[num]}')

book.close()
