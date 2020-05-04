import preprocessing
# 형태소 분석 모듈
# import module.morphs
# 구문 분석 모듈
# import module.syntax
from konlpy.tag import Komoran
from matplotlib import pyplot as plt
from matplotlib import font_manager as fm
import numpy as np

numOfPage = 200
numOfEmotion = 6

# -------------------- 1. 입력 데이터 설정 --------------------
# 파일 입력
fileName = input() + ".txt"
book = open(f'../res/book/{fileName}', "rt", encoding='UTF8')
userDic = open("../user_dic.txt", "wt", encoding='UTF8')

# 감정을 추출할 등장인물 수 입력
numOfCharacter = int(input())
listOfCharacter = []

# <결과 1. 각 등장인물의 페이지별 각 감정 수준> 을 표현할
# [등장인물][감정][페이지] 구조의 3차원 벡터 생성
v1 = np.zeros(numOfCharacter * numOfEmotion * numOfPage)
vector1 = v1.reshape(numOfCharacter, numOfEmotion, numOfPage)

# <결과 2. 모든 등장인물의 페이지별 감정 흐름>을 표현할
# [등장인물][페이지] 구조의 2차원 벡터 생성
v2 = np.zeros(numOfCharacter * numOfPage)
vector2 = v2.reshape(numOfCharacter, numOfPage)

# 사용자 사전에 등장인물 고유명사로 추가
for n in range(0, numOfCharacter):
    name = input()
    userDic.write(f"{name}\tNNP\n")
    listOfCharacter.append(name)

userDic.close()

# -------------------- 2. 전처리 --------------------
# 개행 문자 제거 , 꺽쇠 -> 따옴표 변환 ,
context = preprocessing.del_new_lines(book)

# 단위  1p? = 전체 글자수 / 200
unit = int(len(context) / numOfPage)

# -------------------- 3. 감정 추출 --------------------


# -------------------- 4. 감정 분석 --------------------


# -------------------- 5. 결과 추출 --------------------

fontprop = fm.FontProperties(fname="../res/fonts/malgun.ttf", size=24).get_name()
plt.rc('font', family=fontprop)
plt.rcParams['axes.unicode_minus'] = False

# 결과 1. 각 등장인물의 페이지별 감정 수준
# 등장인물 별 그래프 생성 및 페이지별 감정 레벨 값 대입
x = np.arange(1, numOfPage)

for num in range(0, numOfCharacter):
    plt.figure(num)
    plt.xlabel('페이지')
    plt.ylabel('감정 레벨')
    for emo in range(0, numOfEmotion):
        plt.plot(x, vector1[num][emo][x])

# 결과 2. 모든 등장인물의 페이지별 감정 흐름
# 그래프 생성 및 등장인물 별 감정 흐름 값 대입
plt.figure(numOfCharacter)
plt.plot(x, vector2[num][x])
plt.xlabel('페이지')
plt.ylabel('감정 레벨')

# 그래프 출력
plt.show()
book.close()
