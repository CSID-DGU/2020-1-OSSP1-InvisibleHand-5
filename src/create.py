import os
import numpy as np
import pandas as pd


# 소설 입력
def open_book(fileName):
    fileName = fileName + ".txt"
    book = open(f'../res/book/{fileName}', "rt", encoding='UTF8', errors='ignore')
    return book


# 결과 출력용 디렉토리 생성
def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("디렉토리 생성에 실패했습니다." + directory)


# 사용자 입력받아서 사전에 등장인물 고유명사로 추가
def create_userdic(numOfCharacter):
    listOfCharacter = []
    userdic = open("user_dic.txt", "wt", encoding='UTF8')  # userdic 저장 경로 변경
    for n in range(0, numOfCharacter):
        name = input(f"등장인물 {n + 1} : ")
        userdic.write(f"{name}\tNNP\n")
        listOfCharacter.append(name)
    userdic.close()
    return listOfCharacter


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
    if len(connect) < len(sentence):  # 마지막 문장 예외처리
        connect.append("")
    return sentence, punctuation, kind, connect


# 문장 데이터프레임 생성 [문장, 구두문자, 문장 종류, 연결 여부, 주어, 목적어, 감정 별 점수]
def create_sentence_dataframe(context, listOfEmotion):
    sentence, punctuation, kind, connect = create_sentence_list(context)
    df = pd.DataFrame(sentence, columns=['문장'])
    df['페이지 번호'] = 0
    df['구두 문자'] = pd.Series(punctuation, index=df.index)
    df['문장 종류'] = pd.Series(kind, index=df.index)
    df['대화 진행 여부'] = ""
    df['연결 여부'] = pd.Series(connect, index=df.index)
    #df['핵심 문장'] = ""
    df['감정 단어'] = ""
    df['화자'] = ""
    df['lemma'] = ""
    for emo in listOfEmotion:
        df[f'{emo}'] = 0.0
    return df


def save_df(df, storyName, fileName):
    df.to_excel(f"../res/output/{storyName}/{fileName}.xlsx")
