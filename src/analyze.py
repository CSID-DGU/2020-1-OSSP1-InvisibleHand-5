import konlpy
import nltk
from konlpy.tag import Komoran


# 감정 사전에서 단어 찾기
def find_word(emotion_dictionary_lists, words):
    for w in words:
        for emo in emotion_dictionary_lists:
            if w[0] in emo.keys():
                return emo[w[0]]
    return -1, 0  # 단어사전에 없었다면


def find_character(words, listOfCharacter):
    grammar = '''
# 체언 = 명사/대명사/수사(NN*/NP/NR)

# 주어 = 체언 + 주격 조사/보조사(JKS/JX)
주어: {<N.*>+<JKS>}
주어: {<N.*>+<JX>}

# 서술어 = 동사/형용사(VV/VA) + 어미(E)
#         체언 + 서술격조사(VCP/VCN) -> komoran에선 지정사 VC
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
#         체언 + 부사격 조사(JKB)
#         동사/형용사(VV/VA) + 부사형 어미(EC)
#         -> komoran에 부사형 어미 존재X, 연결어미(EC)로 출력됨. 서술어와 구분 필요
부사어: {<MA.*>}
부사어: {<N.*>+<JKB>}
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
    parser = nltk.RegexpParser(grammar)
    chunks = parser.parse(words)

    for subtree in chunks.subtrees():
        if subtree.label() == '주어':
            for e in list(subtree):
                if (e[0] in listOfCharacter):  # 등장인물이라면
                    print(listOfCharacter.index(e[0]))
                    return listOfCharacter.index(e[0])
    return -1  # 아니라면


def analyze_text(numOfPage, charOfPage, emotion_dictionary_lists, emotionVector, listOfCharacter):
    komoran = Komoran()

    context = u'그의 아내는 살인자이다.'
    words = komoran.pos(context)


    count = 0
    for page in range(0, numOfPage):  # 페이지 수 만큼
        count += len(context)  # 문장 길이 만큼 count 증가
        word_result = find_word(emotion_dictionary_lists, words)
        print(word_result)
        if word_result != (-1, 0):  # 문장에서 단어 사전에 있는 단어가 있다면
            if word_result[0] == 'joy':
                emotion = 0
            elif word_result[0] == 'sadness':
                emotion = 1
            elif word_result[0] == 'anger':
                emotion = 2
            elif word_result[0] == 'fear':
                emotion = 3
            elif word_result[0] == 'disgust':
                emotion = 4
            elif word_result[0] == 'surprise':
                emotion = 5
            score = float(word_result[1])
            print(score)
            # 주어가 등장인물일 경우
            num = find_character(words, listOfCharacter)
            if num != -1:
                emotionVector[num][emotion][page] += score  # 값 증가
        if count > charOfPage:  # 페이지 넘기기
            page += 1
            count = 0

    print(emotionVector)
    return emotionVector
