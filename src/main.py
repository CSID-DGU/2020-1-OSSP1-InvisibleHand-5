# 전처리 모듈
import preprocessing
# 형태소 분석 모듈
# import module.morphs
# 구문 분석 모듈
# import module.syntax
from konlpy.tag import Komoran


# 1. 입력 데이터 설정
# 파일 입력
fileName = input() + ".txt"
book = open(f'../res/book/{fileName}', "rt", encoding='UTF8')

# 등장 인물 입력받아 유저 사전에 저장

# 2. 전처리
# 개행 문자 제거 , 꺽쇠 -> 따옴표 변환 ,
context = preprocessing.del_new_lines(book)
unit = int(len(context)/200)

# 3. 감정 추출

# 4. 감정 분석

# 5. 결과 추출