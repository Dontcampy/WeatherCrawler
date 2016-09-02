import pymongo

# 数据库初始化
client = pymongo.MongoClient("localhost", 27017)
db = client.w_data
cur_weather = db.cur_weather # 实时天气
day_weather = db.day_weather # 统计概况天气


for i in cur_weather.find():
    if day_weather.find_one({'_id': i['_id']}):
        book = [i['Weather'][0]]
        day_weather.update({'_id': day_weather['id']}, {'$push': {'Weather': {'$each': book, '$position': 0}}})

    else:
        weather = i['Weather'][0]
        book = {'_id': i['_id'], 'Location': i['Location'], 'Weather': [weather]}
        day_weather.insert(book)

