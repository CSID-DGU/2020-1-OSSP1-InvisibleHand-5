import numpy as np
import pandas as pd
import re


# 소설 입력
def open_book(fileName):
    fileName = fileName + ".txt"
    book = open(f'../res/book/{fileName}', "rt", encoding='UTF8', errors='ignore')
    return book


# 사용자 입력받아서 사전에 등장인물 고유명사로 추가
def create_userdic(numOfCharacter, listOfCharacter):
    userdic = open("user_dic.txt", "wt", encoding='UTF8') # userdic 저장 경로 변경
    for n in range(0, numOfCharacter):
        #name = input(f"등장인물 {n + 1} : ")
        name = "김첨지"# 테스트용 #########나중에 수정######################
        userdic.write(f"{name}\tNNP\n")
        listOfCharacter.append(name)
    userdic.close()


# 문장 리스트 생성
def create_sentence_list(context):
    conversation = False
    conversation_end = False
    sentence = []
    punctuation = []
    kind = []
    connect = []
    buffer = ""

    for char in context:
        buffer = buffer + char
        if char == '\"':
            if conversation:  # 닫는 따옴표 -> 대화문
                sentence.append(buffer)
                punctuation.append(buffer[-2])
                kind.append("대화문")
                conversation_end = True
                buffer = ""
            conversation = not conversation
        elif (char == '.' or char == '?' or char == '!') and (not conversation):  # 따옴표 밖의 구두 문자 -> 서술문
            sentence.append(buffer)
            punctuation.append(char)
            kind.append("서술문")
            connect.append("")
            buffer = ""
        elif conversation_end:  # 대화문 다음 글자가
            if char == " ":  # 공백이라면 미연결
                connect.append("미연결")
            else:
                connect.append("연결")  # 글자라면 연결
            conversation_end = False
    connect.append("")
    return sentence, punctuation, kind, connect


# 문장 데이터프레임 생성 [문장, 구두문자, 문장 종류, 연결 여부, 주어, 목적어, 감정 별 점수]
def create_sentence_dataframe(context, listOfEmotion):
    sentence, punctuation, kind, connect = create_sentence_list(context)
    df = pd.DataFrame(sentence, columns=['문장'])
    df['페이지 번호'] = 0
    df['구두 문자'] = pd.Series(punctuation, index=df.index)
    df['문장 종류'] = pd.Series(kind, index=df.index)
    df['연결 여부'] = pd.Series(connect, index=df.index)
    df['주어'] = ""
    df['목적어'] = ""
    df['감정 단어'] = ""
    df['화자'] = ""
    for emo in listOfEmotion:
        df[f'{emo}'] = 0.0
    return df


# 등장인물 데이터프레임 생성
def create_character_dataframe(numOfPage, listOfCharacter, listOfEmotion):
    writer = pd.ExcelWriter("../res/output/등장인물.xlsx")
    df_list = []
    for character in listOfCharacter:
        df = pd.DataFrame(index=range(0, numOfPage), columns=[f"{emotion}" for emotion in listOfEmotion])
        df_list.append(df)
        df.to_excel(writer, sheet_name=f"{character}")
    writer.save()
    return df_list


# <결과 1. 각 등장인물의 페이지별 각 감정 수준> 을 표현할
# [등장인물][감정][페이지] 구조의 3차원 벡터 생성
def create_emotion_vector(numOfCharacter, numOfEmotion, numOfPage):
    vector = np.zeros(numOfCharacter * numOfEmotion * numOfPage, dtype=np.float_)
    emotion_vector = vector.reshape(numOfCharacter, numOfEmotion, numOfPage)
    return emotion_vector


# <결과 2. 모든 등장인물의 페이지별 감정 흐름>을 표현할
# [등장인물][페이지] 구조의 2차원 벡터 생성
def create_sentiment_vector(numOfCharacter, numOfEmotion, numOfPage):
    vector = np.zeros(numOfCharacter * numOfPage, dtype=np.float_)
    sentiment_vector = vector.reshape(numOfCharacter, numOfPage)
    return sentiment_vector


# 감정 사전 생성
def create_emotion_dictionary():
    lex_file = open('../res/dic/Korean_Lexicon.txt', 'rt', encoding='UTF8')
    lex_file.seek(0)
    stab = re.compile("[^\t]+")

    sentiments = ['분노', '기대', '혐오', '공포', '기쁨', '슬픔', '놀람', '신뢰']
    anger = {}
    anticipation = {}
    disgust = {}
    fear = {}
    joy = {}
    sadness = {}
    surprise = {}
    trust = {}
    emotion_dictionary_lists = [joy, sadness, anger, fear, disgust, surprise]

    line_data = lex_file.readline()
    line_data = lex_file.readline()

    while line_data:
        key = stab.findall(line_data)[1]  # 단어 (키값)
        if stab.findall(line_data)[2] == "anger": # 감정의 종류 (ex. anger, joy)
            val1 = "분노"
        if stab.findall(line_data)[2] == "anticipation": # 감정의 종류 (ex. anger, joy)
            val1 = "기대"
        if stab.findall(line_data)[2] == "disgust": # 감정의 종류 (ex. anger, joy)
            val1 = "혐오"
        if stab.findall(line_data)[2] == "fear": # 감정의 종류 (ex. anger, joy)
            val1 = "공포"
        if stab.findall(line_data)[2] == "joy": # 감정의 종류 (ex. anger, joy)
            val1 = "기쁨"
        if stab.findall(line_data)[2] == "sadness": # 감정의 종류 (ex. anger, joy)
            val1 = "슬픔"
        if stab.findall(line_data)[2] == "surprise": # 감정의 종류 (ex. anger, joy)
            val1 = "놀람"
        if stab.findall(line_data)[2] == "trust": # 감정의 종류 (ex. anger, joy)
            val1 = "신뢰"
        val2 = stab.findall(line_data)[3].replace("\n", "")  # 감정의 정도

        if val1 == sentiments[0]:
            anger[key] = [val1, val2]
            line_data = lex_file.readline()
        elif val1 == sentiments[1]:
            anticipation[key] = [val1, val2]
            line_data = lex_file.readline()
        elif val1 == sentiments[2]:
            disgust[key] = [val1, val2]
            line_data = lex_file.readline()
        elif val1 == sentiments[3]:
            fear[key] = [val1, val2]
            line_data = lex_file.readline()
        elif val1 == sentiments[4]:
            joy[key] = [val1, val2]
            line_data = lex_file.readline()
        elif val1 == sentiments[5]:
            sadness[key] = [val1, val2]
            line_data = lex_file.readline()
        elif val1 == sentiments[6]:
            surprise[key] = [val1, val2]
            line_data = lex_file.readline()
        elif val1 == sentiments[7]:
            trust[key] = [val1, val2]
            line_data = lex_file.readline()
        else:
            print('끝')

    lex_file.close()

    return emotion_dictionary_lists


def save_df(df, fileName):
    df.to_excel(f"../res/output/{fileName}.xlsx")
