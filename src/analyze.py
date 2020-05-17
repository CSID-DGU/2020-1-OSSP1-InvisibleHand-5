# -*- coding: utf-8 -*-
import nltk
import create
import pandas as pd
import grammar
import morphs

# 감정 사전에서 단어 찾기
def find_word(emotion_dictionary_lists, token):
    for emo in emotion_dictionary_lists:
        if token[0] in emo.keys():
            return emo[token[0]]
    return -1, 0  # 단어사전에 없었다면

# 문장 성분 분석
def input_element(df, index, token_list):
    parser = nltk.RegexpParser(grammar.grammar)
    chunks = parser.parse(token_list)
    subject = []
    object = []
    for sub_tree in chunks.subtrees():
        if sub_tree.label() == "주어":
            subject.append(sub_tree[0][0])
        elif sub_tree.label() == "목적어":
            object.append(sub_tree[0][0])
    df.at[index, "주어"] = subject
    df.at[index, "목적어"] = object
    return df

# 감정 분석
def input_emotion_word(df,index, emotion_dictionary_lists, token_list):
    emo_word = []
    for token in token_list:
        word_result = find_word(emotion_dictionary_lists, token)
        if word_result != (-1, 0):  # 문장에서 단어 사전에 있는 단어가 있다면
            emo_word.append(token[0])
            df.at[index, f"{word_result[0]}"] += float(word_result[1])
    df.at[index, "감정 단어"] = emo_word
    return df

# 화자 분석
def input_character(df, index, listOfCharacter, token_list):
    count = [0 for i in range(len(listOfCharacter))]  # 문장 당 등장인물의 출현 횟su

    for token in token_list:
        if token[0] in listOfCharacter:  # 문장에서 등장인물 등장 체크
            count[listOfCharacter.index(token[0])] += 1
    for i, c in enumerate(count):
        if c >= 1:
            df.at[index, "화자"]=[listOfCharacter[i], str(c)]
    return df

def analyze_sentence(df, listOfCharacter, emotion_dictionary_lists, charOfPage):
    page_num = 0
    length = 0
    index = 0

    for line in df["문장"]:
        if(length > charOfPage):
            page_num = page_num + 1
            length = 0
        length = length + len(line)#
        df.at[index, "페이지 번호"] = page_num

        token_list = morphs.tokenizer(line)
        df = input_element(df, index, token_list) #df에 주어,목적어 값 입력
        df = input_emotion_word(df,index,emotion_dictionary_lists,token_list) #df에 감정 단어 및 감정 값 입력
        df = input_character(df,index, listOfCharacter,token_list) #df에 화자 값 입력
        index = index + 1
    return df
