import numpy as np
<<<<<<< .merge_file_xakkt8
import mpld3
import jinja2
from matplotlib import pyplot as plt
from matplotlib import font_manager as fm

=======
from matplotlib import pyplot as plt
from matplotlib import font_manager as fm


>>>>>>> .merge_file_odb4Al
def config_graph(x_size):
    fontprop = fm.FontProperties(fname="../res/fonts/malgun.ttf", size=24).get_name()
    plt.rc('font', family=fontprop)
    print(x_size)
    plt.rcParams['figure.figsize'] = (x_size, 6)
    plt.rcParams['axes.unicode_minus'] = False


# 결과 1. 각 등장인물의 페이지별 감정 수준
# 등장인물 별 그래프 생성 및 페이지별 감정 레벨 값 대입
<<<<<<< .merge_file_xakkt8
def display_emotion_graph(df_list_character, listOfCharacter, numOfCharacter, listOfEmotion):
=======
def display_emotion_graph(df_list_character, df_list_character_by_page, listOfCharacter, numOfCharacter, listOfEmotion):
>>>>>>> .merge_file_odb4Al
    for num in range(0, numOfCharacter):

        x = np.arange(0, len(df_list_character[num].index))
        f = plt.figure()
        df = df_list_character[num]
        #
        for emo in listOfEmotion:
            plt.plot(x, df[f'{emo}'], label=f'{emo}')
        plt.title(f'{listOfCharacter[num]}')
<<<<<<< .merge_file_xakkt8
        # plt.xlabel('페이지')
=======
>>>>>>> .merge_file_odb4Al
        plt.xlabel('문장')
        plt.ylabel('감정 값')
        plt.legend(loc='upper right')
        plt.grid(color='gray', dashes=(2, 2))
        plt.show()
<<<<<<< .merge_file_xakkt8
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
=======

        x = np.arange(0, len(df_list_character_by_page[num].index))
        df = df_list_character_by_page[num]
        #
        for emo in listOfEmotion:
            plt.plot(x, df[f'{emo}'], label=f'{emo}')
        plt.title(f'{listOfCharacter[num]}')
        plt.xlabel('페이지')
        plt.ylabel('감정 값')
        plt.legend(loc='upper right')
        plt.grid(color='gray', dashes=(2, 2))
        plt.show()


# 결과 2. 소설 장르, 시대적 배경 파악

# 결과 3. 등장인물의 주요 감정 파악
def display_main_emo(df_list_character_by_page, numOfCharacter, listOfEmotion):
    main_emo_list = []
    main_emo = ""
    i = -1
    for num in range(0, numOfCharacter):
        df = df_list_character_by_page[num]
        for emo in listOfEmotion:
            if df[f'{emo}'].sum() > i:
                main_emo = emo
                i = df[f'{emo}'].sum()
        main_emo_list.append(main_emo)
        return main_emo_list


def display_emo_ratio(df_sentence, listOfCharacter, numOfCharacter, listOfEmotion):

    listOfRatio = []
    # 화자 필터링
    for character in listOfCharacter:
        li = []
        m1 = df_sentence['화자'] == character
        filtered_df = df_sentence.loc[m1]
        filtered_df = filtered_df.loc[:, ('기쁨', '슬픔', '분노', '공포', '혐오', '놀람')]  # 추출한 행들의 감정 열 추출
        for emo in listOfEmotion:
            count = 0
            s_emo = filtered_df[emo]  # 시리즈 추출
            for v in s_emo.values:
                if v > 0:
                    count = count + 1
            li.append(count / len(filtered_df.index))  # 감정 비율 추가
        count = 0
        emo_s = filtered_df.sum(axis=1)  # 행 합의 시리즈
        for s in emo_s:
            if s == 0:
                count = count + 1
        li.append(count/len(filtered_df.index))
        listOfRatio.append(li)  # 캐릭터 리스트에 추가
    return listOfRatio


>>>>>>> .merge_file_odb4Al
