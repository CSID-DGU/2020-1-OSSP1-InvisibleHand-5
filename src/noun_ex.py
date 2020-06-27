from collections import defaultdict

count = defaultdict(lambda: 0)


def noun_extract(df):
    for line in df["문장"]:
        for word in line.split():
            count[word] += 1

    for line in df["문장"]:
        for word in line.split():
            f = count[word]

def train_extract(self, sents, min_noun_score=0.5, min_noun_frequency=5,
                  noun_candidates=None):

    self.train(sents, min_noun_frequency)
    return self.extract(min_noun_score, min_noun_frequency, noun_candidates)
