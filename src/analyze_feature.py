import create
import preprocess
import nltk
import pandas as pd
from konlpy.tag import Komoran

kom = Komoran()


# 장르 딕셔너리를 데이터프레임으로 변환 및 출력
def make_dataframe(word_dic, total):
    df = pd.DataFrame.from_dict(word_dic, orient='index', columns=['count'])

    # 등장 비율 칼럼 추가
    df['percentage'] = df['count'] / total

    df = df.sort_values(by='count', ascending=False)
    return df


# 단어 등장 회수 카운트
def count(context, word_dic, total_count):
    token_list = kom.pos(context)
    for i, token in enumerate(token_list):
        total_count = total_count + 1
        if 'NNG' in token[1]:  # 대명사
            if token in word_dic:
                word_dic[token] = word_dic.get(token, 0) + 1
            else:
                word_dic[token] = 1
        if 'NNP' in token[1]:  # 고유 명사
            if token in word_dic:
                word_dic[token] = word_dic.get(token, 0) + 1
            else:
                word_dic[token] = 1
        if 'VA' in token[1]:  # 형용사
            if token in word_dic:
                word_dic[token] = word_dic.get(token, 0) + 1
            else:
                word_dic[token] = 1
        if 'VV' in token[1]:  # 동사
            if token in word_dic:
                word_dic[token] = word_dic.get(token, 0) + 1
            else:
                word_dic[token] = 1
    return word_dic, total_count


# 장르 소설 분석
def analyze_genre(genre, fileName, book_count):
    dict_genre = {}
    total_count = 0
    for num in range(1, book_count):
        book = open(f'../res/book/genre/{genre}/{fileName}{num}.txt', "r", encoding='utf-8', errors='ignore')
        context = preprocess.remove_etc(book)
        dict_genre, total_count = count(context, dict_genre, total_count)

        print(f'{fileName}{num} 완료')
        book.close()

    # 단어 비율 계산하여 칼럼 추가 후 데이터 프레임으로 변환
    df = make_dataframe(dict_genre, total_count)

    # 데이터 프레임 출력
    create.save_df(df, f'{genre}')
    return 0


def analyze_generation(generation, fileName, book_count):
    dict_generation = {}
    total_count = 0
    for num in range(1, book_count):
        book = open(f'../res/book/generation/{generation}/{fileName}{num}.txt', "r", encoding='utf-8', errors='ignore')
        context = preprocess.remove_etc(book)
        dict_genre, total_count = count(context, dict_generation, total_count)

        print(f'{fileName}{num} 완료')
        book.close()

    # 단어 비율 계산하여 칼럼 추가 후 데이터 프레임으로 변환
    df = make_dataframe(dict_generation, total_count)

    # 데이터 프레임 출력
    create.save_df(df, f'{generation}')
    return 0


def analyze_feature():
    #   analyze_genre("detective", "detective", dict_detective, total_count, 69)
    #   analyze_generation("joseon", "조선왕조실록", dict_detective, total_count, 2432)
    #   analyze_genre("romance", "romance", 8)
    pass