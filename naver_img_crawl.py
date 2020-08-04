from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen
import requests
import time
import os

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--headless')

# 드라이버 경로 지정
driver = webdriver.Chrome("/usr/local/bin/chromedriver", options=options)

# 검색어 입력
query = input("입력 : ")

# 검색어로 폴더명 지정
dirs = query

# 경로 지정
path = "/Users/tife/PycharmProjects/pythonProject1/" + dirs

print("__ 크롤링 스타트 __")

Url = ("https://search.naver.com/search.naver?where=image&section=image&query=" + query + "&res_fr=786432&res_to=100000000&sm=tab_opt&face=0&color=0&ccl=0&nso=so%3Ar%2Ca%3Aall%2Cp%3Aall&datetype=0&startdate=0&enddate=0&start=1")
driver.get(Url)
time.sleep(3)
count = 0

pictures = []
before_src = ""

# 폴더 생성
if not os.path.exists(dirs):
    os.mkdir(dirs)

pictures = driver.find_elements_by_tag_name("span.img_border")

for index, img in enumerate(pictures[0:]):
    # 위의 큰 이미지를 구하기 위해 위의 태그의 리스트를 하나씩 클릭한다.
    img.click()
    # 한번에 많은 접속을 하여 image를 크롤링하게 되면 naver, google서버에서 우리의 IP를 10~20분
    # 정도 차단을 하게된다. 때문에 Crawling하는 간격을 주어 IP 차단을 피하도록 장치를 넣어주었다.
    time.sleep(2)
    # 확대된 이미지의 정보는 img태그의 _image_source라는 class안에 담겨있다.
    html_objects = driver.find_element_by_tag_name('img._image_source')
    current_src = html_objects.get_attribute('src')
    print("=============================================================")
    print("현재 src :" + current_src)
    print("이전 src :" + before_src)
    if before_src == current_src:
        continue
    elif before_src != current_src:
        t = urlopen(current_src).read()
        if index < 40:
            filename = path + '/' + query + str(count) + ".jpg"
            with open(filename, "wb") as f:
                f.write(t)
                count += 1
                before_src = current_src
                current_src = ""
            print("Img Save Success")
        else:
            driver.close()
            break

