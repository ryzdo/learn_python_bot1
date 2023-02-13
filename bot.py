import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from environs import Env


logging.basicConfig(filename="bot.log", level=logging.INFO)

# PROXY = {'proxy_url': settings.PROXY_URL,
#          'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME,
#                                   'password': settings.PROXY_PASSWORD}}


async def greet_user(update, context):
    logging.info("Вызван /start")
    await update.message.reply_text("Здравствуй, пользователь!")


async def talk_to_me(update, context):
    text = update.message.text
    logging.info(text)
    await update.message.reply_text(text)


def main():

    env: Env = Env()
    env.read_env()
    mybot = Application.builder().token(env('TG_TOKEN')).build()

    mybot.add_handler(CommandHandler('start', greet_user))
    mybot.add_handler(MessageHandler(filters.TEXT, talk_to_me))

    logging.info("Бот стартовал")
    mybot.run_polling()


if __name__ == "__main__":
    main()
