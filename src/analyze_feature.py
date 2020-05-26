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
        if 'NNG' in token[1]:   # 대명사
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
def analyze_feature(feature ,genre, fileName, word_dic, total_count):
    book = open(f'../res/book/{feature}/{genre}/{fileName}.txt', "r", encoding='utf-8', errors='ignore')
    context = preprocess.remove_etc(book)
    word_dic, total = count(context, word_dic, total_count)

    print(f'{fileName} 완료')
    book.close()
    return word_dic, total

'''
### 장르
dict_detective = {}
dict_romance = {}
feature = "genre"
total_count = 0

############# 장르
# 데이터프레임 컬럼: 단어, 등장 횟수, 등장 비율

# 추리 소설 분석 및 데이터프레임으로 저장
for num in range(1, 69):
    fileName = f"detective{num}"
    # 단어 빈도 계산
    dict_detective, total_count = analyze_feature(feature, "detective", fileName, dict_detective, total_count)

# 단어 비율 계산하여 칼럼 추가 후 데이터 프레임으로 변환
df_detective = make_dataframe(dict_detective, total_count)

# 데이터 프레임 출력
create.save_df(df_detective, "detective")
'''


####### 시대
dict_joseon = {}
dict_ilje = {}
dict_modern = {}
total_count =0
feature = "generation"
# 조선시대 소설 분석 및 데이터프레임으로 저장
for num in range(0, 2432):
    fileName = f"조선왕조실록{num}"
    # 단어 빈도 계산
    dict_joseon, total_count = analyze_feature(feature, "joseon", fileName, dict_joseon, total_count)

# 단어 비율 계산하여 칼럼 추가 후 데이터 프레임으로 변환
df_joseon = make_dataframe(dict_joseon, total_count)

# 데이터 프레임 출력
create.save_df(df_joseon, "joseon")

