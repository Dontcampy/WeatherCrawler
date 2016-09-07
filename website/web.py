from flask import Flask, url_for, render_template, request
from flask_bootstrap import Bootstrap
import pymongo

# 数据库初始化
client = pymongo.MongoClient("localhost", 27017)
db = client.w_data
cur_weather = db.cur_weather

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather/<name>')
def weather(name):
    data = cur_weather.find_one({'Location.NameEn': name})
    location = data['Location']
    name = '天气-' + location['Name']
    name1 = location['Name']
    weather = data['Weather']
    day = weather[0]['Day']
    night = weather[0]['Night']
    # 记得改Temperature_low
    return render_template('weather.html', name = name, day = day, night = night, name1 = name1,
                           Update_Time = weather[0]['Update_Time'],
                           Temperature_hi = day['Temperature_hi'], Condition = day['Condition'],
                           RealFeel_temp = day['RealFeel_temp'], RealFeel_rain = day['RealFeel_rain'],
                           Wind = day['Wind'], Gust = day['Gust'], UV = day['UV'], Storm = day['Storm'],
                           Water = day['Water'], Rain = day['Rain'], Snow = day['Snow'], Ice = day['Ice'],
                           WaterHour = day['WaterHour'], RainHour = day['RainHour'],
                           Temperature_low = night['Temperature_low'], ConditionN = night['Condition'],
                           RealFeel_tempN = night['RealFeel_temp'], RealFeel_rainN = night['RealFeel_rain'],
                           WindN = night['Wind'], GustN = night['Gust'], UVN = night['UV'], StormN = night['Storm'],
                           WaterN = night['Water'], RainN = night['Rain'], SnowN = night['Snow'], IceN = night['Ice'],
                           WaterHourN = night['WaterHour'], RainHourN = night['RainHour']
                           )

@app.route('/search')
def search():
    key = request.args.get('key')
    data = cur_weather.find_one({'$or': [{'Location.NameEn': {'$regex': key, '$options':'i'}},
                                         {'Location.Name': {'$regex': key, '$options':'m'}}]})
    location = data['Location']
    result = location['Name']
    name = location['NameEn']
    weather = data['Weather']
    day = weather[0]['Day']
    night = weather[0]['Night']

    return render_template('search.html', name = name, result = result, temperature_hi = day['Temperature_hi'],
                           temperature_low = night['Temperature_low'])



if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)