from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import re
import pandas as pd
from selenium.webdriver.support.select import Select

# 1 : 정규시즌
# 2 : 포스트시즌
def select_season(num):
    select_ss = Select(driver.find_element_by_id('ddlSeries'))
    select_ss.select_by_index(num)

# 0 : 2021 ~ 4 : 2017
# 해가 넘어가면 최신화
def select_year(num):
    select_yr = Select(driver.find_element_by_id('ddlYear'))
    select_yr.select_by_index(num)

# 0 : 1월 ~ 11 : 12월
def select_mon(num):
    select_m = Select(driver.find_element_by_id('ddlMonth'))
    select_m.select_by_index(num)

# 정규시즌 데이터
# 점수차는 그 이닝 시작 전 점수차
def regular_season(num):
    select_season(1)
    time.sleep(5)
    select_year(num)
    time.sleep(5)
    for i in range(2, 10):
        select_mon(i)
        html = driver.page_source
        soup = bs(html, 'html.parser')
        match_info = []
        hrefs = []
        
        games = soup.select('tbody > tr')
        for game in games:
            if '-' in game.select('td')[-1] :
                hrefs.append(game.select_one('td.relay a')['href'])
                match_info.append(re.sub(r'[0-9]+', '', game.select_one('td.play').text))
            else :
                continue
        
        if hrefs == []:
            continue
        
        else :
            columns = ['일자', '구장', '경기시간', '7회점수차', '8회점수차', '9회점수차', '10회점수차', '11회점수차', '12회점수차']
            rows = []
            time.sleep(5)

            for href in hrefs:
                url = 'https://www.koreabaseball.com' + href
                driver.get(url)
                time.sleep(10)
                html = driver.page_source
                soup = bs(html, 'html.parser')
                time.sleep(5)
                date = soup.find(id = 'lblGameDate').text
                stadium = soup.find(id = 'txtStadium').text.split(':')[1].split(' ')[1]
                runtime = soup.find(id = 'txtRunTime').text.split(':')[1].split(' ')[1] + '시간' + soup.find(id = 'txtRunTime').text.split(':')[2] + '분'
                scores_1 = soup.select('#tblScordboard2 > tbody:nth-child(3) > tr:nth-child(1) > td')
                scores_2 = soup.select('#tblScordboard2 > tbody:nth-child(3) > tr:nth-child(2) > td')
                a = []
                b = []
                for score_1 in scores_1 :
                    if score_1.text == '-':
                        continue
                    else :
                        a.append(int(score_1.text))
                for score_2 in scores_2 :
                    if score_2.text == '-':
                        continue
                    else :
                        b.append(int(score_2.text))
                if len(a) == 9 :
                    inning7 = abs(sum(a[0 : 6]) - sum(b[0 : 6]))
                    inning8 = abs(sum(a[0 : 7]) - sum(b[0 : 7]))
                    inning9 = abs(sum(a[0 : 8]) - sum(b[0 : 8]))
                    inning10 = '-'
                    inning11 = '-'
                    inning12 = '-'
                elif len(a) == 10 :
                    inning7 = abs(sum(a[0 : 6]) - sum(b[0 : 6]))
                    inning8 = abs(sum(a[0 : 7]) - sum(b[0 : 7]))
                    inning9 = abs(sum(a[0 : 8]) - sum(b[0 : 8]))
                    inning10 = abs(sum(a[0 : 9]) - sum(b[0 : 9]))
                    inning11 = '-'
                    inning12 = '-'
                elif len(a) == 11 :
                    inning7 = abs(sum(a[0 : 6]) - sum(b[0 : 6]))
                    inning8 = abs(sum(a[0 : 7]) - sum(b[0 : 7]))
                    inning9 = abs(sum(a[0 : 8]) - sum(b[0 : 8]))
                    inning10 = abs(sum(a[0 : 9]) - sum(b[0 : 9]))
                    inning11 = abs(sum(a[0 : 10]) - sum(b[0 : 10]))
                    inning12 = '-'
                elif len(a) == 12 :
                    inning7 = abs(sum(a[0 : 6]) - sum(b[0 : 6]))
                    inning8 = abs(sum(a[0 : 7]) - sum(b[0 : 7]))
                    inning9 = abs(sum(a[0 : 8]) - sum(b[0 : 8]))
                    inning10 = abs(sum(a[0 : 9]) - sum(b[0 : 9]))
                    inning11 = abs(sum(a[0 : 10]) - sum(b[0 : 10]))
                    inning12 = abs(sum(a[0 : 11]) - sum(b[0 : 11]))
                else :
                    pass
                rows.append([date, stadium, runtime, inning7, inning8, inning9, inning10, inning11, inning12])
    
            df_1 = pd.DataFrame(rows, columns = columns)
            df_2 = pd.DataFrame({'경기': match_info})
            df = pd.concat([df_1,df_2], axis = 1)
            df = df[['일자','경기', '구장', '경기시간', '7회점수차', '8회점수차', '9회점수차', '10회점수차', '11회점수차',
                   '12회점수차']]
            
            year = df['일자'][0].split('(')[0].split('.')[0]
            month = df['일자'][0].split('(')[0].split('.')[1]
            df.to_excel(f'./kbo/kbo_{year}_{month}.xlsx')
            time.sleep(3)
            
            result2 = driver.find_element_by_id('snb')
            result2.find_elements_by_tag_name('li')[2].click()
            time.sleep(3)
            select_season(1)
            time.sleep(5)
            select_year(num)
            time.sleep(5)

