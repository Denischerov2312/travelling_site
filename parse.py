import os
import json
import time
from pathlib import Path
from os.path import join

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def parse_excursions(response, city):
    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.find_all(class_='exp-list-item-wrapper exp-snippet')
    city_name = soup.select_one("nav[class=location-crumbs]").find_all("span")[3].text

    excursions = []

    for card in cards:
        num = card.find(class_='exp-header')['href']
        excursion_url = f'https://experience.tripster.ru{num}'
        title_text = card.find(class_='title').text.strip()
        description = card.find(class_='tagline').text.strip()
        duration = card.find(class_='duration')
        movement = card.find(class_='movement').text.strip()
        datetime = card.find(class_='dates')
        payment = card.find(class_='price-actual').text.strip()
        quantity = find_quantity(card)
        tour_type = find_tour_type(card)
        img_url = card.find('img', class_='exp-pic lazy-image')['src']
        img_name = card.find('img', class_='exp-pic lazy-image')['alt']
        img_name = sanitize_filename(img_name.split('"')[1])
        img_path = download_image(img_url, f'{img_name}.jpeg', fr'excursions_images\{city}')
        if duration:
            time = duration.text.strip()
        else:
            time = 'Время экскурсии будет объявлено позднее'
        if datetime:
            date = datetime.text.strip()
        else:
            date = 'Ежедневно'

        excursions.append({
            'excursion_url': excursion_url,
            'city_name': city_name,
            'title_text': title_text,
            'description': description,
            'duration': time,
            'movement': movement,
            'datetime': date,
            'payment': payment,
            'quantity': quantity,
            'tour_type': tour_type,
            'image_url': img_url,
            'img_path': img_path
        })
    return excursions


def find_tour_type(soup):
    tour_type = soup.find(class_='price-for').text.strip()
    if tour_type.lower() == 'за одного':
        return tour_type.strip()
    else:
        tour_type = tour_type.split(',')
        return tour_type[0].strip()


def find_quantity(soup):
    quantity = soup.find(class_='price-for').text.strip()
    if quantity.lower() == 'за одного':
        return 'Индивидуальная'
    else:
        quantity = quantity.split(',')
        return quantity[1].strip()


def download_image(url, filename, folder):
    try:
        image_response = requests.get(url)
        image_response.raise_for_status()
        os.makedirs(folder, exist_ok=True)
        filepath = join(folder, filename)
        with open(filepath, 'wb') as file:
            file.write(image_response.content)
        return filepath
    except requests.exceptions.HTTPError:
        return None


Path('cities').mkdir(parents=True, exist_ok=True)
cities = [
    'Arkhangelsk',
    'Astrakhan',
    'Vladivostok',
    'Volgograd',
    'Vladimir',
    'Voronezh',
    'Kazan',
    'Kaliningrad',
    'Moscow',
    'Nizhny_Novgorod',
    'Rostov-on-Don',
    'Saint_Petersburg',
    'Sochi',
    'Tobolsk'
]


def main():
    for city in cities:
        url = f'https://experience.tripster.ru/experience/{city}'
        all_activities = []

        try:
            city_response = requests.get(url)
            city_response.raise_for_status()
            city_soup = BeautifulSoup(city_response.text, "html.parser")

            pagination = city_soup.find(class_='pagination')
            if pagination:
                page_count = pagination.find_all('a')
                page_count = int(page_count[-1].text)

                for page_num in range(1, page_count+1):
                    payload = {'page': page_num}
                    page_response = requests.get(url, params=payload)
                    page_response.raise_for_status()
                    [all_activities.append(excursion) for excursion in parse_excursions(page_response, city)]
            else:
                [all_activities.append(excursion) for excursion in parse_excursions(city_response, city)]

            with open(f'cities/{city}.json', 'w', encoding='utf8') as outfile:
                json.dump(all_activities, outfile, ensure_ascii=False,)
        except requests.exceptions.ConnectionError:
            print("Соединение с сайтом прервано.")
            time.sleep(20)


if __name__ == '__main__':
    main()
