# -*- coding: utf-8 -*-

from konlpy.tag import Komoran

komoran = Komoran(userdic='user_dic.txt')

print(komoran.nouns('최윤호가 김우용, 박종근이랑'))
print(komoran.pos('최윤호가 김우용, 박종근이랑'))

'''f = open('res/book/test.txt', 'r', encoding='UTF8')

for line in f:
    if len(line) > 1:
        line = line.strip('\n')
        print(Komoran().pos(line))  # 품사 태깅
        print(Komoran().morphs(line))  # 형태소만 추출
        print(Komoran().nouns(line))  # 명사 추출
        print('\n')
f.close()'''