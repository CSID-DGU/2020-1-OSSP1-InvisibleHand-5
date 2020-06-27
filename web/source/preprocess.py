import re

def del_new_lines(book):
    context = book.read().replace("\n", " ")
    return context


def change_to_qm(string):  # 매개변수 = 문자열 (꺽쇠를 쌍따옴표로)
    string = string.replace("「", "\"")
    string = string.replace("」", "\"")
    return string


def remove_chinese(string):  # 매개변수 = 문자열.(한자 제거)
    ch = '([\u2e80-\u2eff]+)' # 한중일 부수 보충
    string = re.sub(ch, '', string)

    ch = '([\u3400-\u4dbf]+)' # 한중일 통합 한자 확장 - A
    string = re.sub(ch, '', string)

    ch = '([\u4e00-\u9fbf]+)'  # 한중일 통합 한자
    string = re.sub(ch, '', string)

    ch = '([\uf900-\ufaff]+)'  # 한중일 호환용 한자
    string = re.sub(ch, '', string)

    return string


def change_etc(string):
    ch = '[\u201c-\u201d]'
    string = re.sub(ch, '\"', string)
    ch = '\u2014'
    string = re.sub(ch, 'ㅡ', string)
    return string


def remove_etc(book):
    context = del_new_lines(book)
    context = change_to_qm(context)
    context = remove_chinese(context)
    context = change_etc(context)
    return context