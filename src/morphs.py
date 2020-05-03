# -*- coding: utf-8 -*-

from konlpy.tag import Komoran

kom=Komoran(userdic='userDic.txt')


f=open('../res/book/test1.txt', 'r', encoding='UTF8')

for line in f:
    if len(line) > 1: # 추후 엔터 제거 전처리 적용 예정
        line = line.strip('\n')
        print(kom.pos(line))
        print('\n')
f.close()