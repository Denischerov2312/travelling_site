import os
import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server


def get_files_path(folder):
    files = []
    for file_name in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, file_name)):
            files.append(os.path.join(folder, file_name))
    return files


def get_file_content(file_name):
    with open(file_name, 'r', encoding='utf8') as my_file:
        files_content = json.load(my_file)
    return files_content


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')

    towns = {
        'Архангельск': 'Arkhangelsk',
        'Астрахань': 'Astrakhan',
        'Владивосток': 'Vladivostok',
        'Владимир': 'Vladimir',
        'Волгоград': 'Volgograd',
        'Воронеж': 'Voronezh',
        'Казань': 'Kazan',
        'Калининград': 'Kaliningrad',
        'Москва': 'Moscow',
        'Нижний Новгород': 'Nizhny_Novgorod',
        'Ростов': 'Rostov-on-Don',
        'Санкт-Петербург': 'Saint_Petersburg',
        'Сочи': 'Sochi',
        'Тобольск': 'Tobolsk'
    }

    city_weather = get_file_content('weather/weather.json')
    cities = get_files_path('cities')
    city = city_weather['city']
    for ru_town, eng_town in towns.items():
        city = city.replace(ru_town, eng_town)
    city_index = cities.index(f'cities\\{city}.json')
    city_excursions = get_file_content(cities[city_index])

    rendered_page = template.render(
        excursions=city_excursions,
        weather=city_weather
    )
    with open('pages/index.html', 'w', encoding='utf8') as file:
        file.write(rendered_page)


def main():
    Path('pages').mkdir(parents=True, exist_ok=True)
    on_reload()

    server = Server()
    server.watch('template.html', on_reload)
    server.watch('weather/weather.json', on_reload)
    server.serve(root='.',  default_filename='pages/index.html')


if __name__ == '__main__':
    main()
