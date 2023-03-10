import logging

from settings import TG_TOKEN
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler

from handlers import (count_words, game_city, greet_user, guess_number,
                      next_full_moon, scalc, talk_to_me, user_coordinates,
                      where_is_the_planet, check_user_photo)
from tasks import show_tasks_list, show_task, mark_task, to_list, test

logging.basicConfig(filename="bot.log", level=logging.INFO,
                    format=u'%(lineno)d #%(levelname)-8s '
                    u'[%(asctime)s] - %(name)s - %(message)s')


# PROXY = {'proxy_url': settings.PROXY_URL,
#          'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME,
#                                   'password': settings.PROXY_PASSWORD}}


def main() -> None:

    mybot = Application.builder().token(TG_TOKEN).build()

    mybot.add_handler(CommandHandler('start', greet_user))
    mybot.add_handler(CommandHandler('guess', guess_number))
    mybot.add_handler(CommandHandler('planet', where_is_the_planet))
    mybot.add_handler(CommandHandler('wordcount', count_words))
    mybot.add_handler(CommandHandler('next_full_moon', next_full_moon))
    mybot.add_handler(CommandHandler('city', game_city))
    mybot.add_handler(CommandHandler('calc', scalc))

    mybot.add_handler(CommandHandler('task', show_tasks_list))
    mybot.add_handler(CommandHandler('test', test))
    mybot.add_handler(CallbackQueryHandler(mark_task, pattern='mark'))
    mybot.add_handler(CallbackQueryHandler(to_list, pattern='to_list'))
    mybot.add_handler(CallbackQueryHandler(show_task, pattern=r'^\d*$'))

    mybot.add_handler(MessageHandler(filters.PHOTO, check_user_photo))

    # mybot.add_handler(MessageHandler(filters.Text('Когда ближайшее полнолуние?'), next_full_moon))
    mybot.add_handler(MessageHandler(filters.Regex(r'^(Когда ближайшее полнолуние\?)$'), next_full_moon))
    mybot.add_handler(MessageHandler(filters.LOCATION, user_coordinates))
    mybot.add_handler(MessageHandler(filters.TEXT, talk_to_me))

    logging.info("Bot started")
    mybot.run_polling()


if __name__ == "__main__":
    main()
