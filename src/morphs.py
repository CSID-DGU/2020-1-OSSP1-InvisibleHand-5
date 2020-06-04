# -*- coding: utf-8 -*-

from konlpy.tag import Komoran
import os

if not os.path.isfile('user_dic.txt'):
    open("user_dic.txt", "wt", encoding='UTF8')
kom = Komoran(userdic='user_dic.txt')  # 사용자 사전 적용

# 형태소 분석
def tokenizer(line):
    test = "젠장"
    #print(kom.pos(test))
    token_list = kom.pos(line)
    #print(token_list)
    for i, token in enumerate(token_list):
        #print(token)
        if 'SW' in token[1]:  # 기타 기호 삭제
            token_list.remove(token)
        if 'NA' in token[1]:  # 분석불능범주 삭제
            token_list.remove(token)
        if 'SH' in token[1]:  # 한자 삭제
            token_list.remove(token)
        if token[1] == 'NP' and token[0] == '그':
            if token_list[i+1][0] == 'ㄴ' and token_list[i+1][1] == 'JX':
                del token_list[i]
                del token_list[i]
                token_list.insert(i,('근','MM'))
    #print("")
    return token_list

#Lemmatization
def lemmatize_token(token):
    if token[1] == 'VA' or token[1] == 'VV':
        return token[0] + '다'

def lemmatize_word(word):
    token = kom.pos(word)
    print(token)
    if token[0][1] == 'VA' or token[0][1] == 'VV':
        return token[0][0] + '다'
    else:
        return ""
