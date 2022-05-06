import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from wordcloud import WordCloud
from wordcloud import STOPWORDS
import matplotlib.pyplot as plt
from collections import Counter
from konlpy.tag import Okt

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
print("야구갤러리 제목파싱")
start = int(input("시작페이지 번호를 입력하세요"))
end = int(input("끝페이지 번호를 입력하세요"))

makingFileTitle = './BaseBallGall0309Title' + str(start) + '_' + str(end) + '.txt'
makingFileDate = './BaseBallGall0309Date' + str(start) + '_' + str(end) + '.txt'

titlefilePath = ('%s' % makingFileTitle)
datefilePath = ('%s' % makingFileDate)

firstTitle = os.path.exists(titlefilePath)
# 파일이 없다면 최초 생성
if not firstTitle:
    with open(titlefilePath, 'w', encoding='utf-8') as f:
        f.writelines("제목 리스트\n")
        f.close()
firstDate = os.path.exists(datefilePath)
if not firstDate:
    with open(datefilePath, 'w', encoding='utf-8') as f:
        f.writelines("날짜 리스트\n")
        f.close()


def findtitle(a, b):
    for i in range(a, b):
        titleselector = ""
        titleselector += "#container > section.left_content > article:nth-child(3) > div.gall_listwrap.list > table > tbody > tr:nth-child("
        titleselector += str(i)
        titleselector += ") > td.gall_tit.ub-word> a:nth-child(1)"

        dateselector = ""
        dateselector += "#container > section.left_content > article:nth-child(3) > div.gall_listwrap.list > table > tbody > tr:nth-child("
        dateselector += str(i)
        dateselector += ") > td.gall_date"

        title = driver.find_elements(By.CSS_SELECTOR, '%s' % titleselector)
        date = driver.find_elements(By.CSS_SELECTOR, '%s' % dateselector)
        for j in title:
            titleList.append(j.text)
            titleList.append("\n")

        for j in date:
            dateList.append(j.text)
            dateList.append("\n")


for i in range(start, end + 1):
    linkPath = ""
    linkPath += "https://gall.dcinside.com/board/lists/?id=baseball_new10&page="
    linkPath += str(i)
    linkPath += "&list_num=100"
    driver.get("%s" % linkPath)
    driver.implicitly_wait(10)
    findtitle(2, 101)
    print(i)

with open(titlefilePath, 'a', encoding='utf-8') as f:
    f.writelines(titleList)
    f.close()
with open(datefilePath, 'a', encoding='utf-8') as f:
    f.writelines(dateList)
    f.close()

driver.close()

# 현재시간
edt = datetime.datetime.now()
print("시작시간", sdt)
print("끝난시간", edt)
print("걸린시간:", edt - sdt)

with open("./MergeResult.txt", 'w', encoding='utf-8') as f:
    f.close()

# To text
f1 = open(titlefilePath, 'r', encoding='utf-8')
f2 = open(datefilePath, 'r', encoding='utf-8')
f3 = open("./MergeResult.txt", 'a', encoding='utf-8')
while True:
    a = f1.readline()
    a = a.strip()

    k = f2.readline()

    m = a + k

    if not m:
        break

    f3.writelines(m)

f1.close()
f2.close()
f3.close()

# Word Cloud

with open("./MergeResult.txt", 'r', encoding='utf-8') as f:
    text = f.read()

okt = Okt()
nouns = okt.nouns(text)

words = [n for n in nouns if len(n) > 1]
c = Counter(words)

# 불용어

stwd = set(STOPWORDS)
stwd.add('이미지')
stwd.add('순서')

wc = WordCloud(stopwords=stwd, font_path='Maplestory Light.ttf', width=500, height=500, scale=2.0, max_font_size=250)
gen = wc.generate_from_frequencies(c)
plt.figure()
plt.imshow(gen)
makingWCTitle = './BaseBallGall0309.png'
wcPath = ('%s' % makingWCTitle)

wc.to_file('%s' % wcPath)

os.system("pause")