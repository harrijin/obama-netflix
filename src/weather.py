import datetime
import requests
from enum import Enum
from typing import Dict, Tuple
import pgeocode

NOMI = pgeocode.Nominatim('us')

class WeatherCondition(Enum):
    SUNNY = 0
    CLOUDY = 1
    FOG = 2
    RAIN = 3
    SNOW = 4

class WeatherForecast:
    forecast: Dict[datetime.datetime, WeatherCondition]

    def __init__(
        self,
        zip_code: str,
    ):
        self.forecast = {}
        lat, lon = self._get_lat_lon(zip_code)
        try:
            for i in range(4):
                points_response = requests.get(f'https://api.weather.gov/points/{lat},{lon}')
                if points_response.status_code == 200:
                    break
            for i in range(4):
                hourly_forecast_response = requests.get(str(points_response.json()['properties']['forecastHourly']))
                if hourly_forecast_response == 200:
                    break
            hourly_forecast = hourly_forecast_response.json()['properties']['periods']
            for period in hourly_forecast:
                key = datetime.datetime.fromisoformat(period['startTime'])
                key = key.replace(tzinfo=None)
                self.forecast[key] = self._parse_weather_condition(period['shortForecast'])
        except:
            print("WARNING: Unable to retrieve weather data. Not applying weather constraints")

    def _get_lat_lon(self, zip_code: str) -> Tuple[float, float]:
        query = NOMI.query_postal_code(zip_code)
        return (query["latitude"], query["longitude"])

    def _parse_weather_condition(self, weather_condition_str: str) -> WeatherCondition:
        weather_condition_str = weather_condition_str.lower()
        if 'sunny' in weather_condition_str:
            return WeatherCondition.SUNNY
        if 'cloudy' in weather_condition_str:
            return WeatherCondition.CLOUDY
        if 'fog' in weather_condition_str:
            return WeatherCondition.FOG
        if (
            'snow' in weather_condition_str or
            'sleet' in weather_condition_str or
            'hail' in weather_condition_str
        ):
            return WeatherCondition.SNOW
        if 'rain' in weather_condition_str:
            return WeatherCondition.RAIN
        return WeatherCondition.SUNNY

    def check_weather(self, query: datetime) -> WeatherCondition:
        key = datetime.datetime(query.year, query.month, query.day, query.hour)
        return self.forecast.get(key, WeatherCondition.SUNNY)