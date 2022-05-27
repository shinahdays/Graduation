import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import os

# 시작시간
sdt = datetime.datetime.now()

# 드라이버 설정
opt = webdriver.ChromeOptions()
opt.add_argument('headless')
opt.add_argument('disable-gpu')
srv = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=srv, options=opt)

titleList = []
dateList = []
nickList = []
numList = []

# 갤러리 안내
# 야갤 https://gall.dcinside.com/board/lists?id=baseball_new10
# 롤갤 https://gall.dcinside.com/board/lists?id=leagueoflegends4
# 키갤 https://gall.dcinside.com/mgallery/board/lists?id=kizunaai
# 프세카갤 https://gall.dcinside.com/mgallery/board/lists?id=pjsekai
# 버스갤 https://gall.dcinside.com/mini/board/lists?id=virtual_streamer
# 이세돌갤 https://gall.dcinside.com/mini/board/lists?id=isekaidol

print('갤러리 제목파싱')
print('정규 갤러리 야갤 -y // 롤갤 -l')
print('마이너 갤러리 키갤 -k // 프세카갤 -p')
print('미니 갤러리 버스갤 -b // 이세돌갤 -i')
gallInfo = input('어떤 갤러리를 선택하시겠습니까')
gallPath = ''

# 갤러리 셋팅
if gallInfo == 'y':
    gallInfo = '야갤'
    gallPath = 'board/lists?id=baseball_new10'
elif gallInfo == 'l':
    gallInfo = '롤갤'
    gallPath = 'board/lists?id=leagueoflegends4'
elif gallInfo == 'k':
    gallInfo = '키갤'
    gallPath = 'mgallery/board/lists?id=kizunaai'
elif gallInfo == 'p':
    gallInfo = '프세카갤'
    gallPath = 'mgallery/board/lists?id=pjsekai'
elif gallInfo == 'b':
    gallInfo = '버스갤'
    gallPath = 'mini/board/lists?id=virtual_streamer'
elif gallInfo == 'i':
    gallInfo = '이세돌갤'
    gallPath = 'mini/board/lists?id=isekaidol'
else:
    print('제대로된 값을 입력해주세요')

# 탐색하고자 하는 페이지 입력
start = int(input('시작페이지 번호를 입력하세요'))
end = int(input('끝페이지 번호를 입력하세요'))

# 파일 최초생성 제목 설정
makingFileRes = './' + '%s' % gallInfo + 'res' + str(start) + '_' + str(end) + '.txt'

# 파일 경로
resfilePath = ('%s' % makingFileRes)

# 파일이 없다면 최초 생성
firstNum = os.path.exists(resfilePath)
if not firstNum:
    with open(resfilePath, 'w', encoding='utf-8') as f:
        f.close()


# 요소찾기 함수
def find_element(a, b):
    for i in range(a, b):
        # 번호 셀렉터
        numselector = ''
        numselector += '#container > section.left_content > article:nth-child(3) > div.gall_listwrap.list > table > tbody > tr:nth-child('
        numselector += str(i)
        numselector += ') > td.gall_num'

        # 제목 셀렉터
        titleselector = ""
        titleselector += "#container > section.left_content > article:nth-child(3) > div.gall_listwrap.list > table > tbody > tr:nth-child("
        titleselector += str(i)
        titleselector += ") > td.gall_tit.ub-word> a:nth-child(1)"

        # 닉네임 셀렉터
        nickselector = ""
        nickselector += "#container > section.left_content > article:nth-child(3) > div.gall_listwrap.list > table > tbody > tr:nth-child("
        nickselector += str(i)
        nickselector += ") > td.gall_writer.ub-writer"

        # 날짜 셀렉터
        dateselector = ""
        dateselector += "#container > section.left_content > article:nth-child(3) > div.gall_listwrap.list > table > tbody > tr:nth-child("
        dateselector += str(i)
        dateselector += ") > td.gall_date"

        num = driver.find_elements(By.CSS_SELECTOR, '%s' % numselector)
        title = driver.find_elements(By.CSS_SELECTOR, '%s' % titleselector)
        nick = driver.find_elements(By.CSS_SELECTOR, '%s' % nickselector)
        date = driver.find_elements(By.CSS_SELECTOR, '%s' % dateselector)

        for j in num:
            numList.append(j.text)
            #numList.append('\n')

        for j in title:
            titleList.append(j.text)
            #titleList.append('\n')

        for j in nick:
            nickList.append(j.text)
            #nickList.append('\n')

        for j in date:
            dateList.append(j.text)
            #dateList.append('\n')


# 링크에서 요소찾기 함수 실행
for i in range(start, end + 1):
    linkPath = ""
    linkPath += "https://gall.dcinside.com/"
    linkPath += gallPath
    linkPath += "&page="
    linkPath += str(i)
    linkPath += "&list_num=100"

    driver.get("%s" % linkPath)
    driver.implicitly_wait(10)
    find_element(2, 101)
    print(i)

driver.close()
# 최초 생성된 파일에 각각의 리스트 작성
# print(len(numList))
# print(len(titleList))
# print(len(nickList))
# print(len(dateList))

with open(resfilePath, 'a', encoding='utf-8') as f:
    for i in range(len(numList)):
        s = numList[i]
        s += " - "
        s += titleList[i]
        s += " - "
        s += nickList[i]
        s += " - "
        s += dateList[i]
        s += "\n"
        f.writelines(s)
    f.close()


# 현재시간
edt = datetime.datetime.now()
print("시작시간", sdt)
print("끝난시간", edt)
print("걸린시간:", edt - sdt)
