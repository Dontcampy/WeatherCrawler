##爬取AccuWeather网站并生成列表 仅中国地区

from  collections import deque
from bs4 import BeautifulSoup
import requests

file_weblist = open('weblist.txt', 'a+') #读取爬虫列表，以备追加
file_visited = open('visited.txt', 'a+') #读取已访问列表，以备追加

queue = deque()
#初始化已访问列表,防止重复爬取url
visited = set(file_visited.readline().split(';'))

# 初始化爬虫列表
webList = set(file_weblist.readline().split(';'))

url = "http://www.accuweather.com/zh/browse-locations/asi/cn" #爬虫入口

queue.append(url)
cnt = 0

while queue:
    url = queue.popleft()#网页出队等待爬取
    visited.add(url)#标记该url已访问
    file_visited.write(url + ';')

    print('已经抓取: ' + str(cnt) + '   正在抓取 <---  ' + url)
    cnt += 1

    response = requests.get(url)
    soup = BeautifulSoup(response.text)

    #爬取主爬虫列表
    if 'day=1' in url and url not in webList:
        webList.add(url)
        file_weblist.write(url + ';')
        print('已将：' + url + ' 加入爬虫列表')

    #爬取所有链接 *need a more efficient method
    for link in soup.find_all('a'):
        x = str(link.get('href'))
        if 'cn' in x and 'http' in x and x not in visited:
            queue.append(x)
            print('加入队列 --->  ' + x)


file_weblist.close()

file_visited.close()
