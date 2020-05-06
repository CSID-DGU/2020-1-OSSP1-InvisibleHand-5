import re
import csv
lex_file = open('Korean_Lexicon.txt','rt', encoding='UTF8')
lex_file.seek(0)
stab = re.compile("[^\t]+")

sentiments = ['anger', 'anticipation', 'disgust', 'fear', 'joy','sadness', 'surprise', 'trust']

anger = {}
anticipation = {}
disgust = {}
fear = {}
joy = {}
sadness = {}
surprise = {}
trust = {}


line_data = lex_file.readline()
line_data = lex_file.readline()

while line_data:

    key = stab.findall(line_data)[1]    # 단어 (키값)
    val1 = stab.findall(line_data)[2]   # 감정의 종류 (ex. anger, joy)
    val2 = stab.findall(line_data)[3].replace("\n", "") # 감정의 정도
   
    if val1==sentiments[0]:
        anger[key] = [val1,val2]
        line_data = lex_file.readline()
    elif val1 == sentiments[1]:
        anticipation[key] = [val1,val2]
        line_data = lex_file.readline()
    elif val1 == sentiments[2]:
        disgust[key] = [val1,val2]
        line_data = lex_file.readline()
    elif val1 == sentiments[3]:
        fear[key] = [val1,val2]
        line_data = lex_file.readline()
    elif val1 == sentiments[4]:
        joy[key] = [val1,val2]
        line_data = lex_file.readline()
    elif val1 == sentiments[5]:
        sadness[key] = [val1,val2]
        line_data = lex_file.readline()
    elif val1 == sentiments[6]:
        surprise[key] = [val1,val2]
        line_data = lex_file.readline()
    elif val1 == sentiments[7]:
        trust[key] = [val1,val2]
        line_data = lex_file.readline()
    else :
        print('끝')



a_file = open("sentiments.csv", "w", encoding = 'UTF8')

writer = csv.writer(a_file)
for key, value in anger.items():
    writer.writerow([key, value])
for key, value in anticipation.items():
    writer.writerow([key, value])
for key, value in disgust.items():
    writer.writerow([key, value])
for key, value in fear.items():
    writer.writerow([key, value])
for key, value in joy.items():
    writer.writerow([key, value])
for key, value in sadness.items():
    writer.writerow([key, value])
for key, value in surprise.items():
    writer.writerow([key, value])
for key, value in trust.items():
    writer.writerow([key, value])



a_file.close()
lex_file.close()