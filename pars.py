from bs4 import BeautifulSoup
import requests
import json


url = "https://www.sputnik8.com/ru/nizhnynovgorod?filters[category][slug]=top10&filters[sort]=reviews_count"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")



cards = soup.find_all(class_='activity-card_n0wr gtm-activity-card activity-card_new_xjRx')

excursions=[]

for card in cards:
    title_text = card.find(class_='heading_0NyQ heading_tag_div heading_size_h4_HrI1 heading_color_black heading_weight_bold_Ed7c title_xIA3').text.strip()
    description = card.find(class_='text-string_8e2Q text-string_size_s_lvye text-string_color_grey_vowO description_phiK').text.strip()
    type_excursion = card.find(class_='wrap_Pp7D wrap_margin_none_rTLS details_ZBWU').text.strip()
    datetime = card.find(class_='events_UOUT')
    payment = card.find(class_='value_uU6k').text.strip()
    quantity = card.find(class_='text-string_8e2Q text-string_size_xs_sqUc price-type_v+Gt').text.strip()
    if datetime is not None:
        time = datetime.text.strip()
    else:
        time = None

    excursions.append({
        #'image_url': 'Scott',
        'name': title_text,
        'description': description,
        'type_excursion': type_excursion,
        'datetime': time,
        'payment': payment,
        'quantity': quantity
    })
    print(title_text, description, type_excursion, time, payment, quantity)


# with open('data.json', 'w', encoding='utf8') as outfile:
#     json.dump(excursions, outfile, ensure_ascii=False,)