import copy
import re
import chardet
from ..types.type import ParsedSMI

'''
Author: pgh268400 (https://pgh268400.tistory.com/)
Version: 1.0
License: MIT License
'''

# smi 파싱할 정규식
SMI_REGEX = r"<\s*Sync\s*Start\s*=\s*(\d+)\s*><\s*P\s*Class\s*=\s*\w+\s*>"

def read_file(path : str) -> str:
    #파일 열어서 인코딩 확인
    rawdata = open(path, 'rb').read()
    result = chardet.detect(rawdata)
    enc = result['encoding']
    
    #인코딩 맞게 열기
    f = open(path, "r", encoding = enc)
    line = f.readline()

    data = ""
    while line:
        data += line
        line = f.readline()
    f.close()
    return data

#raw_data => 자막 파일 텍스트 데이터
def parse_smi(path : str) -> ParsedSMI:
    raw_data = read_file(path)

    td : list[list[str]]= []
    text : list[str] = []

    # 자막 언어 추출
    TYPE_REGEX = r"<\s*Sync\s*Start\s*=\s*\d+\s*><\s*P\s*Class\s*=\s*(\w+)\s*>"
    p = re.compile(TYPE_REGEX, re.MULTILINE)
    type = p.search(raw_data)
    if type : type = type.group(1)
    else : type = None

    # 자막 타임라인 추출
    p = re.compile(SMI_REGEX, re.MULTILINE)
    time_line : list[str] = p.findall(raw_data)

    #타임라인 문자 전부 특수문자로 치환 후 split로 쪼갠다.
    base = '${SYNC}'
    lines : list[str] = p.sub(base, raw_data).split(base)[1:]

    # 마지막 요소에 있는 </BODY>, </SAMI> 태그를 제거한다.
    lines[-1] = lines[-1].replace("</BODY>", "").replace("</SAMI>", "")

    # 대사를 반복하며 양쪽에 있는 엔터, 공백을 제거한다.
    for i in range(len(lines)):
        lines[i] = lines[i].strip()

    # [타임라인, 대사] 로 저장한다.
    for i in range(len(time_line)):
        td.append([time_line[i], lines[i]]) 
        # 처리하면서 text에도 저장한다.
        text.append(lines[i])

    #데이터 정리
    result = ParsedSMI(orig=path,main=td, raw=raw_data, text=text, line=len(td), type = type)
    
    return result


#텍스트로 파싱된 라인 찾기
def find_line_by_text(parsed_data : ParsedSMI, target):
    main = parsed_data.main
    j = -1
    for element in main:
        j+= 1
        for i in range(len(element)):
            if target in element[i]:
                return j
    return j

#정규식으로 파싱된 라인 찾기
def find_line_by_regex(parsed_data : ParsedSMI, regex):
    main = parsed_data.main
    
    j = -1
    for element in main:
        j+= 1
        for i in range(len(element)):
            m = re.search(regex, element[i])
            if m : return j
    return j
    
# parsed_data => parse_smi 의 output으로 나온 리스트 데이터
# start_line => 몇번째 항목부터 옮길 것인지. (0번째부터 시작)
# shift_amount => 얼마만큼 싱크 조절할 것인지. (-1000 -> 1초 빨리 나오게 하기, 10000 -> 10초 늦게 나오게 하기)
def sync_shift_by_index(parsed_data : ParsedSMI, start_line_idx : int, shift_amount : int): 
    # 참고 : 건드는 것은 main 항목뿐이다. 나머지는 그대로 둔다.

    # parsed_data 는 Class Type 이므로 복사본을 만들어서 건드린다. (깊은 복사 수행)
    copy_parsed_data = copy.deepcopy(parsed_data)

    for i, element in enumerate(copy_parsed_data.main):
        if i >= start_line_idx:
            element[0] = str(int(element[0]) + shift_amount)
    return copy_parsed_data

def remove_line(parsed_data : ParsedSMI, remove_line_idx):
    parsed_data.main.pop(remove_line_idx)
    parsed_data.line = len(parsed_data.main)
    return parsed_data

#path => 파일 저장 경로
#shifted_data => 덮어 씌울 싱크 작업된 parsed_data
def smi_file_save(path : str, shifted_data : ParsedSMI):
    raw = shifted_data.raw
    try:
        #싱크 작업된 데이터를 SMI 문자열로 변환한다.
        smi_data = "\n"
        for element in shifted_data.main:
            timeline, text = element
            smi_data += f"<Sync Start={timeline}><P Class={shifted_data.type}>\n{text}\n"

        # 정규표현식을 사용하여 BODY 태그 사이의 내용을 찾고, 그 안에 있는 내용을 작업한 내용으로 대체한다.
        match = re.search(r'<BODY>(.*?)<\/BODY>', raw, re.DOTALL)

        if match:
            body_content = match.group(1)  # BODY 태그 안의 내용
            output = raw.replace(body_content, smi_data)  # BODY 태그 안의 내용을 치환한다.
        else:
            raise Exception('BODY 태그를 찾을 수 없습니다.')
        
        # 수정된 문자열을 파일로 저장한다.
        f = open(path, "w", encoding='utf-8')
        f.write(output)
        f.close()
        return True
    except Exception as e:
        raise e