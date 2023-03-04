from emoji import emojize
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


task_list: list = [{'name': 'Утренняя зарядка', 'time': '06:00', 'done': True},
                   {'name': 'Уроки Python', 'done': False},
                   {'name': 'Уроки English', 'done': False},
                   {'name': 'Слова English', 'done': True},
                   {'name': 'Лекарства', 'time': '12:15', 'done': False}
                   ]

emoji_todo = ':white_medium_square:'
emoji_done = ':white_check_mark:'


async def show_tasks_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text: str = 'Задачи на сегодня:\n\n'
    for index, task in enumerate(task_list, start=1):
        text += str(index)
        time = task.get('time', '')
        if task['done']:
            text += f' {emojize(emoji_done, language="alias")} ~{time} {task["name"]}~\n'
        else:
            text += f' {emojize(emoji_todo, language="alias")} {time} {task["name"]}\n'
    text += '\nВыберите номер задачи для просмотра'
    if update.message:
        await update.message.reply_markdown_v2(text, reply_markup=task_list_inline_keyboard())


async def show_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.callback_query:
        await update.callback_query.answer()
        text: str = f"Выбран вариант: {update.callback_query.data}"
        await update.callback_query.edit_message_text(text)


async def test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text1 = [i+1 for i in range(len(task_list))]
    if update.message:
        await update.message.reply_text(str(text1))


def task_list_inline_keyboard() -> InlineKeyboardMarkup:
    inlinekeyboard = [[InlineKeyboardButton(str(i+1), callback_data=str(i)) for i in range(len(task_list))]]
    return InlineKeyboardMarkup(inlinekeyboard)
