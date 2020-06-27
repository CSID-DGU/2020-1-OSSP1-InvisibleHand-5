import re
import create
import nltk
from konlpy.tag import Komoran
from nltk.tag import StanfordPOSTagger
import pandas as pd
import morphs

# 감정 데이터프레임 입력
def open_emotion_dataframe():
    df = pd.read_excel('../res/dic/감정 단어.xlsx', index_col=0, convert_float=True)
    return df

# 감정 단어 품사 태깅
def emotion_pos_tagging():
    tag_target = ['V', 'N', 'J', 'R']
    tag_list = []

    # 단어 사전 엑셀 파일 입력
    df_emotion = open_emotion_dataframe()

    # 품사 태깅
    for word in df_emotion['영어']:
        STANFORD_POS_MODEL_PATH = "path/english-bidirectional-distsim.tagger"
        STANFORD_POS_JAR_PATH = "path/stanford-postagger-3.9.2.jar"

        pos_tagger = StanfordPOSTagger(STANFORD_POS_MODEL_PATH, STANFORD_POS_JAR_PATH)

        pos = pos_tagger.tag([word])
        tag_first = pos[0][1][0]
        if tag_first in tag_target:
            if tag_first == 'V':
                tag_list.append('동사')
            if tag_first == 'N':
                tag_list.append('명사')
            if tag_first == 'J':
                tag_list.append('형용사')
            if tag_first == 'R':
                tag_list.append('부사')
        else:
            tag_list.append('')
    df_emotion['품사'] = tag_list

    # 품사 태깅한 확장 단어 사전 데이터프레임 출력
    df_emotion.to_excel(f"../res/dic/감정 단어.xlsx")


# 감정 단어 lemmatization
def emotion_lemmatization():
    lemma = ""
    df_emotion = open_emotion_dataframe()

    for i, pos in enumerate(df_emotion['품사']):
        df_emotion.at[i + 1, 'lemma'] = ""
        if(pos == '동사' or pos == '형용사'):
            word = (df_emotion.at[i+1, '한글'])
            lemma = morphs.lemmatize_word(word)
            #print(word, lemma)
            if(lemma == '하다'):
                continue
            df_emotion.at[i+1, 'lemma'] = lemma
        else:
             lemma = ""
    df_emotion.to_excel(f"../res/dic/감정 단어.xlsx")

    return df_emotion


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
