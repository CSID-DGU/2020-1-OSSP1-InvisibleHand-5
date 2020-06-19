import create
import preprocess
import result
import analyze
import morphs
import emotion_word
import math
import pandas as pd
import noun_ex

pd.set_option('mode.chained_assignment', None)

# 파일 입력
# fileName = input("소설명 : ")
fileName = "운수좋은날"  # 테스트용 #########나중에 수정######################
book = create.open_book(fileName)

# 전처리
context = preprocess.remove_etc(book)

# 변수 선언
# charOfPage = 700
charOfPage = len(context) / 20
listOfEmotion = ['기쁨', '슬픔', '분노', '공포', '혐오', '놀람']
numOfEmotion = len(listOfEmotion)
numOfPage = math.ceil(len(context) / charOfPage)
# numOfCharacter = int(input("등장인물 수 : "))
numOfCharacter = 1  # 테스트용 #########나중에 수정######################
listOfCharacter = []

# 사용자 사전 생성
create.create_userdic(numOfCharacter, listOfCharacter)

# 문장 테이블 생성
df = create.create_sentence_dataframe(context, listOfEmotion)
create.save_df(df, fileName)

# 명사 추출
# noun_ex.noun_extract(df)

# emotion_word.emotion_lemmatization()

# 문장 데이터프레임 생성
df_sentence = create.create_sentence_dataframe(context, listOfEmotion)

# 감정 사전 생성
emotion_dictionary_lists = emotion_word.create_emotion_dictionary()

# 구축되어 있는 감정 사전 데이터 프레임 오픈
df_emotion = emotion_word.open_emotion_dataframe()

# 문장 분석
df_sentence = analyze.analyze_sentence(df_sentence, listOfCharacter, df_emotion, charOfPage)
create.save_df(df_sentence, fileName)

# 등장인물 별 페이지 감정 점수 합산하여 등장인물 데이터프레임 생성
df_list_character = analyze.merge_character(df_sentence, listOfEmotion, listOfCharacter)
df_list_character_by_page = analyze.merge_character_page(df_sentence, numOfPage, listOfEmotion, listOfCharacter)

# 20 문장 당 x축 사이즈 = 1
# 그래프 설정
x_size = len(df_sentence.index) / 20 + 1
result.config_graph(x_size)

# 결과 1. 각 등장인물의 페이지별 감정 수준 그래프 생성 및 출력
result.display_emotion_graph(df_list_character, df_list_character_by_page, listOfCharacter, numOfCharacter,
                             listOfEmotion)

# 결과 3. 각 등장인물의 주요 감정
emo_list = result.display_main_emo(df_list_character_by_page, numOfCharacter, listOfEmotion)
for emo in emo_list:
    print(emo)

# 결과 4. 각 등장인물의 감정 비율
ratio_list = result.display_emo_ratio(df_sentence, listOfCharacter, numOfCharacter, listOfEmotion)
for num in range(0, numOfCharacter):
    print(f'{listOfCharacter[num]}의 감정 비율 : {ratio_list[num]}')
book.close()
