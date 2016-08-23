##爬取AccuWeather网站并生成列表 仅中国地区
##请一口气运行完
import requests
import re
import time
from requests import exceptions
from collections import deque
from bs4 import BeautifulSoup


file_visitedR = open('visited.txt', 'r') #读取已访问列表
file_weblistR = open('weblist.txt', 'r') #读取爬虫列表
file_queue = open('queue.txt', 'w+') #读取queue（如果有）

queue = deque(file_queue.readlines())
file_queue.close()
#初始化已访问列表,防止重复爬取url
visited = set(file_visitedR.readline().split(';'))
file_visitedR.close()

# 初始化爬虫列表
webList = set(file_weblistR.readline().split(';'))
file_weblistR.close()

url = "http://www.accuweather.com/zh/browse-locations/asi/cn" #爬虫入口

queue.append(url)
cnt = 0


while queue:
    url = queue.popleft()#网页出队等待爬取
    visited.add(url)#标记该url已访问

    file_visitedA = open('visited.txt', 'a')
    file_visitedA.write(url + ';')
    file_visitedA.close()

    print('已经抓取: ' + str(cnt) + '   正在抓取 <---  ' + url)
    cnt += 1

    try:
        response = requests.get(url, timeout = 180)
        soup = BeautifulSoup(response.text)
    #出现错误将重试3次（超过3次将停止程序），并输出至errorLog.txt
    except ConnectionError:
        try:
            print('出现异常，正在尝试重新连接（1）...')
            response = requests.get(url, timeout=180)
            soup = BeautifulSoup(response.text)
        except requests.exceptions.RequestException as log:
            try:
                print('出现异常，正在尝试重新连接（2）...')
                response = requests.get(url, timeout=180)
                soup = BeautifulSoup(response.text)
            except requests.exceptions.RequestException as log:
                try:
                    print('出现异常，正在尝试重新连接（3）...')
                    response = requests.get(url, timeout=180)
                    soup = BeautifulSoup(response.text)
                except requests.exceptions.RequestException as log:
                    errorLog = open('errorLog.txt', 'a')
                    errorLog.write(time.strftime('[' + "%a, %d %b %Y %H:%M:%S", time.localtime()) + ']' + str(log) + '\r\n')
                    errorLog.close()
                    queue_save = open('queue.txt', 'w')
                    queue_save.writelines(list(queue))
                    queue_save.close()
                    print('连接失败，异常内容：' + str(log))
                    exit()

    #爬取主爬虫列表
    match_webList = re.match(r'http://www.accuweather.com/zh/cn/(.*)/daily-weather-forecast/(.*)?day=1', url, re.I)
    if match_webList and url not in webList:
        webList.add(url)
        file_weblistA = open('weblist.txt', 'a')
        file_weblistA.write(url + ';')
        file_weblistA.close()
        print('已将：' + url + ' 加入爬虫列表')

    #爬取所有链接
    for link in soup.find_all('a'):
        url = str(link.get('href'))
        match_queue1 = re.match(r'http://www.accuweather.com/zh/browse-locations/asi/cn', url, re.I)
        match_queue2 = re.match(r'http://www.accuweather.com/zh/cn/-/(.*)/weather-forecast', url, re.I)
        match_webList = re.match(r'http://www.accuweather.com/zh/cn/(.*)/daily-weather-forecast/(.*)?day=1', url, re.I)
        if (match_queue1 or match_queue2 or match_webList) and (url not in visited):
            queue.append(url)
            print('加入队列 --->  ' + url)
            visited.add(url)

print('========== webList爬取完成 ===========')