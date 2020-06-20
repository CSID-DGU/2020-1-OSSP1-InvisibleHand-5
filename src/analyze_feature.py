import preprocess
import pandas as pd
from konlpy.tag import Komoran

# from google.cloud import translate_v3beta1 as translate

kom = Komoran()


# # 구글 번역 api
# def translate_text(text, project_id="project_id"):
#     """Translating Text."""
#
#     client = translate.TranslationServiceClient()
#
#     parent = client.location_path(project_id, "global")
#
#     # Detail on supported types can be found here:
#     # https://cloud.google.com/translate/docs/supported-formats
#     response = client.translate_text(
#         parent=parent,
#         contents=[text],
#         mime_type="text/plain",  # mime types: text/plain, text/html
#         source_language_code="en-US",
#         target_language_code="ko",
#     )
#     # Display the translation for each input text provided
#     for translation in response.translations:
#         trans = translation.translated_text
#     return trans


# # 개체명(직업) 사전 구축
# def create_occupation_dataframe:
#     book = open("filepath", "rt", encoding='UTF8', errors='ignore')
#
#     line = book.readline()
#     total = ""
#     trans_list = []
#     occu_list = []
#     count = 0
#     while line:
#         if count > 49:
#             trans_data = translate_text(total)
#             print(trans_data.split("\n"))
#             for trans in trans_data.split("\n"):
#                 if trans != '':
#                     trans_list.append(trans)
#             total = ""
#             count = 0
#             print(len(trans_list))
#         line = line.replace("http://dbpedia.org/resource/", "")
#         line = line.replace("_", " ")
#         occu_list.append(line)
#         total += line
#         count += 1
#         line = book.readline()
#
#     trans_data = translate_text(total)
#     print(trans_data.split("\n"))
#     for trans in trans_data.split("\n"):
#         if trans != '':
#             trans_list.append(trans)
#
#     df = pd.DataFrame(occu_list, columns=['직업'])
#     df['번역'] = pd.Series(trans_list, index=df.index)
#     df.to_excel(f"../res/dic/occupation.xlsx")
#     return 0


def save_df(feature, df, fileName):
    df.to_excel(f"../res/feature/{feature}/{fileName}.xlsx")


# 장르 딕셔너리를 데이터프레임으로 변환 및 출력
def make_dataframe(word_dic, total):
    df = pd.DataFrame.from_dict(word_dic, orient='index', columns=['count'])
    df.index.names = ['word']
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
    save_df("genre", df, f'{genre}')
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
    save_df("generation", df, f'{generation}')
    return 0


# 각 특징 별 공통된 단어 데이터프레임 생성
def analyze_common():
    # 장르
    detective_df = pd.read_excel('../res/feature/genre/detective.xlsx')  # 추리
    romance_df = pd.read_excel('../res/feature/genre/romance.xlsx')  # 로맨스

    # 시대
    joseon_df = pd.read_excel('../res/feature/generation/joseon.xlsx')  # 조선시대
    bloom_df = pd.read_excel('../res/feature/generation/bloom.xlsx')  # 개화기
    # bloom_df = pd.read_excel('../res/feature/generation/bloom.xlsx')  # 일제 강점기

    genre_common_df = pd.merge(detective_df, romance_df, how='inner', on=['word'])
    generation_common_df = pd.merge(joseon_df, bloom_df, how='inner', on=['word'])

    save_df("genre", genre_common_df, 'common')
    save_df("generation", generation_common_df, 'common')


# 원 데이터 프레임에서 공통된 데이터 프레임 sub
def exclude_common():
    # 장르
    common_genre_df = pd.read_excel('../res/feature/genre/common.xlsx')  # 장르 공통
    detective_df = pd.read_excel('../res/feature/genre/detective.xlsx')  # 추리
    romance_df = pd.read_excel('../res/feature/genre/romance.xlsx')  # 로맨스

    # 시대
    common_generation_df = pd.read_excel('../res/feature/generation/common.xlsx')  # 시대 공통
    joseon_df = pd.read_excel('../res/feature/generation/joseon.xlsx')  # 조선시대
    bloom_df = pd.read_excel('../res/feature/generation/bloom.xlsx')  # 개화기
    # ilje_df = pd.read_excel('../res/feature/generation/ilje.xlsx')  # 일제 강점기

    # 장르 공통 제외
    detective_only_df = detective_df[~detective_df['word'].isin(common_genre_df['word'])]
    romance_only_df = romance_df[~romance_df['word'].isin(common_genre_df['word'])]

    bloom_only_df = bloom_df[~bloom_df['word'].isin(common_generation_df['word'])]
    joseon_only_df = joseon_df[~joseon_df['word'].isin(common_generation_df['word'])]

    # 출력
    save_df("genre", detective_only_df, 'detective_only')
    save_df("genre", romance_only_df, 'romance_only')

    save_df("generation", bloom_only_df, 'bloom_only')
    save_df("generation", joseon_only_df, 'joseon_only')


def analyze_feature():
    #   analyze_genre("detective", "detective", 69)  # 추리 소설
    #   analyze_genre("romance", "romance", 8)  # 로맨스 소설

    #   analyze_generation("joseon", "조선왕조실록", 2432)  # 조선 시대
    #   analyze_generation("bloom", "bloom", 102)  # 개화기 시대
    #   analyze_generation("ilje", "ilje", 15)  # 일제 시대
    return 0

# analyze_common()
# exclude_common()
