# easysmi
- The following libraries make it easy to handle smi files.
- 다음 라이브러리를 사용하면 간편하게 smi 파일의 싱크를 조절 할 수 있습니다.

## install
```python
pip install easysmi
```
다음 명령어를 입력하여 라이브러리를 설치합니다.



```python
pip uninstall easysmi
```

설치를 했는데 문제가 발생해서 제거해야 하는 경우는 다음 명령어를 입력 합니다.

## How to Use
```python
from easysmi import *
path = "C:/[SubsPlease] Tokyo Revengers - 01.smi"
p = parse_smi(path)
```
우선 다음과 같이 열 파일의 자막 경로를 parse_smi에 인자값으로 제공하여 smi를 파싱합니다.

```python
print(p['line'])
print(p['main'][0:10])
print(p['text'][0:10])
```
해당 명령어로 파싱된 smi의 다양한 정보를 가져올 수 있습니다.  
**line**은 총 줄 갯수, **main**은 리스트 형태로 SMI의 싱크, 그 싱크에 표시되는 텍스트를 한번에 추출하고  
**text**는 리스트 형태로 텍스트 만을 추출합니다.
* 해당 라이브러리에서는 줄 갯수를 대사마다 한줄씩 새는 것이 아닌 한 싱크에 표시되는 항목을 한 줄로 인식합니다.  
  ex) 어떤 영상 1:00에서 5줄, 10줄인 대사가 나와도 1줄(1개의 항목)로 생각합니다.

<br/>

**자막이 10초 늦게 나올때 (-10초 만큼 땡김)**

```python
path = "C:/[SubsPlease] Tokyo Revengers - 01.smi"
p = parse_smi(path)
s = sync_shift(p, 0, -10000) #0번째(첫번째)라인부터 끝까지 -10초
```



**자막이 10초 빨리 나올때 (+10초 만큼 지연)**

```python
path = "C:/[SubsPlease] Tokyo Revengers - 01.smi"
p = parse_smi(path)
s = sync_shift(p, 0, 10000) #0번째(첫번째)라인부터 끝까지 +10초
```



**작업한 자막 파일 저장 방법**

```python
path = "C:/test.smi"
p = parse_smi(path)
s = sync_shift(p, 0, 2000)

new_path = "enter_your_save_path_here"
file_save(new_path, s)
```



**smi에서 첫번째 항목 제거**

```python
path = "C:/[SubsPlease] Tokyo Revengers - 01.smi"
p = parse_smi(path)
print(p['main'][0:5])
r = remove_line(p, 0)
print(r['main'][0:5])
```



## S(sponsored) 자막을 NS(non-sponsored) 자막으로 쉽게 바꾸기

![image](https://user-images.githubusercontent.com/31213158/134211650-89ec18d8-ef05-4a99-bdd4-f198b89b58d6.png)

애니메이션을 보다 보면 영상 시작전 10초 정도 다음과 같은 화면에서 스폰서(후원자)가 표시되고 영상이 진행되는 경우가 많습니다. 

보통 방영중인 애니메이션이 한참 방영중일때는 릴그룹이 방영중인 TV영상을 파일로 변환해서 배포하기 때문에 자막 작업 하시는 분들도 이 스폰서가 중간에 껴있는걸 기준으로 작업하시는 경우가 많습니다.  

(이렇게 스폰서가 껴있고 빠른 Release로 유명한 그룹이 Ohys-Raws)



그런데 시간이 지나면서 BD판이 뜨고, 편집본이 뜨다보면 중간에 스폰서가 편집상 사라지는 경우가 99%인데 스폰서를 기준으로 작업한 것은 싱크가 10초정도 어긋나게 됩니다. 

보통 다음팟플레이어 같은 것으로 -10초를 하게 되면 싱크가 대부분 맞게 되는데 전체적으로 -10초 되는 것이기 때문에 앞의 오프닝의 싱크가 맞지 않는 불상사가 생깁니다. 물론 오프닝은 대부분 몇번만 보고 스킵하겠지만 저는 이게 불편해서 해당 라이브러리를 제작 했습니다.



```python
#단일 파일 처리

folder = 'C:/자막/'
filename = '[SubsPlease] Tokyo Revengers - 02 (1080p) [B66CEAA7].smi'

p = parse_smi(folder + filename)
search_line = find_line_by_text(p, "sub by")

if search_line != -1:
    s = sync_shift(p, search_line, -10000)
    s = sync_shift(s, 0, 1300)
    
    make_dirs(folder + 'output') #make output folder
    new_path = folder + "output/" + filename
    file_save(new_path, s)
else:
    print("cannot find item")
```

영상 자막이 (sub by 제작자)가 뜨고 나서 스폰서가 뜨는데 제가 받은 영상엔 스폰서가 없어서 싱크가 맞지 않습니다.

"sub by" 텍스트의 위치부터 자막 끝까지 -10초로 싱크를 조절하고 다시 전체적으로 +1.3초로 조정 한 뒤 output 폴더에 저장하는 예제입니다.



```python
find_line_by_text(p, "sub by")
```

find_line_by_text 함수는 파싱된 자막 데이터 내에서 인자로 들어온 string 값의 포함여부를 확인하고 그 line 위치를 반환합니다.

찾지 못한다면 -1을 반환 합니다.



```python
find_line_by_regex(p, "pattern"):
```

또한 정규식을 통한 검색도 지원 합니다. 단, 정규식에서 처음으로 match 된 string의 위치를 반환 합니다.

찾지 못한다면 -1을 반환 합니다.



지원되는 함수를 이용해 자유롭게 자막 작업을 하시길 바랍니다.

## 사용시 주의 할 점
이 프로그램은 단순히 특정 규칙에 따라 싱크를 조절 하므로 어떤 영상의 경우엔 스폰서가 아예 없어서 이렇게 조절하면 오히려 싱크가 어긋날 수 있습니다.  
영상 시청 중 그런 문제가 발생시 다시 수동으로 조절하시거나 원래 자막으로 복구하시면 됩니다.  
그리고 웬만하면 해당 BD 자막이 존재하면 그걸 받아서 쓰는게 제일 좋습니다.  

### Bug Report

버그 발견시 해당 Github 사이트 내의 Issues 탭을 이용해 제보 부탁드립니다.
또한 개선점도 제보 해주시면 좋습니다.
