from os.path import join
from os import getenv

import telebot
from more_itertools import chunked
from telebot.types import KeyboardButton
from telebot.types import ReplyKeyboardMarkup
from dotenv import load_dotenv

from weather import get_weather


load_dotenv()

bot = telebot.TeleBot('7301427607:AAH2VYUSuxDRwa6a2c9tn7IecwcKukeCKMk')
TOWNS = [
    'Архангельск',
    'Астрахань',
    'Владивосток',
    'Владимир',
    'Волгоград',
    'Воронеж',
    'Казань',
    'Калининград',
    'Москва',
    'Нижний Новгород',
    'Ростов',
    'Санкт-Петербург',
    'Сочи',
    'Тобольск'
    ]
TOWN_IMAGES_FOLDER = getenv('TOWNS_TG_IMAGES_FOLDER', default='assets/images/town_images/')
HOST_URL = getenv('HOST_URL', default='http://127.0.0.1:5500')


@bot.message_handler(commands=['start'])
def start_bot(message):
    markup = ReplyKeyboardMarkup(input_field_placeholder='Select town:')
    for towns in list(chunked(TOWNS, 2)):
        button_1 = KeyboardButton(towns[0])
        button_2 = KeyboardButton(towns[1])
        markup.row(button_1, button_2)
    bot.send_message(message.chat.id, 'Выберите город:', reply_markup=markup)


@bot.message_handler(commands=['help'])
def send_help_info(message):
    bot.send_message(
        message.chat.id,
        'Выберите из предложенных городов, нужный вам город'
                     )


def lowercase_list(data):
    data = map(lambda x: x.lower(), data)
    return (list(data))


def render_answer(weather, town):
    try:
        answer = f"""*{town}*
Температура🌡️ {weather['temp']}°, {weather['condition']}
Влажность💧{weather['humidity']}%
Скорость ветра💨 {weather['wind_speed']} км/ч, направление: {weather['wind_dir']}
[Узнайте подробнее про {town}.]({HOST_URL})
        """
    except Exception:
        return 'Непрвильно указан город'
    return answer


@bot.message_handler()
def reply(message):
    if message.text.lower() in lowercase_list(TOWNS):
        weather = get_weather(message.text)
        answer = render_answer(weather, message.text)
        filepath = join(TOWN_IMAGES_FOLDER, f'{message.text}.jpg')
        with open(filepath, 'rb') as photo:
            bot.send_photo(message.chat.id,
                           photo,
                           caption=answer,
                           parse_mode='Markdown'
                           )
    else:
        bot.send_message(message.chat.id, 'Неправильно указан город')


if __name__ == '__main__':
    bot.polling(none_stop=True)
