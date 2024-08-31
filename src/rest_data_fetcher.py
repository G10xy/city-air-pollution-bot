import requests
from datetime import datetime

OWM_API_KEY = ''

class RestDataFetcher:
    def get_coordinates(self, city_name):
        url = f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}&appid={OWM_API_KEY}'
        response = requests.get(url)
        data = response.json()
        return data[0]['lat'], data[0]['lon']

    def get_current_air_quality(self, lat, lon):
        url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OWM_API_KEY}'
        response = requests.get(url)
        return response.json()

    def get_forecast_air_quality(self, lat, lon):
        url = f'http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={lat}&lon={lon}&appid={OWM_API_KEY}'
        response = requests.get(url)
        return response.json()

    def get_historical_air_quality(self, lat, lon):
        current_datetime = datetime.now()
        current_timestamp = int(current_datetime.timestamp())
        one_week_ago_timestamp = current_timestamp - (7 * 24 * 60 * 60)
        url = f'http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={one_week_ago_timestamp}&end={current_timestamp}&appid={OWM_API_KEY}'
        response = requests.get(url)
        return response.json()
