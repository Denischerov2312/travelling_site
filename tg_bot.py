import telebot
from more_itertools import chunked
from telebot.types import KeyboardButton
from telebot.types import ReplyKeyboardMarkup


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


@bot.message_handler(commands=['help'])
def send_help_info(message):
    bot.send_message(message.chat.id, 'Выберите из предложенных городов, нужный вам город')


@bot.message_handler(commands=['start'])
def start_bot(message):
    markup = ReplyKeyboardMarkup(
        one_time_keyboard=True,
        input_field_placeholder='Select town:')
    for towns in list(chunked(TOWNS, 2)):
        button_1 = KeyboardButton(towns[0])
        button_2 = KeyboardButton(towns[1])
        markup.row(button_1, button_2)
    bot.send_message(message.chat.id, 'Выберите город:', reply_markup=markup)


@bot.message_handler()
def reply(message):
    bot.send_message(message.chat.id, 'Вы выбрали ', message.text)


if __name__ == '__main__':
    bot.polling(none_stop=True)
