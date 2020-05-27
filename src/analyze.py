# -*- coding: utf-8 -*-
import nltk
import create
import numpy as np
import pandas as pd
import grammar
import morphs


# 감정 사전에서 단어 찾기
def find_word(df_emotion, token):
    tag_all = ['NNB', 'NNG', 'NNP', 'NP', 'VV', 'VA', 'MAG', 'MAJ']
    tag_noun = ['NNB', 'NNG', 'NNP', 'NP']
    tag_verb = ['VV']
    tag_adj = ['VA']
    tag_adv = ['MAG', 'MAJ']

    if token[1] in tag_all:  # 명사, 동사, 형용사, 부사인지 확인
        if token[1] in tag_noun:
            tag = "명사"
        elif token[1] in tag_verb:
            tag = "동사"
        elif token[1] in tag_adj:
            tag = "부사"
        elif token[1] in tag_adv:
            tag = "형용사"
    else:  # 다른 품사일 경우 -1, 0 반환 ( 감정 단어 사전에 없음 )
        return [-1], [0]

    df_filter = df_emotion[(df_emotion['한글'] == token[0]) & (df_emotion['품사'] == tag)]
    if len(df_filter) == 0:  # 조건을 만족하는 행이 없으면 -1, 0 반환
        return [-1], [0]
    else:  # 있으면 감정, 점수 반환
        return df_filter['감정'].tolist(), df_filter['점수'].tolist()
    return [-1], [0]  # 단어사전에 없었다면

# 주어 목적어 분석 기능을 -> 구문 분석 모듈로 확장 (input_element -> parser)
# 구문 분석
def parser(df, index, token_list, listOfCharacter):
    parser = nltk.RegexpParser(grammar.grammar)
    chunks = parser.parse(token_list)
    print(chunks)

    tlist = ["NNG","NNP","NP","NNB"]
    subject = []
    object = []
    busa = []
    kwanhyeong = []
    for sub_tree in chunks.subtrees():
        if sub_tree.label() == "주어":
            subject.append(sub_tree[0][0])
        elif sub_tree.label() == "목적어":
            object.append(sub_tree[0][0])
            #print(sub_tree[0])
        elif sub_tree.label() == "부사어":
            busa.append(sub_tree[0][0])
        elif sub_tree.label() == "관형어":
            if(sub_tree[0][1] != "MM"):
                print("관형어인데 MM아닌거" + sub_tree[0][0])
                kwanhyeong.append(sub_tree[0][0])

        #df.at[index, "주어"] = subject
        #df.at[index, "목적어"] = object
    return subject, object, busa, kwanhyeong

# def input_emotion_word(df, index, emotion_dictionary_lists, token_list):
#     emo_word = []
#     for token

# 감정 분석
def input_emotion_word(df, index_word, df_emotion, token_list):
    emo_word = []
    # 중복 계산 방지
    anger_flag = False
    joy_flag = False
    sadness_flag = False
    fear_flag = False
    disgust_flag = False
    surprise_flag = False

    for token in token_list:
        emotion_list, score_list = find_word(df_emotion, token)
        if -1 not in emotion_list:  # 문장에서 단어 사전에 있는 단어가 있다면
            emo_word.append(token[0])  # 단어 란에 입력
            for emo in emotion_list:
                if emo == 'anger' and anger_flag is False:
                    df.at[index_word, '분노'] += float(score_list[emotion_list.index(emo)])  # 감정과 점수 입력
                    anger_flag = True
                elif emo == 'joy' and joy_flag is False:
                    df.at[index_word, '기쁨'] += float(score_list[emotion_list.index(emo)])  # 감정과 점수 입력
                    joy_flag = True
                elif emo == 'sadness' and sadness_flag is False:
                    df.at[index_word, '슬픔'] += float(score_list[emotion_list.index(emo)])  # 감정과 점수 입력
                    sadness_flag = True
                elif emo == 'fear' and fear_flag is False:
                    df.at[index_word, '공포'] += float(score_list[emotion_list.index(emo)])  # 감정과 점수 입력
                    fear_flag = True
                elif emo == 'disgust' and disgust_flag is False:
                    df.at[index_word, '혐오'] += float(score_list[emotion_list.index(emo)])  # 감정과 점수 입력
                    disgust_flag = True
                elif emo == 'surprise' and surprise_flag is False:
                    df.at[index_word, '놀람'] += float(score_list[emotion_list.index(emo)])  # 감정과 점수 입력
                    surprise_flag = True
    df.at[index_word, "감정 단어"] = emo_word
    return df


