from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

# 이닝별 판정, x좌표, y좌표
def inning():
    global rows
    global innings
    rows = []
    innings = driver.find_elements_by_class_name('inning__view')
    if len(innings) >= 9 :
        for inning in innings:
            inning_index = innings.index(inning) + 1
            stzone = inning.find_elements_by_class_name('strike__zone')[3]      # 4번째 그림 심판이 판정한 스트라이크 + 볼
            svg = stzone.find_element_by_tag_name('svg')
            imgs = svg.find_elements_by_tag_name('image')
            for img in imgs:
                inn = inning_index
                xcd = img.get_attribute('x')
                ycd = img.get_attribute('y')
                if img.get_attribute('xlink:href') == '/_nuxt/img/1c8f58b.png' :
                    sb = 1
                else :
                    sb = 0
                rows.append([inn, xcd, ycd, sb])
            time.sleep(5)
    else :
        pass

# 한 경기 모든 이닝 크롤링 + 엑셀 저장
def inning_crawl():
    columns = ['이닝', '판정', 'x좌표', 'y좌표']
    games = driver.find_elements_by_class_name('search__data')
    for i in range(len(games)):
        driver.find_elements_by_class_name('search__data')[i].click()
        time.sleep(10)
        html = driver.page_source
        soup = bs(html, 'html.parser')
        time.sleep(3)
        match = soup.select('div.match__team > span')[0].text + ' ' + soup.select('div.match__team > span')[1].text + ' ' + soup.select('div.match__team > span')[2].text
        date = soup.select_one('div.match__date').text.strip().split('투')[0]
        referee = soup.select_one('div.match__date > span').text.split('(')[1].split('심')[0].split(' ')[0]
        inning()
        df = pd.DataFrame(rows, columns = columns)
        df.index.names = [f'{date}_{match}_{referee}']
        df.to_excel(f'./cd/{date}_{match}_{referee}1.xlsx')
        
# 달력 넘기기
def first_cal(num):
    driver.find_element_by_class_name('strike__zone__wrapper').click()
    driver.find_element_by_class_name('mx-input-wrapper').click()
    time.sleep(3)
    for i in range(num):
        driver.find_element_by_class_name('mx-icon-last-month').click()
        time.sleep(1)
        if i == num :
            break

# 날짜 넘어갈 때마다 달력 넘기기
def last_cal(num):
    driver.find_element_by_class_name('mx-input-wrapper').click()
    time.sleep(3)
    for i in range(num):
        driver.find_element_by_class_name('mx-icon-last-month').click()
        time.sleep(1)
        if i == num :
            break

# 한 달 크롤링
def game_crawl(num):
    for i in range(42):
        month = driver.find_element_by_class_name('mx-panel.mx-panel-date')
        day = month.find_elements_by_tag_name('td')[i]
        time.sleep(3)
        if day.get_attribute('class') == 'cell cur-month' :
            day.click()
            time.sleep(3)
            driver.find_element_by_class_name('mx-datepicker-btn.mx-datepicker-btn-confirm').click()
            time.sleep(10)
            inning_crawl()
            last_cal(num)
        else :
            continue

# 최종
def crawl(num):
    first_cal(num)
    game_crawl(num)

# 리스트 만들어서 할 필요는 없음. 빠르게 하려고.
# 한 달 넘어갈 때마다 최신화

"""2021.12 달력 넘기는 횟수 리스트"""
# 2021.11 : 1 ~ 2021.04 : 8
# 2020.11 : 13 ~ 2020.05 : 19
# 2019.10 : 26 ~ 2019.03 : 33
# 2018.11 : 37 ~ 2018.03 : 45
# 2017.10 : 50 ~ 2017.03 : 57

driver = webdriver.Chrome(r'C:/Users/JngMK/Desktop/2021KNUpython2/chromedriver')
url = 'https://strikes.zone/game/211115DSBKTW'
driver.get(url)
time.sleep(10)
driver.find_element_by_css_selector('div.match__type > button.type__btn.type__btn--inning').click()
crawl_months = [1,2,3,4,5,6,7,8,13,14,15,16,17,18,19,26,27,28,29,30,31,32,33,37,38,39,40,41,42,43,44,45,50,51,52,53,54,55,56,57]
for i in crawl_months:
    crawl(i)