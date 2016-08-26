##Weather Crawler 天气爬虫##
##Author:Dontcampy##

import re
from bs4 import BeautifulSoup
import requests
from requests import exceptions
from  collections import deque
import sqlite3
import time

##Function##
############
def getLocation(soup):
    # location
    location = soup.find(id = 'country-breadcrumbs')
    #Loc_global = location.find_all('li')[0].text #全球
    Loc_continent = location.find_all('li')[1].text #大洲
    Loc_country = location.find_all('li')[2].text #国家
    Loc_city = location.find_all('li')[3].text #城市
    Loc_name = location.find_all('li')[4].text #具体地址：市，区，县，街道，特殊地点

    location = soup.find(id = 'current-city-tab')
    link = location.find('a')
    url = str(link.get('href'))
    match = re.match(r'http://www.accuweather.com/zh/cn/(.*)/(.*)/.*/.*', url, re.I)

    Loc_nameEn = match.group(1) #地区英文名(小写，仅供搜索使用)
    Loc_ID = int(match.group(2)) #地区ID

    return Loc_ID, Loc_continent, Loc_country, Loc_city, Loc_name, Loc_nameEn



#Get day information and highest temperature
def getDayInform(soup):
    panel = soup.find(class_ = 'detail-tab-panel')
    try:
        stime = panel.find(class_ = 'day muted')
        match = re.search(r'(\d+)', stime.find(class_ = 'temp').text)
        hi_temp = int(match.group(1))
    except AttributeError:
        stime = panel.find(class_='day')
        match = re.search(r'(\d+)', stime.find(class_='temp').text)
        hi_temp = int(match.group(1))

    # Condition
    desc = stime.find(class_='desc')
    condition = desc.find_all('p')
    wea_condition = condition[4].text

    #RealFeel®
    realfeel = stime.find_all(class_ = 'realfeel')

    match = re.search(r'(\d+)', realfeel[0].text)
    realfeel_temp = int(match.group(1))

    match = re.search(r'(\d+)', realfeel[1].text)
    realfeel_rain = int(match.group(1))

    # wind,rain,UV
    misc = stime.find_all('strong')
    # 风速风向
    misc_wind = misc[0].text
    # 阵风风速
    match = re.search(r'(\d+)', misc[1].text)
    misc_gust = int(match.group(1))
    # 最高紫外线指数
    misc_UV = misc[2].text
    # 雷雨
    match = re.search(r'(\d+)', misc[3].text)
    misc_storm = int(match.group(1))
    # 降水
    match = re.search(r'(\d+)', misc[4].text)
    misc_water = int(match.group(1))
    # 雨
    match = re.search(r'(\d+)', misc[5].text)
    misc_rain = int(match.group(1))
    # 雪
    match = re.search(r'(\d+)', misc[6].text)
    misc_snow = int(match.group(1))
    # 冰冻
    match = re.search(r'(\d+)', misc[7].text)
    misc_ice = int(match.group(1))

    return hi_temp, wea_condition, realfeel_temp, realfeel_rain, misc_wind, misc_gust, misc_UV, misc_storm, misc_water, misc_rain, misc_snow, misc_ice

#Get night information and lowest temperature
def getNightInform(soup):
    panel = soup.find(class_='detail-tab-panel')
    stime = panel.find(class_ = 'night')
    match = re.search(r'(\d+)', stime.find(class_='temp').text)
    low_temp = int(match.group(1))

    # RealFeel®
    realfeel = stime.find_all(class_ = 'realfeel')

    match = re.search(r'(\d+)', realfeel[0].text)
    realfeel_temp = int(match.group(1))

    match = re.search(r'(\d+)', realfeel[1].text)
    realfeel_rain = int(match.group(1))

    # Condition
    desc = stime.find(class_='desc')
    condition = desc.find_all('p')
    wea_condition = condition[4].text

    # wind,rain,UV
    misc = stime.find_all('strong')
    # 风速风向
    misc_wind = misc[0].text
    # 阵风风速
    match = re.search(r'(\d+)', misc[1].text)
    misc_gust = int(match.group(1))
    # 最高紫外线指数
    misc_UV = misc[2].text
    # 雷雨
    match = re.search(r'(\d+)', misc[3].text)
    misc_storm = int(match.group(1))
    # 降水
    match = re.search(r'(\d+)', misc[4].text)
    misc_water = int(match.group(1))
    # 雨
    match = re.search(r'(\d+)', misc[5].text)
    misc_rain = int(match.group(1))
    # 雪
    match = re.search(r'(\d+)', misc[6].text)
    misc_snow = int(match.group(1))
    # 冰冻
    match = re.search(r'(\d+)', misc[7].text)
    misc_ice = int(match.group(1))

    return low_temp, wea_condition, realfeel_temp, realfeel_rain, misc_wind, misc_gust, misc_UV, misc_storm, misc_water, misc_rain, misc_snow, misc_ice