# 화자 분석
def input_character(df, index, listOfCharacter, token_list):
    subject, object, busa, kwanhyeong = parser(df, index, token_list, listOfCharacter)
    count = [0 for i in range(len(listOfCharacter))]  # 문장 당 등장인물의 출현 횟su
    flag = True
    nplist = ["그", "그녀",""]
    for i, token in enumerate(token_list):
        #print(token)
        if token[0] in listOfCharacter:  # 문장에서 등장인물 등장 체크
            count[listOfCharacter.index(token[0])] += 1
            if(token[0] in subject):
                flag = True
            elif(token[0] in object):
                flag = False
            elif(token[0] in busa):
                flag = True
            elif(token[0] in kwanhyeong):
                flag = True
        if token[1] == "NP":
            if token[0] in nplist:
                if(df.at[index-1, "화자"] in listOfCharacter):
                    df.at[index, "화자"] = token[0] + "(" + df.at[index-1,"화자"] + ")"
                    print(token[0] + "(" + df.at[index-1, "화자"] + ")")
    for i, c in enumerate(count):
        if c >= 1 & flag == True:
            df.at[index, "화자"] = listOfCharacter[i]
            print("------화자"+listOfCharacter[i])
    print("")
    return df


# 메인
def analyze_sentence(df, listOfCharacter, df_emotion, charOfPage):
    page_num = 0
    length = 0
    index_word = 0

    for line in df["문장"]:
        if (length > charOfPage):
            page_num = page_num + 1
            length = 0
        length = length + len(line)  #
        df.at[index_word, "페이지 번호"] = page_num

        token_list = morphs.tokenizer(line)
        #parser(df, index, token_list,listOfCharacter)  # df에 주어,목적어 값 입력
        df = input_character(df, index_word, listOfCharacter, token_list)  # df에 화자 값 입력
        df = input_emotion_word(df, index_word, df_emotion, token_list)  # df에 감정 단어 및 감정 값 입력
        index_word = index_word + 1
    return df


def merge_sentence(df_sentence, numOfPage, listOfEmotion, listOfCharacter):
    writer = pd.ExcelWriter("../res/output/등장인물.xlsx", engine='openpyxl')

    df_list_character = []
    df_character = pd.DataFrame(index=range(0, numOfPage), columns=[f"{emotion}" for emotion in listOfEmotion])

    for character in listOfCharacter:
        for num in range(0, numOfPage):
            '''
            page_speaker_filter = df_sentence['페이지 번호'].isin([num]) & df_sentence['화자'].isin([character])
            #speaker_filter = df_sentence['화자'].isin([character])
            page_filtered_df = df_sentence[page_speaker_filter]  # num 페이지 행들 추출
'''
            m1 = ((df_sentence['페이지 번호'] == num) & (df_sentence['화자'] == character))
            page_filtered_df = df_sentence.loc[m1]
            page_filtered_df = page_filtered_df.loc[:, ('기쁨', '슬픔', '분노', '공포', '혐오', '놀람')]  # 추출한 행들의 감정 열 추출
            emotion_sum_df = page_filtered_df.sum(axis=0)  # 감정 별 합 추출
            df_character.loc[num] = emotion_sum_df  # 등장인물 데이터프레임에 감정 별 합 대입
        df_list_character.append(df_character)
        df_character.to_excel(writer, sheet_name=f"{character}")

    writer.save()
    return df_list_character
