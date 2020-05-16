import konlpy
import nltk

from konlpy.tag import Komoran
komoran = Komoran()

context = u'사흘 전부터 설렁탕 국물이 마시고 싶다고 남편을 졸랐다.'
words = komoran.pos(context)

# 구문 분석 규칙 정의
# 보어 -> 주어로 나오는 문제 수정 필요
# 대화체에서 조사가 생략되면 구문 분석이 어려워짐
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

parser = nltk.RegexpParser(grammar)
chunks = parser.parse(words)

print(chunks.pprint())

for subTree in chunks.subtrees():
    if subTree.label() == "주어":
        print(subTree)