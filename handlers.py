import logging
from datetime import datetime

import ephem

from simple_calc import calc
from utils import (find_city, get_cities, get_smile, main_keyboard, play_random_numbers)


async def greet_user(update, context):
    logging.info("Called /start")
    context.user_data['emoji'] = get_smile(context.user_data)
    my_keyboard = main_keyboard()
    await update.message.reply_text(f"Здравствуй, пользователь {context.user_data['emoji']}!", reply_markup=my_keyboard)


async def talk_to_me(update, context):
    logging.info("Called TEXT")
    context.user_data['emoji'] = get_smile(context.user_data)
    username = update.effective_user.first_name
    text = update.message.text
    logging.info(text)
    await update.message.reply_text(f"Здравствуй, {username} {context.user_data['emoji']}! Ты написал: {text}")


async def where_is_the_planet(update, context):
    logging.info("Called /planet")
    # planets = update.message.text.split()
    planets = context.args
    date = update.message.date
    for planet in planets:
        if hasattr(ephem, planet.capitalize()):
            pl = getattr(ephem, planet.capitalize())()
            pl.compute(date)
            const = ephem.constellation(pl)
            print(const)
            message = f'{planet} находиться в {const}'
        else:
            message = f'Нет планеты {planet}'
        await update.message.reply_text(message)


async def count_words(update, context):
    logging.info("Called /wordcount")
    words = context.args
    count_words = len(words)
    message = f'{count_words} слова' if count_words else 'Введите фразу после /wordcount'
    await update.message.reply_text(message)


async def guess_number(update, context):
    logging.info("Called /guess")
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = "Введите целое число"

    await update.message.reply_text(message)


async def next_full_moon(update, context):
    logging.info("Called /next_full_moon")
    try:
        date = datetime.strptime(context.args[0], '%Y-%m-%d')
    except (TypeError, ValueError, IndexError):
        date = update.message.date
    message = str(ephem.next_full_moon(date))
    await update.message.reply_text(f'Ближайшее полнолуние от {date.date()} будет {message}')


async def game_city(update, context):
    logging.info("Called /city")
    context.user_data['cities'] = get_cities(context.user_data)
    try:
        context.user_data['cities'].remove(context.args[0].capitalize())
        letter = context.args[0][-2] if context.args[0][-1] in 'ьъы' else context.args[0][-1]
        try:
            city = find_city(context.user_data['cities'], letter)
            context.user_data['cities'].remove(city)
            logging.info(f'Cities {context.args[0]} and {city} deleted')
            message = f'{city}, ваш ход'
        except (IndexError):
            logging.info(f'City {context.args[0]} deleted')
            message = f'Города на букву {letter.upper()} нет'
    except IndexError:
        message = 'Введите город после /city'
    except ValueError:
        message = 'Неверно указан город'
    await update.message.reply_text(message)


async def scalc(update, context):
    logging.info("Called /calc")
    await update.message.reply_text(calc(update.message.text[6:]))


async def user_coordinates(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    coords = update.message.location
    await update.message.reply_text(
        f'Ваши координаты {coords} {context.user_data["emoji"]}!',
        reply_markup=main_keyboard()
    )
