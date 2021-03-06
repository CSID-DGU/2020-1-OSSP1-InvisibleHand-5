# -*- coding: utf-8 -*-
import nltk
import create
import numpy as np
import sympy
import pandas as pd
import grammar
import morphs
from collections import defaultdict


# 감정 사전에서 단어 찾기
def find_word(df_emotion, token):
    tag_all = ['NNB', 'NNG', 'NNP', 'NP', 'VV', 'VA', 'MAG', 'MAJ']
    tag_noun = ['NNB', 'NNG', 'NNP', 'NP']
    tag_verb = ['VV']
    tag_adj = ['VA']
    tag_adv = ['MAG', 'MAJ']
    tag = ""
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

    df_filter = df_emotion[((df_emotion['한글'] == token[0])
                            & (df_emotion['품사'] == tag))]
    if len(df_filter) == 0:  # 조건을 만족하는 행이 없으면 -1, 0 반환
        return [-1], [0]
    else:  # 있으면 감정, 점수 반환
        return df_filter['감정'].tolist(), df_filter['점수'].tolist()


# 감정 사전에서 단어 찾기(lemma)
def find_word_lemma(df_emotion, lemma):
    # print(lemma)
    df_filter = df_emotion[(df_emotion['lemma'] == lemma)]
    if len(df_filter) == 0:  # 조건을 만족하는 행이 없으면 -1, 0 반환
        return [-1], [0]
    else:  # 있으면 감정, 점수 반환
        return df_filter['감정'].tolist(), df_filter['점수'].tolist()


# 주어 목적어 분석 기능을 -> 구문 분석 모듈로 확장 (input_element -> parser)
# 구문 분석
def parser(df, index, token_list, listOfCharacter):
    parser = nltk.RegexpParser(grammar.grammar)
    chunks = parser.parse(token_list)

    tlist = ["NNG", "NNP", "NP", "NNB"]
    subject = []
    object = []
    busa = []
    kwanhyeong = []
    # print(chunks)
    for sub_tree in chunks.subtrees():
        if sub_tree.label() == "주어":
            subject.append(sub_tree[0][0])
        elif sub_tree.label() == "목적어":
            object.append(sub_tree[0][0])
        elif sub_tree.label() == "부사어":
            busa.append(sub_tree[0][0])
        elif sub_tree.label() == "관형어":
            if sub_tree[0][1] != "MM":
                kwanhyeong.append(sub_tree[0][0])
    return subject, object, busa, kwanhyeong


# 감정 분석
def input_emotion_word(df, index_word, df_emotion, token_list):
    emo_word = []

    for token in token_list:
        emotion_list, score_list = find_word(df_emotion, token)
        if -1 not in emotion_list:  # 문장에서 단어 사전에 있는 단어가 있다면
            emo_word.append(token[0])  # 단어 란에 입력
            for emo in emotion_list:
                if emo == '분노':
                    # 감정과 점수 입력
                    df.at[index_word,
                          '분노'] += float(score_list[emotion_list.index(emo)])

                elif emo == '기쁨':
                    # 감정과 점수 입력
                    df.at[index_word,
                          '기쁨'] += float(score_list[emotion_list.index(emo)])

                elif emo == '슬픔':
                    # 감정과 점수 입력
                    df.at[index_word,
                          '슬픔'] += float(score_list[emotion_list.index(emo)])

                elif emo == '공포':
                    # 감정과 점수 입력
                    df.at[index_word,
                          '공포'] += float(score_list[emotion_list.index(emo)])

                elif emo == '혐오':
                    # 감정과 점수 입력
                    df.at[index_word,
                          '혐오'] += float(score_list[emotion_list.index(emo)])

                elif emo == '놀람':
                    # 감정과 점수 입력
                    df.at[index_word,
                          '놀람'] += float(score_list[emotion_list.index(emo)])
    lem_list = df.at[index_word, 'lemma']
    for lem in lem_list:
        emotion_list, score_list = find_word_lemma(df_emotion, lem)
        if -1 not in emotion_list:  # 문장에서 단어 사전에 있는 단어가 있다면
            emo_word.append(lem)  # 단어 란에 입력
            for emo in emotion_list:
                if emo == '분노':
                    # 감정과 점수 입력
                    df.at[index_word,
                          '분노'] += float(score_list[emotion_list.index(emo)])
                elif emo == '기쁨':
                    # 감정과 점수 입력
                    df.at[index_word,
                          '기쁨'] += float(score_list[emotion_list.index(emo)])
                elif emo == '슬픔':
                    # 감정과 점수 입력
                    df.at[index_word,
                          '슬픔'] += float(score_list[emotion_list.index(emo)])
                elif emo == '공포':
                    # 감정과 점수 입력
                    df.at[index_word,
                          '공포'] += float(score_list[emotion_list.index(emo)])
                elif emo == '혐오':
                    # 감정과 점수 입력
                    df.at[index_word,
                          '혐오'] += float(score_list[emotion_list.index(emo)])
                elif emo == '놀람':
                    # 감정과 점수 입력
                    df.at[index_word,
                          '놀람'] += float(score_list[emotion_list.index(emo)])
    df.at[index_word, "감정 단어"] = emo_word
    return df


