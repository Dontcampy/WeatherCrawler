##Weather Crawler 天气爬虫##
##Author:Dontcampy##

import re
from bs4 import BeautifulSoup
import requests
from  collections import deque

#Function
def getLocation(soup):
    # location
    country = soup.find(id='country-breadcrumbs')
    location0 = country.find_all('li')[0].text #全球
    location1 = country.find_all('li')[1].text #大洲
    location2 = country.find_all('li')[2].text #国家
    location3 = country.find_all('li')[3].text #城市
    location4 = country.find_all('li')[4].text #具体地址：市，区，县，街道，特殊地点

def getDayInform(soup): #Get day information and highest temperature
    panel = soup.find(class_ = 'detail-tab-panel')
    time = panel.find(class_ = 'day muted')
    hi_temp = time.find(class_ = 'temp').text

    #RealFeel®
    realfeel = time.find_all(class_ = 'realfeel')
    realfeel_temp = realfeel[0].text
    realfeel_rain = realfeel[1].text

    #wind,rain,UV
    misc = time.find_all('strong')
    misc_wind = misc[0].text #风速风向
    misc_gust = misc[1].text #阵风风速
    misc_UV = misc[2].text #最高紫外线指数
    misc_storm = misc[3].text #雷雨
    misc_water = misc[4].text #降水
    misc_rain = misc[5].text #雨
    misc_snow = misc[6].text #雪
    misc_ice = misc[7].text #冰冻


    print(hi_temp + realfeel_temp + realfeel_rain + misc_wind + misc_gust + misc_UV + misc_storm + misc_water + misc_rain + misc_snow + misc_ice)

def getNightInform(soup): #Get night information and lowest temperature
    panel = soup.find(class_='detail-tab-panel')
    time = panel.find(class_ = 'night')
    low_temp = time.find(class_ = 'temp').text

    # RealFeel®
    realfeel = time.find_all(class_='realfeel')
    realfeel_temp = realfeel[0].text
    realfeel_rain = realfeel[1].text

    # wind,rain,UV
    misc = time.find_all('strong')
    misc_wind = misc[0].text  # 风速风向
    misc_gust = misc[1].text  # 阵风风速
    misc_UV = misc[2].text  # 最高紫外线指数
    misc_storm = misc[3].text  # 雷雨
    misc_water = misc[4].text  # 降水
    misc_rain = misc[5].text  # 雨
    misc_snow = misc[6].text  # 雪
    misc_ice = misc[7].text  # 冰冻

    print(low_temp + realfeel_temp + realfeel_rain + misc_wind + misc_gust + misc_UV + misc_storm + misc_water + misc_rain + misc_snow + misc_ice)


