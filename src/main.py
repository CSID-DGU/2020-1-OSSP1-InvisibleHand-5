import sys

# 전처리 모듈
import preprocessing
# 형태소 분석 모듈
# import module.morphs
# 구문 분석 모듈
# import module.syntax
from konlpy.tag import Komoran
from matplotlib import pyplot as plt # graph #python -m pip install matplotlib
import numpy as np

numOfPage = 200
numOfEmotion = 6

# ---------- 1. 입력 데이터 설정 ----------
# 파일 입력
fileName = input() + ".txt"
book = open(f'../res/book/{fileName}', "rt", encoding='UTF8')
userDic = open("../user_dic.txt", "wt", encoding='UTF8')

# 감정을 추출할 등장인물 수
numOfCharacter = int(input())
listOfCharacter = []

# [등장인물][페이지][감정] 구조의 3차원 벡터 생성
v = np.empty(numOfCharacter * numOfPage * numOfEmotion)
vector = v.reshape(numOfCharacter, numOfPage, numOfEmotion)

# 사용자 사전에 등장인물 고유명사로 추가
for n in range(0, numOfCharacter):
    name = input()
    userDic.write(f"{name} nnp\n")
    listOfCharacter.append(name)
userDic.close()

# ---------- 2. 전처리 ----------
# 개행 문자 제거 , 꺽쇠 -> 따옴표 변환 ,
context = preprocessing.del_new_lines(book)

# 단위  1p? = 전체 글자수 / 200
unit = int(len(context) / numOfPage)

# ---------- 3. 감정 추출 ----------

# ---------- 4. 감정 분석 ----------

# ---------- 5. 결과 추출 ----------

x = np.arange(1, numOfPage)
y = x * 5

plt.plot(x, y)
plt.show()

book.close()