# 화자 분석
def input_character(df, index_word, listOfCharacter, token_list):
    subject, object, busa, kwanhyeong = parser(
        df, index_word, token_list, listOfCharacter)
    count = [0 for i in range(len(listOfCharacter))]  # 문장 당 등장인물의 출현 횟su
    flag = True
    nplist = ["그", "그녀", ""]
    for i, token in enumerate(token_list):
        # print(token)
        if token[0] in listOfCharacter:  # 문장에서 등장인물 등장 체크
            count[listOfCharacter.index(token[0])] += 1
            if token[0] in subject:
                flag = True
            elif token[0] in object:
                flag = False
            elif token[0] in busa:
                flag = True
            elif token[0] in kwanhyeong:
                flag = True
        if token[1] == 'NP':
            if token[0] in nplist:
                if index_word > 0 and df.at[index_word - 1, "화자"] in listOfCharacter:
                    df.at[index_word, "화자"] = token[0] + \
                        "(" + df.at[index_word - 1, "화자"] + ")"
                    if df.at[index_word - 2, '연결 여부'] == '연결':
                        df.at[index_word - 2, "화자"] = df.at[index_word - 1, "화자"]
    for i, c in enumerate(count):
        if c >= 1 & flag == True:
            df.at[index_word, "화자"] = listOfCharacter[i]
            if (index_word > 0 and df.at[index_word - 1, '연결 여부'] == '연결'):
                df.at[index_word - 1, "화자"] = listOfCharacter[i]
    if df.at[index_word, '대화 진행 여부'] == '시작':
        if df.at[index_word, '화자'] != "":
            ch = df.at[index_word, '화자']
            while (True):
                if df.at[index_word + 2, '대화 진행 여부'] == "":
                    break
                index_word += 2
                df.at[index_word, '화자'] = ch
    return df


# 대화의 시작과 끝 분석
def analyze_conversation(df):
    index_word = 0
    cnt = 0
    connect = False
    conver = False
    start_index_list = []
    end_index_list = []
    for i, con_kind in enumerate(df['문장 종류']):
        if con_kind == '대화문':
            conver = True
            cnt += 1
            # if (df.at[index_word, '연결 여부'] == '연결'):
            #     connect = True
            # else:
            #     connect = False
        elif con_kind == '서술문':
            if conver == True:
                if (cnt >= 2):
                    df.at[i - cnt, '대화 진행 여부'] = '시작'
                    for j in range((i - cnt) + 1, i - 1):
                        df.at[j, '대화 진행 여부'] = '대화 중'
                    df.at[i - 1, '대화 진행 여부'] = '끝'
                    cnt = 0
                else:
                    conver = False
                    cnt = 0
            # if (connect == True):
            #     connect = False
            #     conver = True
            #     cnt += 1
            # else:
        index_word += 1
    return df


# 핵심 문장 분석
def input_main_sentence(df, index_word, token_list):
    termination_list = ['EC', 'EF', 'EP', 'ETM', 'ETN']
    i = 0
    str = ""
    flag = 0
    for i, token in enumerate(token_list):
        if token[1] == 'EF':
            # print(token, token_list[i])
            # print(i, j)
            for k in reversed(range(i)):
                if k == 0:
                    for p in range(i):
                        if token_list[p][1] in termination_list:
                            # print(token_list[p])
                            flag = 1
                            break
                if flag == 1:
                    break
                # print(k, token_list[k])
                if token_list[k][1] == 'EC':
                    for s in range(k + 1, i + 1):
                        str += token_list[s][0] + " "
                    flag = 1
                    break
            if flag == 1:
                flag = 0
                break
    return df


def input_lemma(df, index_word, token_list):
    lemma_list = []

    for token in token_list:
        lemma = morphs.lemmatize_token(token)
        if lemma is not None:
            lemma_list.append(lemma)

    df.at[index_word, 'lemma'] = lemma_list
    return df


# 단어의 빈도수
count = defaultdict(lambda: 0)


def get_frequency(token_list):
    nList = ['NNP', 'NNG']
    for word in token_list:
        if word[1] in nList:
            count[word[0]] += 1


