import numpy as np
from matplotlib import pyplot as plt
from matplotlib import font_manager as fm

def config_graph():
    fontprop = fm.FontProperties(fname="../res/fonts/malgun.ttf", size=24).get_name()
    plt.rc('font', family=fontprop)
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['axes.unicode_minus'] = False


# 결과 1. 각 등장인물의 페이지별 감정 수준
# 등장인물 별 그래프 생성 및 페이지별 감정 레벨 값 대입
def display_emotion_graph(df_list_character, listOfCharacter, numOfCharacter):

    for num in range(0, numOfCharacter):
        df_list_character[0].plot()
        plt.title(f'{listOfCharacter[num]}')
        # plt.xlabel('페이지')
        plt.xlabel('문장')
        plt.ylabel('감정 값')
        plt.legend(loc='upper right')
        plt.grid(color='gray', dashes=(2, 2))
        plt.show()

# 결과 2. 모든 등장인물의 페이지별 감정 흐름
# 그래프 생성 및 등장인물 별 감정 흐름 값 대입
def display_sentiment_graph(numOfCharacter, listOfCharacter, numOfPage, sentimentVector):
    x = np.arange(1, numOfPage)

    plt.figure(numOfCharacter)
    plt.title("등장인물 별 감정 흐름")
    plt.xlabel('페이지')
    plt.ylabel('감정 레벨')
    for num in range(0, numOfCharacter):
        plt.plot(x, sentimentVector[num][x], label=listOfCharacter[num])

    plt.legend()