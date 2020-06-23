import sys
import create
import preprocess
import result
import analyze
import morphs
import emotion_word
import math
import pandas as pd
import noun_ex
from matplotlib import pyplot as plt

sys.stdout.reconfigure(encoding='utf-8')
pd.set_option('mode.chained_assignment', None)


def main(fileName, name):
    book = open(f'../web/upload/{fileName}', "rt",
                encoding='UTF8', errors='ignore')
    # 전처리
    context = preprocess.remove_etc(book)

    # 변수 선언
    # charOfPage = 700
    charOfPage = len(context) / 20
    listOfEmotion = ['기쁨', '슬픔', '분노', '공포', '혐오', '놀람']
    numOfEmotion = len(listOfEmotion)
    numOfPage = math.ceil(len(context) / charOfPage)
    listOfCharacter = []

    name_str = name.split(',')
    for name in name_str:
        listOfCharacter.append(name)

    numOfCharacter = len(listOfCharacter)

    # 사용자 사전 생성
    create.create_userdic(listOfCharacter)

    # 문장 데이터프레임 생성
    df_sentence = create.create_sentence_dataframe(context, listOfEmotion)
    create.save_df(df_sentence, fileName)

    # 명사 추출
    # noun_ex.noun_extract(df)

    # emotion_word.emotion_lemmatization()

    # 감정 사전 생성
    # emotion_dictionary_lists = emotion_word.create_emotion_dictionary()

    # 구축되어 있는 감정 사전 데이터 프레임 오픈
    df_emotion = emotion_word.open_emotion_dataframe()

    # 문장 분석
    df_sentence = analyze.analyze_sentence(
        df_sentence, listOfCharacter, df_emotion, charOfPage)
    create.save_df(df_sentence, fileName)

    # 등장인물 별 페이지 감정 점수 합산하여 등장인물 데이터프레임 생성
    df_list_character = analyze.merge_character(
        df_sentence, listOfEmotion, listOfCharacter)
    df_list_character_by_page = analyze.merge_character_page(df_sentence, numOfPage, listOfEmotion, listOfCharacter)

    # 20 문장 당 x축 사이즈 = 1
    # 그래프 설정
    x_size = len(df_sentence.index) / 20 + 1
    result.config_graph(x_size)

    # 결과 1. 각 등장인물의 페이지별 감정 수준 그래프 생성 및 출력
    fig_html_list = result.display_emotion_graph(
        df_list_character, listOfCharacter, numOfCharacter, listOfEmotion)

    fig_html_page_list = result.display_emotion_graph(
        df_list_character_by_page, listOfCharacter, numOfCharacter, listOfEmotion)

    # 결과 2. 각 등장인물의 주요 감정
    emo_list = result.display_main_emo(df_list_character_by_page, numOfCharacter, listOfEmotion)

    # 결과 3. 각 등장인물의 감정 비율
    ratio_list = result.display_emo_ratio(df_sentence, listOfCharacter, numOfCharacter, listOfEmotion)


    # 결과 소설 정보, 등장인물 정보 및 html 출력하여 콜백
    # 1. 등장인물의 주요 감정 및 감정 비율
    for num in range(0, numOfCharacter):
        print(f'{listOfCharacter[num]}의 감정 비율 : {ratio_list[num]}')

    # 2. 등장인물 데이터프레임 및 감정 그래프 출력
    for num in range(0, numOfCharacter):
        print(df_list_character[num].to_html(justify='center'))
        print(fig_html_list[num])
        print(fig_html_page_list[num])

    # 3.문장 데이터 프레임 출력
    sentence_html = df_sentence.to_html(justify='center')
    print(sentence_html)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
