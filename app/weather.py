import requests
import json
from utils.logger import setup_logger
from fuzzywuzzy import process
from datetime import date


class WeatherService:
    def __init__(self):
        self.logger = setup_logger()
        self.url = 'http://t.weather.sojson.com/api/weather/city/'

    def get_weather(self, city='北京'):
        try:
            with open('data/city.json', 'r', encoding='utf-8') as f:
                cities = json.load(f)
                city_code = cities.get(city)
        except Exception as e:
            self.logger.error(f"读取城市代码出错: {e}")
            return None

        if not city_code:
            self.logger.warning(f"未找到城市代码: {city}")
            return None

        try:
            response = requests.get(self.url + city_code)
            data = response.json()
        except Exception as e:
            self.logger.error(f"获取天气数据出错: {e}")
            return None

        if data['status'] == 200:
            weather_map = {
                "晴天": ["☀️", "晴朗无云，适合户外活动。"],
                "多云": ["🌥️", "天空多云，气温适宜。"],
                "小雨": ["🌧️", "可能会有小雨，出门记得带伞。"],
                "阴天": ["☁️", "阴天，气温稍低。"]
            }

            weather_type = data["data"]["forecast"][0]["type"]
            weather_types = list(weather_map.keys())
            best_match = process.extractOne(weather_type, weather_types)

            icon = weather_map.get(best_match[0], ["", ""])[0]
            description = weather_map.get(best_match[0], ["", ""])[1]

            weather_info = f"""
            ### {date.today()} {icon} {weather_type}
            - **城市**：{data["cityInfo"]["city"]}
            - **最高温度**：{data["data"]["forecast"][0]["high"]}
            - **最低温度**：{data["data"]["forecast"][0]["low"]}
            - **详情**：{description}
            """
            self.logger.info(f"天气查询成功: {city}, 天气: {weather_type}")
            return weather_info
        else:
            self.logger.warning(f"获取天气数据失败，状态码: {data['status']}")
            return f"查询失败，未找到{city}的天气数据"

if __name__ == '__main__':
    weateher = WeatherService()
    weateher.get_weather()