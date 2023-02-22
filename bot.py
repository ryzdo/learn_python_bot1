import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from environs import Env
from random import randint, choice
from datetime import datetime

import ephem
from emoji import emojize


logging.basicConfig(filename="bot.log", level=logging.INFO)

USER_EMOJI = [':smiley_cat:', ':smiling_imp:', ':panda_face:', ':dog:']

# PROXY = {'proxy_url': settings.PROXY_URL,
#          'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME,
#                                   'password': settings.PROXY_PASSWORD}}


def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(USER_EMOJI)
        return emojize(smile, language='alias')
    return user_data['emoji']


async def greet_user(update, context):
    logging.info("Вызван /start")
    context.user_data['emoji'] = get_smile(context.user_data)
    await update.message.reply_text(f"Здравствуй, пользователь {context.user_data['emoji']}!")


async def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    username = update.effective_user.first_name
    text = update.message.text
    logging.info(text)
    await update.message.reply_text(f"Здравствуй, {username} {context.user_data['emoji']}! Ты написал: {text}")


async def where_is_the_planet(update, context):
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
    words = context.args
    count_words = len(words)
    message = f'{count_words} слова' if count_words else 'Введите фразу после /wordcount'
    await update.message.reply_text(message)


def play_random_numbers(user_number):
    bot_number = randint(user_number-10, user_number+10)
    if user_number > bot_number:
        message = f"Ты загадал {user_number}, я загадал {bot_number}, ты выиграл!"
    elif user_number == bot_number:
        message = f"Ты загадал {user_number}, я загадал {bot_number}, ничья!"
    else:
        message = f"Ты загадал {user_number}, я загадал {bot_number}, я выиграл!"
    return message


async def guess_number(update, context):
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = "Введите целое число"

    await update.message.reply_text(message)


async def next_fool_moon(update, context):
    try:
        date = datetime.strptime(context.args[0], '%Y-%m-%d')
    except (TypeError, ValueError, IndexError):
        date = update.message.date
    message = str(ephem.next_full_moon(date))
    await update.message.reply_text(f'Ближайшее полнолуние от {date.date()} будет {message}')


def main():

    env: Env = Env()
    env.read_env()

    mybot = Application.builder().token(env('TG_TOKEN')).build()

    mybot.add_handler(CommandHandler('start', greet_user))
    mybot.add_handler(CommandHandler('guess', guess_number))
    mybot.add_handler(CommandHandler('planet', where_is_the_planet))
    mybot.add_handler(CommandHandler('wordcount', count_words))
    mybot.add_handler(CommandHandler('next_full_moon', next_fool_moon))
    mybot.add_handler(MessageHandler(filters.Text('Когда ближайшее полнолуние?'), next_fool_moon))
    mybot.add_handler(MessageHandler(filters.TEXT, talk_to_me))

    logging.info("Бот стартовал")
    mybot.run_polling()


if __name__ == "__main__":
    main()
