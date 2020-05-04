# -*- coding: utf-8 -*-

from konlpy.tag import Komoran

kom=Komoran(userdic='userDic.txt')

listOfCharacter = ["김첨지","치삼이","개똥이"] # test

f=open('../res/book/test1.txt', 'r', encoding='UTF8')

for line in f:
    if len(line) > 1: # 추후 엔터 제거 전처리 적용 예정
        line = line.strip('\n')
        tokenList=kom.pos(line)
        print(tokenList)
        #print(len(tokenList))
        """for i in tokenList:
            for j in listOfCharacter:
                if tokenList[i][0] == listOfCharacter[j]:"""
        for i in tokenList:
            if i[1] == 'NNP':  # 등장인물 선별 위해 고유명사 체크
                tempList = i[0]
        for i in tempList:
            for j in listOfCharacter:
                if i == j: # 등장인물이 있으면
                    print(i)
                    # 해당문장에 대한 감정분석

        print('\n')
f.close()

