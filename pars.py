from bs4 import BeautifulSoup
import requests
import json
import os
from pathlib import Path
from os.path import join
import random

def parse_excursions(response, city):
    soup = BeautifulSoup(response.text, "html.parser")
    cards = soup.find_all(class_='exp-list-item-wrapper exp-snippet')
    city_name = soup.select_one("nav[class=location-crumbs]").find_all("span")[3].text

    excursions=[]

    for card in cards:
        title_text = card.find(class_='title').text.strip()
        description = card.find(class_='tagline').text.strip()
        duration = card.find(class_='duration')
        movement = card.find(class_='movement').text.strip()
        datetime = card.find(class_='dates')
        payment = card.find(class_='price-actual').text.strip()
        quantity = card.find(class_='price-for').text.strip()
        img_url = card.find('img', class_='exp-pic lazy-image')['src']
        img_path = download_image(img_url, f'{random.randint(1000000, 1000000000)}.jpeg', f'excursions_images/{city}')
        if duration:
            time = duration.text.strip()
        else:
            time = 'Время экскурсии будет объявлено позднее'

        if datetime:
            date = datetime.text.strip()
        else:
            date = 'Ежедневно'

        excursions.append({
            'city_name': city_name,
            'title_text': title_text,
            'description': description,
            'duration': time,
            'movement': movement,
            'datetime': date,
            'payment': payment,
            'quantity': quantity,
            'image_url': img_url,
            'img_path': img_path
        })
    return excursions
    
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

for city in cities:
    url = f'https://experience.tripster.ru/experience/{city}'

    all_activities = []

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
            all_activities.append(parse_excursions(page_response, city))
    else:
        all_activities.append(parse_excursions(city_response, city))

    with open(f'cities/{city}.json', 'w', encoding='utf8') as outfile:
        json.dump(all_activities, outfile, ensure_ascii=False,)

# if __name__ == '__main__':
#     parse_excursions()