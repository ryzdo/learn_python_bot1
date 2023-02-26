import logging
from random import choice, randint

from emoji import emojize
from telegram import KeyboardButton, ReplyKeyboardMarkup

USER_EMOJI = [':smiley_cat:', ':smiling_imp:', ':panda_face:', ':dog:']


def get_smile(user_data):
    logging.info("Get smile")
    if 'emoji' not in user_data:
        smile = choice(USER_EMOJI)
        return emojize(smile, language='alias')
    return user_data['emoji']


def read_cities() -> list:
    logging.info("Read cities from goroda.txt")
    cities: list = []
    with open('goroda.txt', 'r', encoding='cp1251') as f:
        for line in f:
            city = line.strip()
            if city:
                if 'txt' in city:
                    continue
                elif 'Оспаривается' in city:
                    city = city[:-12]
                cities.append(city)
    return cities


def get_cities(user_data):
    logging.info("Get cities")
    if 'cities' not in user_data:
        cities = read_cities()
        return cities
    return user_data['cities']


def play_random_numbers(user_number: int) -> str:
    bot_number = randint(user_number-10, user_number+10)
    if user_number > bot_number:
        message = f"Ты загадал {user_number}, я загадал {bot_number}, ты выиграл!"
    elif user_number == bot_number:
        message = f"Ты загадал {user_number}, я загадал {bot_number}, ничья!"
    else:
        message = f"Ты загадал {user_number}, я загадал {bot_number}, я выиграл!"
    return message


def find_city(cities: list[str], letter: str) -> str:
    cities_start_letter: list[str] = []
    for city in cities:
        if city.startswith(letter.upper()):
            cities_start_letter.append(city)
    return choice(cities_start_letter)


def main_keyboard():
    return ReplyKeyboardMarkup([
        ['Когда ближайшее полнолуние?', KeyboardButton('Мои координаты', request_location=True)]
    ])
