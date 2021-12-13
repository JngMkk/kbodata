import os
import math
import pandas as pd

def cal_dist(x1, y1, x2, y2, a, b):
    area = abs((x1-a) * (y2-b) - (y1-b) * (x2 - a))
    AB = ((x1-x2)**2 + (y1-y2)**2) **0.5
    distance = area/AB
    return distance

class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

path = "./cd_report/"
file_lst = os.listdir(path)

ref = []
for file in file_lst:
    name = file.split('_')[2].split('.')[0]
    if name not in ref:
        ref.append(name)
    else :
        continue

columns = ['이닝', 'x좌표', 'y좌표', '판정']
for i in ref:
    df = pd.DataFrame(columns = columns)
    for file in file_lst:
        if i in file:
            df = df.append(pd.read_excel(f'./cd_report/{file}', index_col = 0), ignore_index = True)
        else :
            continue
    df.sort_values(by = '이닝', ascending = True, inplace = True)
    df = df.reset_index(drop = True)
    df.index.names = [f'{i}']
    df['이닝']= df['이닝'].replace([1,2,3],'초반')
    df['이닝'] = df['이닝'].replace([4,5,6], '중반')
    df['이닝'] = df['이닝'].replace([7,8,9], '후반')
    df.to_csv(f'./ref/{i}.csv', encoding = 'euc-kr')

path1 = "./ref/"
file_lst1 = os.listdir(path1)

rows = []
columns = ['심판', '초반', '후반']
for file in file_lst1:
    df = pd.read_csv(f'./ref/{file}', index_col =0 , encoding = 'euc-kr')
    df_s = df[df['판정'] == 0]
    df_early = df_s[df_s['이닝'] == '초반']
    df_early = df_early.reset_index(drop = True)
    df_late = df_s[df_s['이닝'] == '후반']
    df_late = df_late.reset_index(drop = True)
    bsx_1 = []
    bsy_1 = []
    for i in range(len(df_early)):
        row = df_early.loc[i]
        if row[1] < 61.5 or row[1] > 173.5 or row[2] < 81.8 or row[2] > 232.8:
            bsx_1.append(row[1])
            bsy_1.append(row[2])
        else :
            continue
    bsx_2 = []
    bsy_2 = []
    for i in range(len(df_late)):
        row = df_late.loc[i]
        if row[1] < 61.5 or row[1] > 173.5 or row[2] < 81.8 or row[2] > 232.8:
            bsx_2.append(row[1])
            bsy_2.append(row[2])
        else :
            continue
    dist_1 = []
    dist_2 = []
    for pair in zip(bsx_1, bsy_1) :
        if pair[0] <= 61.5 and pair[1] <= 81.8 :
            p1 = point(x = pair[0], y = pair[1])
            p2 = point(x = 61.5, y = 81.8)
            a = p2.x - p1.x
            b = p2.y - p1.y
            c = math.sqrt((a * a) + (b * b))
            dist_1.append(c)
        elif pair[0] <= 61.5 and pair[1] >= 232.8:
            p1 = point(x = pair[0], y = pair[1])
            p2 = point(x = 61.5, y = 232.8)
            a = p2.x - p1.x
            b = p2.y - p1.y
            c = math.sqrt((a * a) + (b * b))
            dist_1.append(c)
        elif pair[0] >= 173.5 and pair[1] <= 81.8:
            p1 = point(x = pair[0], y = pair[1])
            p2 = point(x = 173.5, y = 81.8)
            a = p2.x - p1.x
            b = p2.y - p1.y
            c = math.sqrt((a * a) + (b * b))
            dist_1.append(c)
        elif pair[0] >= 173.5 and pair[1] >= 232.8:
            p1 = point(x = pair[0], y = pair[1])
            p2 = point(x = 173.5, y = 232.8)
            a = p2.x - p1.x
            b = p2.y - p1.y
            c = math.sqrt((a * a) + (b * b))
            dist_1.append(c)
        elif 61.5 < pair[0] < 173.5 and pair[1] < 81.8:
            dist_1.append(cal_dist(61.5, 81.8, 173.5, 81.8, pair[0], pair[1]))
        elif pair[0] > 173.5 and 81.8 < pair[1] < 232.8:
            dist_1.append(cal_dist(173.5, 81.8, 173.5, 232.8, pair[0], pair[1]))
        elif 61.5 < pair[0] < 173.5 and pair[1] > 232.8:
            dist_1.append(cal_dist(61.5 , 232.8, 173.5, 232.8, pair[0], pair[1]))
        elif pair[0] < 61.5 and 81.8 < pair[1] < 232.8:
            dist_1.append(cal_dist(61.5, 81.8, 61.5, 232.8, pair[0], pair[1]))
    for pair in zip(bsx_2, bsy_2) :
        if pair[0] <= 61.5 and pair[1] <= 81.8 :
            p1 = point(x = pair[0], y = pair[1])
            p2 = point(x = 61.5, y = 81.8)
            a = p2.x - p1.x
            b = p2.y - p1.y
            c = math.sqrt((a * a) + (b * b))
            dist_2.append(c)
        elif pair[0] <= 61.5 and pair[1] >= 232.8:
            p1 = point(x = pair[0], y = pair[1])
            p2 = point(x = 61.5, y = 232.8)
            a = p2.x - p1.x
            b = p2.y - p1.y
            c = math.sqrt((a * a) + (b * b))
            dist_2.append(c)
        elif pair[0] >= 173.5 and pair[1] <= 81.8:
            p1 = point(x = pair[0], y = pair[1])
            p2 = point(x = 173.5, y = 81.8)
            a = p2.x - p1.x
            b = p2.y - p1.y
            c = math.sqrt((a * a) + (b * b))
            dist_2.append(c)
        elif pair[0] >= 173.5 and pair[1] >= 232.8:
            p1 = point(x = pair[0], y = pair[1])
            p2 = point(x = 173.5, y = 232.8)
            a = p2.x - p1.x
            b = p2.y - p1.y
            c = math.sqrt((a * a) + (b * b))
            dist_2.append(c)
        elif 61.5 < pair[0] < 173.5 and pair[1] < 81.8:
            dist_2.append(cal_dist(61.5, 81.8, 173.5, 81.8, pair[0], pair[1]))
        elif pair[0] > 173.5 and 81.8 < pair[1] < 232.8:
            dist_2.append(cal_dist(173.5, 81.8, 173.5, 232.8, pair[0], pair[1]))
        elif 61.5 < pair[0] < 173.5 and pair[1] > 232.8:
            dist_2.append(cal_dist(61.5 , 232.8, 173.5, 232.8, pair[0], pair[1]))
        elif pair[0] < 61.5 and 81.8 < pair[1] < 232.8:
            dist_2.append(cal_dist(61.5, 81.8, 61.5, 232.8, pair[0], pair[1]))
    name = file.split('.')[0]
    early = sum(dist_1) / len(bsx_1)
    late = sum(dist_2) / len(bsx_2)
    rows.append([name, early, late])

df = pd.DataFrame(rows, columns = columns)
df.to_csv('./ref/평균거리.csv', encoding = 'euc-kr')