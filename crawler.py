##Weather Crawler 天气爬虫##
##Author:Dontcampy##

import re
from bs4 import BeautifulSoup
import requests
from requests import exceptions
import time
import pymongo

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
print('读取完毕，共' + str(len(webList)) + '条。')

# 数据库初始化
client = pymongo.MongoClient("localhost", 27017)
db = client.w_data
cur_weather = db.cur_weather


while webList:

    url = webList.pop()
    print('正在爬取-------->' + url)
    try:
        response = requests.get(url, timeout = 10)
        soup = BeautifulSoup(response.text)
    #异常处理，出现错误将重试3次（超过3次将停止程序），并输出至errorLog.txt
    except requests.exceptions.RequestException :
        try:
            print('出现异常，正在尝试重新连接（1）...')
            response = requests.get(url, timeout = 20)
            soup = BeautifulSoup(response.text)
        except requests.exceptions.RequestException:
            try:
                print('出现异常，正在尝试重新连接（2）...')
                response = requests.get(url, timeout = 40)
                soup = BeautifulSoup(response.text)
            except requests.exceptions.RequestException:
                try:
                    print('出现异常，正在尝试重新连接（3）...')
                    response = requests.get(url, timeout = 80)
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
                    break

    Location = getLocation(soup)
    DayInform = getDayInform(soup)
    NightInform = getNightInform(soup)
    upTime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    All_data = []
    for Ele in Location:
        All_data.append(Ele)
    for Ele in DayInform:
        All_data.append(Ele)
    for Ele in NightInform:
        All_data.append(Ele)
    All_data.append(upTime)
    # 写入数据库 build
    if cur_weather.find_one({'_id': Location[0]}) == None:
        # *Weird indentation
        new_book = {'_id': Location[0],
                    'Location': {'Continent': Location[1], 'Country': Location[2], 'City': Location[3],
                                 'Name': Location[4], 'NameEn': Location[5]},
                    'Weather': [{'Day':
                                     {
                                         'Temperature_hi': DayInform[0],
                                         'Condition': DayInform[1],
                                         'RealFeel_temp': DayInform[2],
                                         'RealFeel_rain': DayInform[3],
                                         'Wind': DayInform[4],
                                         'Gust': DayInform[5],
                                         'UV': DayInform[6],
                                         'Storm': DayInform[7],
                                         'Water': DayInform[8],
                                         'Rain': DayInform[9],
                                         'Snow': DayInform[10],
                                         'Ice': DayInform[11]
                                     },
                                 'Night':
                                     {
                                         'Temperature_hi': NightInform[0],
                                         'Condition': NightInform[1],
                                         'RealFeel_temp': NightInform[2],
                                         'RealFeel_rain': NightInform[3],
                                         'Wind': NightInform[4],
                                         'Gust': NightInform[5],
                                         'UV': NightInform[6],
                                         'Storm': NightInform[7],
                                         'Water': NightInform[8],
                                         'Rain': NightInform[9],
                                         'Snow': NightInform[10],
                                         'Ice': NightInform[11]},
                                 'Update_Time': upTime
                                 }]
                    }
        cur_weather.insert(new_book)
    else:
        # *Weird indentation
        up_book = [{'Day':
                        {
                            'Temperature_hi': DayInform[0],
                            'Condition': DayInform[1],
                            'RealFeel_temp': DayInform[2],
                            'RealFeel_rain': DayInform[3],
                            'Wind': DayInform[4],
                            'Gust': DayInform[5],
                            'UV': DayInform[6],
                            'Storm': DayInform[7],
                            'Water': DayInform[8],
                            'Rain': DayInform[9],
                            'Snow': DayInform[10],
                            'Ice': DayInform[11]
                        },
                    'Night':
                        {
                            'Temperature_hi': NightInform[0],
                            'Condition': NightInform[1],
                            'RealFeel_temp': NightInform[2],
                            'RealFeel_rain': NightInform[3],
                            'Wind': NightInform[4],
                            'Gust': NightInform[5],
                            'UV': NightInform[6],
                            'Storm': NightInform[7],
                            'Water': NightInform[8],
                            'Rain': NightInform[9],
                            'Snow': NightInform[10],
                            'Ice': NightInform[11]
                        },
                    'Update_Time': upTime
                    }]
        # *Weird indentation。。。。。。
        cur_weather.update({'_id': Location[0]}, {'$push': {'Weather': {'$each': up_book, '$position': 0}}})



print('爬虫爬取完毕')
