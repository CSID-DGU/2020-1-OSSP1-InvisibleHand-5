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
    userdic = open("../user_dic.txt", "wt", encoding='UTF8')
    for n in range(0, numOfCharacter):
        name = input(f"등장인물 {n + 1} : ")
        userdic.write(f"{name}\tNNP\n")
        listOfCharacter.append(name)

    userdic.close()


# 문장 테이블 생성 [문장, 마치는 글자, 대화 여부, 다음 문장과 연결 여부]
# 현재 한 줄 밀리는 버그 있음
def create_sentence_table(context):
    isConversation = False
    sentence_table = {}
    isCon = []
    isNext = []
    buffer = ""
    for char in context:
        buffer = buffer + char
        if char == '\"':
            isConversation = not isConversation
            if not isConversation:  # 닫는 따옴표 -> 대화 여부 True
                sentence_table[buffer] = buffer[-2]
                isCon.append("대화문")
                if context[context.index(char) + 1] != " ":  # 다음 문장이 띄어져있지않다면
                    isNext.append("연결")  # 다음 문장 연결 여부 True
                    buffer = ""
                else:  # 다음 문장이
                    isNext.append("미연결")  # 다음 문장 연결 여부 False
                    buffer = ""
        elif (char == '.' or char == '?' or char == '!') and (not isConversation):  # 서술 문장 마침
            sentence_table[buffer] = char
            isCon.append("서술문")
            isNext.append(" ")
            buffer = ""
    sentence_table["test"] = "test"
    df = pd.DataFrame(sentence_table.items(), columns=['문장', '구두 문자'])
    df['문장 종류'] = pd.Series(isCon, index=df.index)
    df['연결 여부'] = pd.Series(isNext, index=df.index)
    return df


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

    sentiments = ['anger', 'anticipation', 'disgust', 'fear', 'joy', 'sadness', 'surprise', 'trust']

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
        val1 = stab.findall(line_data)[2]  # 감정의 종류 (ex. anger, joy)
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
