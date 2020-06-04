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
    if token[1] == 'VA' or token[1] == 'VV':
        return token[0] + '다'
    else:
        return ""

# def lemma_candidate(l, r, predefined=None, debug=False):
#     def add_lemma(stem, ending):
#         candidates.add((stem, ending))
#
#     candidates = {(l, r)}
#     word = l + r
#
#     l_last = decompose(l[-1])
#     l_last_ = compose(l_last[0], l_last[1], ' ')
#     l_front = l[:-1]
#     r_first = decompose(r[0]) if r else ('', '', '')
#     r_first_ = compose(r_first[0], r_first[1], ' ') if r else ' '
#     r_end = r[1:]
#
#     # ㄷ 불규칙 활용: 깨달 + 아 -> 깨닫 + 아
#     if l_last[2] == 'ㄹ' and r_first[0] == 'ㅇ':
#         l_stem = l_front + compose(l_last[0], l_last[1], 'ㄷ')
#         add_lemma(l_stem, r)
#         if debug:
#             debug_message('ㄷ 불규칙 활용', l_stem, r)
#
#     # 르 불규칙 활용: 굴 + 러 -> 구르 + 어
#     if (l_last[2] == 'ㄹ') and (r_first_ == '러' or r_first_ == '라'):
#         l_stem = l_front + compose(l_last[0], l_last[1], ' ') + '르'
#         r_canon = compose('ㅇ', r_first[1], r_first[2]) + r_end
#         add_lemma(l_stem, r_canon)
#         if debug:
#             debug_message('르 불규칙 활용', l_stem, r_canon)
#
#     # ㅂ 불규칙 활용: 더러 + 워서 -> 더럽 + 어서
#     if (l_last[2] == ' '):
#         l_stem = l_front + compose(l_last[0], l_last[1], 'ㅂ')
#         if (r_first_ == '워' or r_first_ == '와'):
#             r_canon = compose('ㅇ', 'ㅏ' if r_first_ == '와' else 'ㅓ', r_first[2] if r_first[2] else ' ') + r_end
#         elif (r_end and r_end[0] =='려'):
#             r_canon = compose('ㅇ', 'ㅜ', r_first[2] if r_first[2] else ' ') + r_end
#         else:
#             r_canon = r
#         add_lemma(l_stem, r_canon)
#         if debug:
#             debug_message('ㅂ 불규칙 활용', l_stem, r_canon)
