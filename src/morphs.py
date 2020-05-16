# -*- coding: utf-8 -*-

from konlpy.tag import Komoran
import nltk
import create
import pandas as pd

kom = Komoran(userdic='user_dic.txt')  # 사용자 사전 적용
grammar = '''
# 체언 = 명사/대명사/수사(NN*/NP/NR)
# 주어 = 체언 + 주격 조사/보조사(JKS/JX)
주어: {<N.*>+<JKS>}
주어: {<N.*>+<JX>}
# 서술어 = 동사/형용사(VV/VA) + 어미(E)
# 체언 + 서술격조사(VCP/VCN) -> komoran에선 지정사 VC
서술어: {<V.*><E.*>+}
서술어: {<N.*>+<VC>}
# 보어 = 체언 + 주격/보격 조사(JKS/JKC) + 되다/아니다
#       -> 보격 조사가 대부분 주격 조사로 나오므로 주격 조사를 포함. 주어와 구분 필요
보어: {<N.*>+<JKS>?<JX>?<VCN>}
보어: {<N.*>+<JKS>?<JX>?<VV><EP><EC>}
# 목적어 = 체언 + 목적격 조사/보조사(JKO/JX) + (부사) + 타동사
#         -> 보조사가 붙을 때 주어와 구분짓기 위해 조건이 더 필요함
목적어: {<N.*>+<JKO>}
# 부사어 = 부사(MAG/MAJ)
# 체언 + 부사격 조사(JKB)
#         동사/형용사(VV/VA) + 부사형 어미(EC)
#         -> komoran에 부사형 어미 존재X, 연결어미(EC)로 출력됨. 서술어와 구분 필요
부사어: {<MA.*>}
부사어: {<N.*>+<JKB>+<JX>}
부사어: {<V.*><EC>}                                             
# 관형어 = 관형사(MM)
#         체언 + 관형격 조사(JKG)
#         동사/형용사(VV/VA) + 관형사형 어미(ETM)
관형어: {<MM>}
관형어: {<N.*>+<JKG>}
관형어: {<V.*><ETM>}
# 독립어 = 감탄사(IC)
#         체언 + 호격 조사(JKV)
#         접속 부사(MAJ) -> 부사어와 구분이 필요 ex) '. 그리고', '. 그러나'
독립어: {<IC>}
독립어: {<N.*>+<JKV>}
독립어: {<SF>+<MAJ>}
'''

# 감정 사전에서 단어 찾기
def find_word(emotion_dictionary_lists, token):
    for emo in emotion_dictionary_lists:
        if token[0] in emo.keys():
            return emo[token[0]]
    return -1, 0  # 단어사전에 없었다면


def analyze_speaker(df, listOfCharacter, emotion_dictionary_lists, charOfPage):
    subject = []
    object = []
    character = []
    page = 0
    length = 0
    index = 0
    for line in df["문장"]:
        if(length > charOfPage):
            page = page + 1
            length = 0
        length = length + len(line)
        token_list = kom.pos(line)
        su = []
        ob = []
        ch = []
        wo = []
        count = [0 for i in range(len(listOfCharacter))]  # 문장 당 등장인물의 출현 횟
        for token in token_list:
            if 'SW' in token[1]:  # 기타 기호 삭제
                token_list.remove(token)
            if 'NA' in token[1]:  # 분석불능범주 삭제
                token_list.remove(token)
            if 'SH' in token[1]:  # 한자 삭제
                token_list.remove(token)
            if token[0] in listOfCharacter:  # 문장에서의 등장인물 등장 체크
                count[listOfCharacter.index(token[0])] += 1
            word_result = find_word(emotion_dictionary_lists, token)
            if word_result != (-1, 0):  # 문장에서 단어 사전에 있는 단어가 있다면
                wo.append(token[0])
                df.at[index, f"{word_result[0]}"] += float(word_result[1])

        for i, c in enumerate(count):
            if c >= 1:
                ch.append([listOfCharacter[i], str(c)])

        parser = nltk.RegexpParser(grammar)
        chunks = parser.parse(token_list)

        for sub_tree in chunks.subtrees():
            if sub_tree.label() == "주어":
                su.append(sub_tree[0][0])
            elif sub_tree.label() == "목적어":
                ob.append(sub_tree[0][0])
        subject.append(su)
        object.append(ob)
        character.append(ch)
        df.at[index, "페이지 번호"] = page
        df.at[index, "감정 단어"] = wo
        index = index + 1
    df['주어'] = pd.Series(subject, index=df.index)
    df['목적어'] = pd.Series(object, index=df.index)
    df['화자'] = pd.Series(character, index=df.index)

    return df
