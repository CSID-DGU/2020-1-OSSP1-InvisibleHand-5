# -*- coding: utf-8 -*-

from konlpy.tag import Komoran
import os

if not os.path.isfile('user_dic.txt'):
    open("user_dic.txt", "wt", encoding='UTF8')
kom = Komoran(userdic='user_dic.txt')  # 사용자 사전 적용

# 형태소 분석
def tokenizer(line):
    token_list = kom.pos(line)
    for i, token in enumerate(token_list):
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
    #string = "손에 쥔 피"

    #print(token_list)

    return token_list

def _add_inter_subtokens(self, token, result):
    adds = []
    for i, base in enumerate(result[:-1]):
        if base[2] == result[i + 1][1]:
            continue

        b = base[2]
        e = result[i + 1][1]
        subtoken = token[b:e]
        adds.append((subtoken, b, e, self._ds, e - b))

    return adds

def _add_first_subtoken(self, token, result):
    e = result[0][1]
    subtoken = token[0:e]
    score = self._scores.get(subtoken, self._ds)
    return [(subtoken, 0, e, score, e)]

def _add_last_subtoken(self, token, result):
    b = result[-1][2]
    subtoken = token[b:]
    score = self._scores.get(subtoken, self._ds)
    return [(subtoken, b, len(token), score, len(subtoken))]

def _max_length_l_tokenize(self, token):

    def nouns_to_larray_and_r(token, nouns_):
        e = sum((len(noun) for noun in nouns_))
        return nouns_, token[e:]

    nouns = []
    n = len(token)

    # string match for generating candidats
    for b in range(n):
        for e in range(b, n + 1):
            subword = token[b:e]
            if subword in self._nouns:
                # (word, begin, length)
                nouns.append((subword, b, e - b))

    # sort. fisrt order: begin index, second order: length (desc)
    nouns = sorted(nouns, key=lambda x: (x[1], -x[2]))

    nouns_ = []
    e = 0
    return nouns_to_larray_and_r(token, nouns_)


def tokenize_(self, sentence, tolerance=0.0, flatten=True, remove_r=False):

    tokens = [token_to_lr(token, tolerance) for token in sentence.split()]

    if remove_r:
        tokens = [token[0] for token in tokens]

    if (flatten) and (remove_r == False):
        tokens = [subtoken for token in tokens for subtoken in token if subtoken]

    return tokens