import re
def del_new_lines(book):
    context = book.read().replace("\n", "")
    return context

def change_to_qm(string): #매개변수 = 문자열 (꺽쇠를 쌍따옴표로)
    string = string.replace("「", "\"")
    string = string.replace("」", "\"")
    return string

def remove_chinese(string): #매개변수 = 문자열.(한자 제거)
    ch = '([\u4e00-\u9fff]+)'
    string = re.sub(ch, '', string)
    return string
