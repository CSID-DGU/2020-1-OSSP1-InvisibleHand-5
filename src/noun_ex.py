from collections import defaultdict

count = defaultdict(lambda: 0)

# 명사 점수 계
# def n_score(w):
#     return pow(count[w]/count[w[0]],1/(len(w)-1))

def noun_extract(df):
    # for line in df["문장"]:
    #     for word in line.split():
    #         n = len(word)
    #         for e in range(1, n+1):
    #             count[word[:e]] += 1

    for line in df["문장"]:
        for word in line.split():
            count[word] += 1

    for line in df["문장"]:
        for word in line.split():
            f = count[word]
            #print('{}, f={}'.format(word, f))

    # for line in df["문장"]:
    #     for word in line.split():
    #         n = len(word)
    #         flag = True
    #         for e in range(2, n + 1):  # 1음절 예외
    #             w = word[:e]
    #             f = count[w]
    #             p = f / count[word[:e - 1]]
    #             s = n_score(w)
    #
    #             print('{}, f={}, p={:.2}, s={:.2}'.format(w, f, p, s))

def train_extract(self, sents, min_noun_score=0.5, min_noun_frequency=5,
                  noun_candidates=None):

    self.train(sents, min_noun_frequency)
    return self.extract(min_noun_score, min_noun_frequency, noun_candidates)
