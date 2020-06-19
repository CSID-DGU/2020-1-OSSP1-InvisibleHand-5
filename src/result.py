import numpy as np
import mpld3
import jinja2
from matplotlib import pyplot as plt
from matplotlib import font_manager as fm

def config_graph(x_size):
    fontprop = fm.FontProperties(fname="../res/fonts/malgun.ttf", size=24).get_name()
    plt.rc('font', family=fontprop)
    print(x_size)
    plt.rcParams['figure.figsize'] = (x_size, 6)
    plt.rcParams['axes.unicode_minus'] = False


# 결과 1. 각 등장인물의 페이지별 감정 수준
# 등장인물 별 그래프 생성 및 페이지별 감정 레벨 값 대입
def display_emotion_graph(df_list_character, listOfCharacter, numOfCharacter, listOfEmotion):
    for num in range(0, numOfCharacter):

        x = np.arange(0, len(df_list_character[num].index))
        f = plt.figure()
        df = df_list_character[num]
        #
        for emo in listOfEmotion:
            plt.plot(x, df[f'{emo}'], label=f'{emo}')
        plt.title(f'{listOfCharacter[num]}')
        # plt.xlabel('페이지')
        plt.xlabel('문장')
        plt.ylabel('감정 값')
        plt.legend(loc='upper right')
        plt.grid(color='gray', dashes=(2, 2))
        plt.show()
    #print("test")
    #mpld3.fig_to_html(f, 'C:\\Users\\whdrm\\Desktop\\figure.html')

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