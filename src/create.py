import numpy as np


def open_book():
    fileName = input("소설명 : ") + ".txt"
    book = open(f'../res/book/{fileName}', "rt", encoding='UTF8')
    return book


# 사용자 입력받아서 사전에 등장인물 고유명사로 추가
def create_userdic(numOfCharacter, listOfCharacter):
    userdic = open("../user_dic.txt", "wt", encoding='UTF8')
    for n in range(0, numOfCharacter):
        name = input(f"등장인물{n} : ")
        userdic.write(f"{name}\tNNP\n")
        listOfCharacter.append(name)
    return userdic

# <결과 1. 각 등장인물의 페이지별 각 감정 수준> 을 표현할
# [등장인물][감정][페이지] 구조의 3차원 벡터 생성
def create_emotion_vector(numOfCharacter, numOfEmotion, numOfPage):
    vector = np.zeros(numOfCharacter * numOfEmotion * numOfPage)
    emotion_vector = vector.reshape(numOfCharacter, numOfEmotion, numOfPage)
    return emotion_vector


# <결과 2. 모든 등장인물의 페이지별 감정 흐름>을 표현할
# [등장인물][페이지] 구조의 2차원 벡터 생성
def create_sentiment_vector(numOfCharacter, numOfEmotion, numOfPage):
    vector = np.zeros(numOfCharacter * numOfPage)
    sentiment_vector = vector.reshape(numOfCharacter, numOfPage)
    return sentiment_vector