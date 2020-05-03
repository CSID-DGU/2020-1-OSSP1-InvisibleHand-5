# -*- coding: utf-8 -*-

from konlpy.tag import Komoran

komoran = Komoran(userdic='user_dic.txt')

f = open('res/book/운수좋은날.txt', 'r', encoding='UTF8')

for line in f:
    if len(line) > 1:
        line = line.strip('\n')
        print(Komoran().pos(line))  # 품사 태깅
        print('\n')
f.close()