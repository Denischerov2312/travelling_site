import requests
import json
from pathlib import Path


def get_weather(sity):
    Path('weather').mkdir(parents=True, exist_ok=True)
    url = 'http://api.weatherapi.com/v1/current.json'
    payload = {
        'key': 'e11a050020a94a0da64171440241907',
        'q': sity,
        'lang': 'ru',
    }
    response = requests.get(url=url, params=payload)

    kmh = response.json()['current']['wind_kph']
    wind_speed = int(kmh * 0.2777777777777778)

    wind_dir = response.json()['current']['wind_dir']
    for eng_letter, ru_letter in {"N": "C", "S": "Ю", 'W': 'З', 'E': 'В'}.items():
        wind_dir = wind_dir.replace(eng_letter, ru_letter)

    weather = {
        'temp': response.json()['current']['temp_c'],
        'condition': response.json()['current']['condition']['text'],
        'humidity': response.json()['current']['humidity'],
        'wind_speed': wind_speed,
        'wind_dir': wind_dir
        }

    with open(f"weather/{sity}", "w", encoding='utf8') as file:
        json.dump(weather, file, ensure_ascii=False)
    return weather