# 메인
def analyze_sentence(df, listOfCharacter, df_emotion, charOfPage):
    page_num = 0
    length = 0
    index_word = 0

    df = analyze_conversation(df)
    for line in df["문장"]:
        if length > charOfPage:
            page_num = page_num + 1
            length = 0
        length = length + len(line)  #
        df.at[index_word, "페이지 번호"] = page_num

        token_list = morphs.tokenizer(line)
        # parser(df, index, token_list,listOfCharacter)  # df에 주어,목적어 값 입력
        df = input_character(df, index_word, listOfCharacter,
                             token_list)  # df에 화자 값 입력
        df = input_lemma(df, index_word, token_list)
        get_frequency(token_list)
        # df에 감정 단어 및 감정 값 입력
        df = input_emotion_word(df, index_word, df_emotion, token_list)
        index_word = index_word + 1

    return df, page_num+1


# original
def merge_character(df_sentence, listOfEmotion, listOfCharacter):
    writer = pd.ExcelWriter("res/output/등장인물.xlsx", engine='openpyxl')

    df_list_character = []

    for character in listOfCharacter:

        df_character = df_sentence[listOfEmotion]

        for i in df_sentence.index:
            df_character.loc[i, listOfEmotion] = 0

        # 화자 필터링
        for i in df_sentence.index:
            if df_sentence.loc[i]['화자'] == character:
                df_character.loc[i,
                                 listOfEmotion] = df_sentence.loc[i, listOfEmotion]

        df_list_character.append(df_character)
        df_character.to_excel(writer, sheet_name=f"{character}")

    writer.save()
    return df_list_character


def merge_character_page(df_sentence, numOfPage, listOfEmotion, listOfCharacter):
    writer = pd.ExcelWriter("res/output/등장인물_페이지.xlsx", engine='openpyxl')

    df_list_character = []

    for character in listOfCharacter:
        df_character = pd.DataFrame(index=range(0, numOfPage), columns=[
                                    f"{emotion}" for emotion in listOfEmotion])
        for num in range(0, numOfPage):
            m1 = ((df_sentence['페이지 번호'] == num) &
                  (df_sentence['화자'] == character))
            page_filtered_df = df_sentence.loc[m1]
            # 추출한 행들의 감정 열 추출
            page_filtered_df = page_filtered_df.loc[:,
                                                    ('기쁨', '슬픔', '분노', '공포', '혐오', '놀람')]
            emotion_sum_df = page_filtered_df.sum(axis=0)  # 감정 별 합 추출
            df_character.loc[num] = emotion_sum_df  # 등장인물 데이터프레임에 감정 별 합 대입
        df_list_character.append(df_character)
        df_character.to_excel(writer, sheet_name=f"{character}")

    writer.save()
    return df_list_character


# 단순 가중치 적용 모델

# def merge_character(df_sentence, listOfEmotion, listOfCharacter):
#     writer = pd.ExcelWriter("../res/output/등장인물.xlsx", engine='openpyxl')
#
#     df_character = df_sentence[listOfEmotion]
#     df_list_character = []
#
#     for character in listOfCharacter:
#         # 해당 등장인물이 아닌 문장 감정 값 0으로 초기화
#         for i in df_sentence.index:
#             # i 행의 '화자' 열
#             if df_sentence.loc[i]['화자'] != character:
#                 df_character.loc[i, listOfEmotion] = 0
#
#         # 0 으로 초기화한 값 이전 값의 기울기 적용
#         for emo in listOfEmotion:  # 감정 별로
#
#             index_last = 0
#             score_last = 0
#             index_now = 0
#
#             # 감정값이 0 인 문장 연속 개수
#             # 20문장 이상일 경우 상황이 끝났다고 판단
#             # 문법 분석에서 상황 종료 판단 가능 시 수정
#             non_emotion_count = 1
#             emotion_count = 1
#             acc_value = 0
#             proceeding_flag = False  # 상황 진행임을 알려주는 변수
#
#             s_emo = df_character[emo]  # 시리즈 추출
#             for j in range(len(s_emo)):
#                 if proceeding_flag:  # 상황 진행 중이라면
#                     if non_emotion_count < 20:  # 감정이 없는 문장 20 연속으로 나오지 않았을 경우
#                         if s_emo[j] == 0:
#                             non_emotion_count = non_emotion_count + 1
#                             s_emo[j] = s_emo[j] * 0.8
#                         else:
#                             non_emotion_count = 1
#                         acc_value = acc_value + s_emo[j]
#                         emotion_count = emotion_count + 1
#                         s_emo[j] = s_emo[j] + acc_value  # 상황 진행 중의 감정의 평균 값을 가중치로 더함
#                     else:  # 20연속 감정 없는 문장 등장 -> 상황 종료라고 판단
#                         proceeding_flag = False  # 상황 종료
#                         non_emotion_count = 1
#                         emotion_count = 1
#                         acc_value = 0
#                 else:  # 상황 종료 중이였다면
#                     if s_emo[j] != 0:  # 감정 문장 등장 -> 상황 시작
#                         proceeding_flag = True
#                         acc_value = s_emo[j]
#                     else:
#                         pass
#
#             df_character[emo] = s_emo.values
#         df_character.to_excel(writer, sheet_name=f"{character}")
#         df_list_character.append(df_character)
#
#     writer.save()
#     return df_list_character


