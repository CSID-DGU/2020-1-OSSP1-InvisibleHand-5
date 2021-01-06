import create
import preprocess
import result
import analyze
import morphs
import emotion_word
import math
import pandas as pd
import noun_ex
from nltk.tag import StanfordPOSTagger
from nltk.tokenize import word_tokenize
from konlpy.tag import Komoran
from matplotlib import pyplot as plt
from koalanlp import API
from koalanlp.proc import EntityRecognizer
from koalanlp.Util import initialize, finalize
import os
import sys

initialize(etri='LATEST')

recognizer = EntityRecognizer(API.ETRI, etri_key="a839fcc8-298c-4a53-8477-c2f7b1273ff3")

parsed = recognizer("그 환자는 서울에 살고있다.")
# 또는 recognizer.analyze(...), recognizer.invoke(...)

# 첫번째 문장의 개체명들을 출력합니다.
for entity in parsed[0].getEntities():
    print(entity)

finalize()