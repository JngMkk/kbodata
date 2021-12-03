from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

# 이닝별 판정, x좌표, y좌표 데이터 프레임(전역 변수)
def inning():
    global innings
    innings = driver.find_elements_by_class_name('inning__view')
    if len(innings) >= 9 :
        for inning in innings:
            inning_index = innings.index(inning) + 1
            stzone = inning.find_elements_by_class_name('strike__zone')[3]      # 4번째 그림 심판이 판정한 스트라이크 + 볼
            svg = stzone.find_element_by_tag_name('svg')
            imgs = svg.find_elements_by_tag_name('image')
            xcd = []
            ycd = []
            sb = []
            append1 = xcd.append
            append2 = ycd.append
            append3 = sb.append
            for img in imgs:
                append1(img.get_attribute('x'))
                append2(img.get_attribute('y'))
                if img.get_attribute('xlink:href') == '/_nuxt/img/1c8f58b.png' :
                    append3(1)
                else :
                    append3(0)
            globals()['cd_{}'.format(inning_index)] = pd.DataFrame({'이닝': [num * 0 + inning_index for num in sb],
                                                                    '판정': sb,
                                                                    'x좌표' : xcd, 
                                                                    'y좌표' : ycd})
            time.sleep(5)
    else :
        pass

# 한 경기 모든 이닝 크롤링 + 엑셀 저장
def inning_crawl():
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
        if len(innings) == 15:
            df = pd.concat([cd_1,cd_2,cd_3,cd_4,cd_5,cd_6,cd_7,cd_8,cd_9,cd_10,cd_11,cd_12,cd_13,cd_14,cd_15], ignore_index = True)
            df.index.names = [f'{date}_{match}_{referee}']
            df.to_excel(f'./cd/{date}_{match}_{referee}.xlsx')
            time.sleep(2)
        elif len(innings) == 14:
            df = pd.concat([cd_1,cd_2,cd_3,cd_4,cd_5,cd_6,cd_7,cd_8,cd_9,cd_10,cd_11,cd_12,cd_13,cd_14], ignore_index = True)
            df.index.names = [f'{date}_{match}_{referee}']
            df.to_excel(f'./cd/{date}_{match}_{referee}.xlsx')
            time.sleep(2)
        elif len(innings) == 13:
            df = pd.concat([cd_1,cd_2,cd_3,cd_4,cd_5,cd_6,cd_7,cd_8,cd_9,cd_10,cd_11,cd_12,cd_13], ignore_index = True)
            df.index.names = [f'{date}_{match}_{referee}']
            df.to_excel(f'./cd/{date}_{match}_{referee}.xlsx')
            time.sleep(2)
        elif len(innings) == 12:
            df = pd.concat([cd_1,cd_2,cd_3,cd_4,cd_5,cd_6,cd_7,cd_8,cd_9,cd_10,cd_11,cd_12], ignore_index = True)
            df.index.names = [f'{date}_{match}_{referee}']
            df.to_excel(f'./cd/{date}_{match}_{referee}.xlsx')
            time.sleep(2)
        elif len(innings) == 11:
            df = pd.concat([cd_1,cd_2,cd_3,cd_4,cd_5,cd_6,cd_7,cd_8,cd_9,cd_10,cd_11], ignore_index = True)
            df.index.names = [f'{date}_{match}_{referee}']
            df.to_excel(f'./cd/{date}_{match}_{referee}.xlsx')
            time.sleep(2)
        elif len(innings) == 10:
            df = pd.concat([cd_1,cd_2,cd_3,cd_4,cd_5,cd_6,cd_7,cd_8,cd_9,cd_10], ignore_index = True)
            df.index.names = [f'{date}_{match}_{referee}']
            df.to_excel(f'./cd/{date}_{match}_{referee}.xlsx')
            time.sleep(2)
        elif len(innings) == 9:
            df = pd.concat([cd_1,cd_2,cd_3,cd_4,cd_5,cd_6,cd_7,cd_8,cd_9], ignore_index = True)
            df.index.names = [f'{date}_{match}_{referee}']
            df.to_excel(f'./cd/{date}_{match}_{referee}.xlsx')
            time.sleep(2)
        else :
            time.sleep(2)
            continue

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

# 2021.11 : 0 ~ 2021.04 : 7
# 2020.11 : 12 ~ 2020.05 : 18
# 2019.10 : 25 ~ 2019.03 : 32
# 2018.11 : 36 ~ 2018.03 : 44
# 2017.10 : 49 ~ 2017.03 : 56

driver = webdriver.Chrome(r'C:/Users/kjm08/Desktop/2021KNUpython2/chromedriver')
url = 'https://strikes.zone/game/211115DSBKTW'
driver.get(url)
time.sleep(10)
driver.find_element_by_css_selector('div.match__type > button.type__btn.type__btn--inning').click()
crawl_months = [0,1,2,3,4,5,6,7,12,13,14,15,16,17,18,25,26,27,28,29,30,31,32,36,37,38,39,40,41,42,43,44,49,50,51,52,53,54,55,56]
for i in crawl_months:
    crawl(i)