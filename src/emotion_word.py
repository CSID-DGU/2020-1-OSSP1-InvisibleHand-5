import re
import pandas as pd

def emotion_pos_tagging():


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
        if stab.findall(line_data)[2] == "anger":  # 감정의 종류 (ex. anger, joy)
            val1 = "분노"
        if stab.findall(line_data)[2] == "anticipation":  # 감정의 종류 (ex. anger, joy)
            val1 = "기대"
        if stab.findall(line_data)[2] == "disgust":  # 감정의 종류 (ex. anger, joy)
            val1 = "혐오"
        if stab.findall(line_data)[2] == "fear":  # 감정의 종류 (ex. anger, joy)
            val1 = "공포"
        if stab.findall(line_data)[2] == "joy":  # 감정의 종류 (ex. anger, joy)
            val1 = "기쁨"
        if stab.findall(line_data)[2] == "sadness":  # 감정의 종류 (ex. anger, joy)
            val1 = "슬픔"
        if stab.findall(line_data)[2] == "surprise":  # 감정의 종류 (ex. anger, joy)
            val1 = "놀람"
        if stab.findall(line_data)[2] == "trust":  # 감정의 종류 (ex. anger, joy)
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
