from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import datetime

#현재시간
dtNow = datetime.datetime.now()
print(dtNow)

# 드라이버 설정
opt = webdriver.ChromeOptions()
srv = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=srv, options=opt)


# 최대창에서 URL 열기
driver.get("https://gall.dcinside.com/mgallery/board/lists?id=kizunaai")
driver.maximize_window()
time.sleep(2)

# 게시글 배열
contInfo = []
contList = []

# 게시글 번호
numInfo = []
numList = []

# 닉네임
nickInfo = []
nickList = []
for i in range(9, 52):
    # 글번호의 css요소 경로
    numPath = ""
    numPath += "#container > section.left_content > article:nth-child(3) > div.gall_listwrap.list > table > tbody > tr:nth-child("
    numPath += str(i)
    numPath += ") > td.gall_num"

    numInfo = driver.find_elements(By.CSS_SELECTOR, '%s' %numPath)

    for j in numInfo:
        numList.append(j.text)

    # 게시글의 css요소 경로
    contPath = ""
    contPath += "#container > section.left_content > article:nth-child(3) > div.gall_listwrap.list > table > tbody > tr:nth-child("
    contPath += str(i)
    contPath += ") > td.gall_tit.ub-word > a:nth-child(1)"

    contInfo = driver.find_elements(By.CSS_SELECTOR, '%s' % contPath)

    for k in contInfo:
        contList.append(k.text)
    # 닉네임의 css요소 경로
    nickPath = ""
    nickPath += "#container > section.left_content > article:nth-child(3) > div.gall_listwrap.list > table > tbody > tr:nth-child("
    nickPath += str(i)
    nickPath += ") > td.gall_writer.ub-writer"

    nickInfo = driver.find_elements(By.CSS_SELECTOR, '%s' % nickPath)

    for l in nickInfo:
        nickList.append(l.text)


print(numList)
print(contList)
print(nickList)



# 스크린샷
driver.save_screenshot('screenshot0.png')
driver.execute_script("window.scrollTo(0, 700)")
driver.save_screenshot('screenshot1.png')
driver.execute_script("window.scrollTo(700, 1400)")
driver.save_screenshot('screenshot2.png')
#driver.close()

# 글 내용 가져오기
writingList = []

for i in range(0, 43):
    writPath = ""
    writPath += "https://gall.dcinside.com/mgallery/board/view/?id=kizunaai&no="
    writPath += numList[i]
    driver.get("%s" % writPath)
    writing = driver.find_elements(By.CSS_SELECTOR, '#container > section > article:nth-child(3) > div.view_content_wrap > div > div.inner.clear > div.writing_view_box')
    for j in writing:
        writingList.append(j.text)

print(writingList)



driver.close()


