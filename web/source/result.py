import numpy as np
import mpld3
import jinja2
from matplotlib import pyplot as plt
from matplotlib import font_manager as fm
import matplotlib
matplotlib.use('Agg')


def config_graph():
    fontprop = fm.FontProperties(
        fname="res/fonts/malgun.ttf", size=24).get_name()
    plt.rc('font', family=fontprop)
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['axes.unicode_minus'] = False


# 결과 1. 각 등장인물의 페이지별 감정 수준
# 등장인물 별 그래프 생성 및 페이지별 감정 레벨 값 대입
def display_emotion_graph(df_list_character, listOfCharacter, numOfCharacter, listOfEmotion):
    fig_list = []

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
        # html 결과 출력부
        # print 내용 콜백
        fig_list.append(mpld3.fig_to_html(f, figid=f"character{num}"))

    return fig_list


def display_emotion_graph_page(df_list_character_by_page, listOfCharacter, numOfCharacter, listOfEmotion):
    fig_page_list = []

    for num in range(0, numOfCharacter):
        x = np.arange(0, len(df_list_character_by_page[num].index+1))
        f = plt.figure()
        df = df_list_character_by_page[num]

        for emo in listOfEmotion:
            plt.plot(x, df[f'{emo}'], label=f'{emo}')
        plt.title(f'{listOfCharacter[num]}')
        plt.xlabel('페이지')
        plt.ylabel('감정 값')
        plt.legend(loc='upper right')
        plt.grid(color='gray', dashes=(2, 2))
        # html 결과 출력부
        # print 내용 콜백
        fig_page_list.append(mpld3.fig_to_html(
            f, figid=f"character{num}_page"))

    return fig_page_list


# 결과 2. 등장인물의 주요 감정 파악
def display_main_emo(df_list_character_by_page, numOfCharacter, listOfEmotion):
    main_emo_list = []
    main_emo = ""

    for num in range(0, numOfCharacter):
        i = -1
        df = df_list_character_by_page[num]
        for emo in listOfEmotion:
            if df[f'{emo}'].sum() > i:
                main_emo = emo
                i = df[f'{emo}'].sum()
        main_emo_list.append(main_emo)
    return main_emo_list


# 결과 3. 각 등장인물의 감정 비율
def display_emo_ratio(df_sentence, listOfCharacter, numOfCharacter, listOfEmotion):
    listOfRatio = []
    # 화자 필터링
    for character in listOfCharacter:
        li = []
        m1 = df_sentence['화자'] == character
        filtered_df = df_sentence.loc[m1]
        # 추출한 행들의 감정 열 추출
        filtered_df = filtered_df.loc[:, ('기쁨', '슬픔', '분노', '공포', '혐오', '놀람')]
        len_sentence = len(filtered_df.index)

        for emo in listOfEmotion:
            count = 0
            s_emo = filtered_df[emo]  # 시리즈 추출
            for v in s_emo.values:
                if v > 0:
                    count = count + 1
            # 감정 비율 추가
            if len_sentence > 0:
                li.append(round(count / len_sentence * 100, 2))  # 감정 비율 추가
        listOfRatio.append(li)  # 캐릭터 리스트에 추가
    return listOfRatio
