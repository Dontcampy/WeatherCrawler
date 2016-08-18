##Weather Crawler 天气爬虫##
##Author:Dontcampy##

import  urllib.parse
import urllib.request

##url生成 test
value = {}
value['word'] = 'shanghai/106577/weather-forecast/106577'
url_value = urllib.parse.urlencode(value)
url = "http://www.accuweather.com/zh/cn/"
url_full = url + url_value

##浏览器伪装防反爬虫
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'Connection': 'keep-alive',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}

##开爬 test
data = urllib.request.urlopen(url_full).read()
data = data.decode('UTF-8')
print(data)