# 포스트시즌 데이터
def post_season(num):
    select_season(2)
    time.sleep(5)
    select_year(num)
    time.sleep(5)
    html = driver.page_source
    soup = bs(html, 'html.parser')
    match_info = []
    hrefs = []

    games = soup.select('tbody > tr')
    for game in games:
        if '-' in game.select('td')[-1] :
            hrefs.append(game.select_one('td.relay a')['href'])
            match_info.append(re.sub(r'[0-9]+', '', game.select_one('td.play').text))
        else :
            continue

    columns = ['일자', '구장', '경기시간', '7회점수차', '8회점수차', '9회점수차', '10회점수차', '11회점수차', '12회점수차', '13회점수차', '14회점수차', '15회점수차']
    rows = []

    for href in hrefs:
        url = 'https://www.koreabaseball.com' + href
        driver.get(url)
        time.sleep(10)
        html = driver.page_source
        soup = bs(html, 'html.parser')
        time.sleep(5)
        date = soup.find(id = 'lblGameDate').text
        stadium = soup.find(id = 'txtStadium').text.split(':')[1].split(' ')[1]
        runtime = soup.find(id = 'txtRunTime').text.split(':')[1].split(' ')[1] + '시간' + soup.find(id = 'txtRunTime').text.split(':')[2] + '분'
        scores_1 = soup.select('#tblScordboard2 > tbody:nth-child(3) > tr:nth-child(1) > td')
        scores_2 = soup.select('#tblScordboard2 > tbody:nth-child(3) > tr:nth-child(2) > td')
        a = []
        b = []
        for score_1 in scores_1 :
            if score_1.text == '-':
                continue
            else :
                a.append(int(score_1.text))
        for score_2 in scores_2 :
            if score_2.text == '-':
                continue
            else :
                b.append(int(score_2.text))
        if len(a) == 9 :
            inning7 = abs(sum(a[0 : 6]) - sum(b[0 : 6]))
            inning8 = abs(sum(a[0 : 7]) - sum(b[0 : 7]))
            inning9 = abs(sum(a[0 : 8]) - sum(b[0 : 8]))
            inning10 = '-'
            inning11 = '-'
            inning12 = '-'
            inning13 = '-'
            inning14 = '-'
            inning15 = '-'
        elif len(a) == 10 :
            inning7 = abs(sum(a[0 : 6]) - sum(b[0 : 6]))
            inning8 = abs(sum(a[0 : 7]) - sum(b[0 : 7]))
            inning9 = abs(sum(a[0 : 8]) - sum(b[0 : 8]))
            inning10 = abs(sum(a[0 : 9]) - sum(b[0 : 9]))
            inning11 = '-'
            inning12 = '-'
            inning13 = '-'
            inning14 = '-'
            inning15 = '-'
        elif len(a) == 11 :
            inning7 = abs(sum(a[0 : 6]) - sum(b[0 : 6]))
            inning8 = abs(sum(a[0 : 7]) - sum(b[0 : 7]))
            inning9 = abs(sum(a[0 : 8]) - sum(b[0 : 8]))
            inning10 = abs(sum(a[0 : 9]) - sum(b[0 : 9]))
            inning11 = abs(sum(a[0 : 10]) - sum(b[0 : 10]))
            inning12 = '-'
            inning13 = '-'
            inning14 = '-'
            inning15 = '-'
        elif len(a) == 12 :
            inning7 = abs(sum(a[0 : 6]) - sum(b[0 : 6]))
            inning8 = abs(sum(a[0 : 7]) - sum(b[0 : 7]))
            inning9 = abs(sum(a[0 : 8]) - sum(b[0 : 8]))
            inning10 = abs(sum(a[0 : 9]) - sum(b[0 : 9]))
            inning11 = abs(sum(a[0 : 10]) - sum(b[0 : 10]))
            inning12 = abs(sum(a[0 : 11]) - sum(b[0 : 11]))
            inning13 = '-'
            inning14 = '-'
            inning15 = '-'
        elif len(a) == 13 :
            inning7 = abs(sum(a[0 : 6]) - sum(b[0 : 6]))
            inning8 = abs(sum(a[0 : 7]) - sum(b[0 : 7]))
            inning9 = abs(sum(a[0 : 8]) - sum(b[0 : 8]))
            inning10 = abs(sum(a[0 : 9]) - sum(b[0 : 9]))
            inning11 = abs(sum(a[0 : 10]) - sum(b[0 : 10]))
            inning12 = abs(sum(a[0 : 11]) - sum(b[0 : 11]))
            inning13 = abs(sum(a[0 : 12]) - sum(b[0 : 12]))
            inning14 = '-'
            inning15 = '-'
        elif len(a) == 14 :
            inning7 = abs(sum(a[0 : 6]) - sum(b[0 : 6]))
            inning8 = abs(sum(a[0 : 7]) - sum(b[0 : 7]))
            inning9 = abs(sum(a[0 : 8]) - sum(b[0 : 8]))
            inning10 = abs(sum(a[0 : 9]) - sum(b[0 : 9]))
            inning11 = abs(sum(a[0 : 10]) - sum(b[0 : 10]))
            inning12 = abs(sum(a[0 : 11]) - sum(b[0 : 11]))
            inning13 = abs(sum(a[0 : 12]) - sum(b[0 : 12]))
            inning14 = abs(sum(a[0 : 13]) - sum(b[0 : 13]))
            inning15 = '-'
        elif len(a) == 15 :
            inning7 = abs(sum(a[0 : 6]) - sum(b[0 : 6]))
            inning8 = abs(sum(a[0 : 7]) - sum(b[0 : 7]))
            inning9 = abs(sum(a[0 : 8]) - sum(b[0 : 8]))
            inning10 = abs(sum(a[0 : 9]) - sum(b[0 : 9]))
            inning11 = abs(sum(a[0 : 10]) - sum(b[0 : 10]))
            inning12 = abs(sum(a[0 : 11]) - sum(b[0 : 11]))
            inning13 = abs(sum(a[0 : 12]) - sum(b[0 : 12]))
            inning14 = abs(sum(a[0 : 13]) - sum(b[0 : 13]))
            inning15 = abs(sum(a[0 : 14]) - sum(b[0 : 14]))
        else :
            pass
        rows.append([date, stadium, runtime, inning7, inning8, inning9, inning10, inning11, inning12, inning13, inning14, inning15])
    
    df_1 = pd.DataFrame(rows, columns = columns)
    df_2 = pd.DataFrame({'경기': match_info})
    df = pd.concat([df_1,df_2], axis = 1)
    df = df[['일자','경기', '구장', '경기시간', '7회점수차', '8회점수차', '9회점수차', '10회점수차', '11회점수차',
           '12회점수차','13회점수차','14회점수차','15회점수차']]
    year = df['일자'][0].split('(')[0].split('.')[0]
    df.to_excel(f'./kbo/kbo_{year}_postseason.xlsx')
    time.sleep(3)
    
    result2 = driver.find_element_by_id('snb')
    result2.find_elements_by_tag_name('li')[2].click()
    time.sleep(3)

driver = webdriver.Firefox(executable_path = r'C:\Users\JngMK\Desktop\2021KNUpython2/geckodriver')
url = 'https://www.koreabaseball.com/Schedule/GameCenter/Main.aspx?gameDate=20211101&gameId=20211101WOOB0&section=REVIEW'
driver.get(url)
time.sleep(10)
result1 = driver.find_element_by_id('lnb')
result1.find_element_by_tag_name('li').click()
time.sleep(5)
result2 = driver.find_element_by_id('snb')
result2.find_elements_by_tag_name('li')[2].click()
time.sleep(5)

# 0 : 2021 ~ 4 : 2017

for i in range(5):
    post_season(i)
    regular_season(i)