##########
## Main ##
##########
file_weblistR = open('weblist.txt', 'r') #读取爬虫列表
webList = file_weblistR.readline().split(';')
webList.pop() # 去除最后一个;造成的空元素

# 数据库初始化
conn = sqlite3.connect('data.db')
print('Opened database successfully')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS TEMP_WEATHER
            (
            ID INT PRIMARY KEY     NOT NULL,
            CONTINENT      TEXT    NOT NULL,
            COUNTRY        TEXT    NOT NULL,
            CITY           TEXT    NOT NULL,
            NAME           TEXT    NOT NULL,
            NAME_EN        TEXT    NOT NULL,
            TEMPERATURE_H  INT    ,
            CONDITION      TEXT    ,
            REALFEEL_T     INT    ,
            REALFEEL_R     INT    ,
            WIND           TEXT    ,
            GUST           INT    ,
            UV             TEXT    ,
            STORM          INT    ,
            WATER          INT    ,
            RAIN           INT    ,
            SNOW           INT    ,
            ICE            INT    ,
            TEMPERATURE_L  INT    ,
            CONDITION_N    TEXT    ,
            REALFEEL_T_N   INT    ,
            REALFEEL_R_N   INT    ,
            WIND_N         TEXT    ,
            GUST_N         INT    ,
            UV_N           TEXT    ,
            STORM_N        INT    ,
            WATER_N        INT    ,
            RAIN_N         INT    ,
            SNOW_N         INT    ,
            ICE_N          INT    ,
            UPDATE_TIME    TEXT    );''')


while webList:

    url = webList.pop()
    try:
        response = requests.get(url, timeout = 60)
        soup = BeautifulSoup(response.text)
    #异常处理，出现错误将重试3次（超过3次将停止程序），并输出至errorLog.txt
    except requests.exceptions.RequestException :
        try:
            print('出现异常，正在尝试重新连接（1）...')
            response = requests.get(url, timeout = 120)
            soup = BeautifulSoup(response.text)
        except requests.exceptions.RequestException:
            try:
                print('出现异常，正在尝试重新连接（2）...')
                response = requests.get(url, timeout = 240)
                soup = BeautifulSoup(response.text)
            except requests.exceptions.RequestException:
                try:
                    print('出现异常，正在尝试重新连接（3）...')
                    response = requests.get(url, timeout = 360)
                    soup = BeautifulSoup(response.text)
                except requests.exceptions.RequestException as log:
                    errorLog = open('errorLog.txt', 'a')
                    errorLog.write(time.strftime('[' + "%a, %d %b %Y %H:%M:%S", time.localtime()) + ']' + str(log) + '\n')
                    errorLog.close()
                    webList.append(url)
                    queue_save = open('queue.txt', 'w')
                    queue_save.write(';'.join(webList))
                    queue_save.close()
                    print('连接失败，异常内容：' + str(log))
                    exit()

    Location = getLocation(soup)
    DayInform = getDayInform(soup)
    NightInform = getNightInform(soup)
    upTime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())

    #写入数据库 build
    cur.execute("INSERT INTO TEMP_WEATHER(ID, CONTINENT, COUNTRY, CITY, NAME, NAME_EN) \
                VALUES(?,?,?,?,?,?)", Location)
    # cur.execute('''UPDATE TEMP_WEATHER
    #                 set TEMPERATURE_H = ?, CONDITION = ?, REALFEEL_T = ?, REALFEEL_R = ?, WIND = ?, GUST = ?, UV = ?, STORM = ?, WATER = ?, RAIN = ?, SNOW = ?, ICE = ?,
    #                     TEMPERATURE_L = ?, CONDITION_N = ?, REALFEEL_T_N = ?, REALFEEL_R_N = ?, WIND_N = ?, GUST_N = ?, UV_N = ?, STORM_N = ?, WATER_N = ?, RAIN_N = ?, SNOW_N = ?, ICE_N = ?,
    #                     UPDATE_TIME = ? WHERE ID = ?''', (DayInform[0], DayInform[1], DayInform[2], DayInform[3], DayInform[4], DayInform[5], DayInform[6], DayInform[7], DayInform[8], DayInform[9], DayInform[10], DayInform[11],
    #                                                             NightInform[0], NightInform[1], NightInform[2], NightInform[3], NightInform[4], NightInform[5], NightInform[6], NightInform[7], NightInform[8], NightInform[9], NightInform[10], NightInform[11],
    #                                                             upTime, Location[0]))
    conn.commit()

conn.close()