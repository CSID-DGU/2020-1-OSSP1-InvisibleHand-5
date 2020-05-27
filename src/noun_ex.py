from collections import defaultdict

count = defaultdict(lambda: 0)

def n_score(w):
    return pow(count[w]/count[w[0]],1/(len(w)-1))

def noun_extract(df):
    for line in df["문장"]:
        for word in line.split():
            n = len(word)
            for e in range(1, n+1):
                count[word[:e]] += 1

    for line in df["문장"]:
        for word in line.split():
            n = len(word)
            flag = True
            for e in range(2, n + 1):  # 1음절 예외
                w = word[:e]
                f = count[w]
                p = f / count[word[:e - 1]]
                s = n_score(w)

                #print('{}, f={}, p={:.2}, s={:.2}'.format(w, f, p,s))

def train_extract(self, sents, min_noun_score=0.5, min_noun_frequency=5,
                  noun_candidates=None):

    self.train(sents, min_noun_frequency)
    return self.extract(min_noun_score, min_noun_frequency, noun_candidates)

def train(self, sents, min_noun_frequency=5):
    check_corpus(sents)
    wordset_l, wordset_r = self._scan_vocabulary(sents, min_noun_frequency)
    lrgraph = self._build_lrgraph(sents, wordset_l, wordset_r)
    self.lrgraph = LRGraph(lrgraph)
    self.words = wordset_l

def _scan_vocabulary(self, sents, min_frequency=5):
    wordset_l = defaultdict(lambda: 0)
    wordset_r = defaultdict(lambda: 0)

    for i, sent in enumerate(sents):
        if not self.ensure_normalized:
            sent = normalize_sent_for_lrgraph(sent)
        for token in sent.split(' '):
            if not token:
                continue
            token_len = len(token)
            for i in range(1, min(self.max_left_length, token_len) + 1):
                wordset_l[token[:i]] += 1
            for i in range(1, min(self.max_right_length, token_len)):
                wordset_r[token[-i:]] += 1
        if self.verbose and (i % 1000 == 999):
            message = 'scanning {} / {} sents'.format(i + 1, len(sents))
            print('\r[Noun Extractor] {}'.format(message), end='')

    self._substring_counter = {w: f for w, f in wordset_l.items() if f >= min_frequency}
    wordset_l = set(self._substring_counter.keys())
    wordset_r = {w for w, f in wordset_r.items() if f >= min_frequency}

    if self.verbose:
        message = '(L,R) has (%d, %d) tokens' % (len(wordset_l), len(wordset_r))
        print('\r[Noun Extractor] scanning was done {}'.format(message))

    return wordset_l, wordset_r

def detaching_features(nouns, features, logpath=None, logheader=None):

    if not logheader:
        logheader = '## Ignored noun candidates from detaching features'

    removals = set()

    for word in nouns:

        if len(word) <= 2:
            continue

        for e in range(2, len(word)):

            l, r = word[:e], word[e:]

            # Skip a syllable word such as 고양이, 이력서
            if len(r) <= 1:
                continue

            if (l in nouns) and (r in features):
                removals.add(word)
                break

    if logpath:
        write_log(logpath, logheader, removals)

    nouns_ = _select_true_nouns(nouns, removals)
    return nouns_, removals