# 단순 절대값 적용 모델
#
# def merge_character(df_sentence, listOfEmotion, listOfCharacter):
#     writer = pd.ExcelWriter("../res/output/등장인물.xlsx", engine='openpyxl')
#
#     df_character = df_sentence[listOfEmotion]
#     df_list_character = []
#
#     for character in listOfCharacter:
#         # 해당 등장인물이 아닌 문장 감정 값 0으로 초기화
#         for i in df_sentence.index:
#             # i 행의 '화자' 열
#             if df_sentence.loc[i]['화자'] != character:
#                 df_character.loc[i, listOfEmotion] = 0
#
#         # 0 으로 초기화한 값 이전 값의 기울기 적용
#         for emo in listOfEmotion:  # 감정 별로
#             s_emo = df_character[emo]  # 시리즈 추출
#             for j in range(len(s_emo)):
#                 if j != 0:
#                     if s_emo[j] == 0:
#                         s_emo[j] = s_emo[j-1] - 0.01
#                     else:
#                         s_emo[j] = s_emo[j-1] + s_emo[j]
#             df_character[emo] = s_emo.values
#         df_character.to_excel(writer, sheet_name=f"{character}")
#         df_list_character.append(df_character)
#
#     writer.save()
#     return df_list_character


# 단순 기울기 적용 모델
#
# def merge_character(df_sentence, listOfEmotion, listOfCharacter):
#     writer = pd.ExcelWriter("../res/output/등장인물.xlsx", engine='openpyxl')
#
#     df_character = df_sentence[listOfEmotion]
#     df_list_character = []
#
#     for character in listOfCharacter:
#         # 해당 등장인물이 아닌 문장 감정 값 0으로 초기화
#         for i in df_sentence.index:
#             # i 행의 '화자' 열
#             if df_sentence.loc[i]['화자'] != character:
#                 df_character.loc[i, listOfEmotion] = 0
#
#         # 0 으로 초기화한 값 이전 값의 기울기 적용
#         for emo in listOfEmotion:  # 감정 별로
#             index_last = 0
#             score_last = 0
#             index_now = 0
#
#             s_emo = df_character[emo]  # 시리즈 추출
#             for v in s_emo.values:  #
#                 if v != 0:
#                     incl = (score_last - v) / (index_last - index_now)  # x 변화량 / y 변화량 = 기울기
#                     for j in range(index_last + 1, index_now):  # 사이 값
#                         s_emo[j] = score_last + incl * (j - index_last)  # 기울기* x 변화량 만큼 증감
#                     index_last = index_now
#                     score_last = v
#                 index_now = index_now + 1
#             df_character[emo] = s_emo.values
#         df_character.to_excel(writer, sheet_name=f"{character}")
#         df_list_character.append(df_character)
#     writer.save()
#     return df_list_character

# 페이지 단위
def merge_sentence_page(df_sentence, numOfPage, listOfEmotion, listOfCharacter):
    writer = pd.ExcelWriter("/res/output/등장인물.xlsx", engine='openpyxl')

    df_list_character = []
    df_character = pd.DataFrame(index=range(0, numOfPage), columns=[
                                f"{emotion}" for emotion in listOfEmotion])

    for character in listOfCharacter:
        for num in range(0, numOfPage):
            m1 = ((df_sentence['페이지 번호'] == num) &
                  (df_sentence['화자'] == character))
            page_filtered_df = df_sentence.loc[m1]
            # 추출한 행들의 감정 열 추출
            page_filtered_df = page_filtered_df.loc[:,
                                                    ('기쁨', '슬픔', '분노', '공포', '혐오', '놀람')]
            emotion_sum_df = page_filtered_df.sum(axis=0)  # 감정 별 합 추출
            df_character.loc[num] = emotion_sum_df  # 등장인물 데이터프레임에 감정 별 합 대입
        df_list_character.append(df_character)
        df_character.to_excel(writer, sheet_name=f"{character}")

    writer.save()
    return df_list_character
