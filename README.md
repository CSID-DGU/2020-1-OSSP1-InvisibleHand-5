# 2020-1-OSSP1-InvisibleHand-5
- 공개SW프로젝트01 5조 보않손
- 팀원 : 김우용, 박종근, 최윤호, 김도훈


## 주제
 NLTK 및 konlpy를 활용한 국문 소설 등장인물의 감정 분석 및 흐름 파악


## 사용 오픈소스 라이브러리
- [konlpy](https://github.com/konlpy/konlpy)
- [NLTK](https://github.com/nltk/nltk) 3.5
- [numpy](https://github.com/numpy/numpy) 1.18.3 
- [pandas](https://github.com/pandas-dev/pandas) 1.0.3
- [openpyxl](https://foss.heptapod.net/openpyxl/openpyxl)  3.0.3
- [JPype](https://github.com/jpype-project/jpype) 0.7.4
- [matplotlib](https://github.com/matplotlib/matplotlib) - 3.2.1
- [NRC LEXICON EMOTION ](http://saifmohammad.com/WebPages/NRC-Emotion-Lexicon.htm) - 감정 사전


## 개발 환경
Develop Tool : Python, Node.js

## 기능
분석하고싶은 소설 텍스트 파일과 등장인물 이름을 입력 

- 예시
```
소설: 운수 좋은날 - 현진건
등장인물: 김첨지
```

- 문장별 감정 분석 데이터프레임 출력

<img src="https://user-images.githubusercontent.com/53558710/85926224-e1440700-b8d8-11ea-939b-e74549a8703a.png"  width="600">

- 각 등장인물 문장 별 감정 분석 결과 그래프 출력
<img src="https://user-images.githubusercontent.com/53558710/85925707-354cec80-b8d5-11ea-8622-36038efac320.png"  width="600">

- 흐름을 보기 용이하게 일정 단위로 묶은 감정 분석 결과 그래프 
<img src="https://user-images.githubusercontent.com/53558710/85925945-b789e080-b8d6-11ea-8f0b-dcb4f4e3bd05.png"  width="600">



## 문의
박종근 - whdrms5826@naver.com
