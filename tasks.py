from emoji import emojize
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

task_list: list = [{'id': '1111', 'name': 'Утренняя зарядка', 'time': '06:00', 'done': True},
                   {'id': '1112', 'name': 'Уроки Python', 'done': False},
                   {'id': '1113', 'name': 'Уроки English', 'description': '15 мин занятия', 'done': False},
                   {'id': '1114', 'name': 'Слова English', 'description': 'Выучить 5 новых слов', 'done': True},
                   {'id': '1115', 'name': 'Лекарства', 'time': '12:15', 'done': False}
                   ]

emoji_todo = ':white_medium_square:'
emoji_done = ':white_check_mark:'


def get_tasks_list() -> str:
    text: str = 'Задачи на сегодня:\n\n'
    for index, task in enumerate(task_list, start=1):
        text += str(index)
        time = task.get('time', '')
        if task['done']:
            text += f' {emojize(emoji_done, language="alias")} ~{time} {task["name"]}~\n'
        else:
            text += f' {emojize(emoji_todo, language="alias")} {time} {task["name"]}\n'
    text += '\nВыберите номер задачи для просмотра'
    return text


async def show_tasks_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = get_tasks_list()
    if update.message:
        await update.message.reply_markdown_v2(text, reply_markup=task_list_inline_keyboard())


async def show_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.callback_query:
        await update.callback_query.answer()
        if update.callback_query.data:
            task_id: str = update.callback_query.data
        for task in task_list:
            if task['id'] == task_id:
                text: str = f"*{task['name']}*\n\n"
                if task['done']:
                    text += f' {emojize(emoji_done, language="alias")} Завершено\n'
                else:
                    text += f' {emojize(emoji_todo, language="alias")} Выполнить\n'
                text += f"Время \- {task.get('time', 'Не задано')}\n"
                text += f"_{task.get('description', ' ')}_"
        await update.callback_query.edit_message_text(text,
                                                      parse_mode=ParseMode.MARKDOWN_V2,
                                                      reply_markup=task_inline_keyboard())


async def mark_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.callback_query:
        await update.callback_query.edit_message_text('Отметить')


async def to_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.callback_query:
        text = get_tasks_list()
        await update.callback_query.edit_message_text(text,
                                                      parse_mode=ParseMode.MARKDOWN_V2,
                                                      reply_markup=task_list_inline_keyboard())


async def test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text1 = [i+1 for i in range(len(task_list))]
    if update.message:
        await update.message.reply_text(str(text1))


def task_list_inline_keyboard() -> InlineKeyboardMarkup:
    inlinekeyboard = [[InlineKeyboardButton(str(i), callback_data=task['id']) for i, task in enumerate(task_list, 1)]]
    return InlineKeyboardMarkup(inlinekeyboard)


def task_inline_keyboard() -> InlineKeyboardMarkup:
    inlinekeyboard = [[InlineKeyboardButton('Отметить', callback_data='mark'),
                       InlineKeyboardButton('К списку', callback_data='to_list')
                       ]]
    return InlineKeyboardMarkup(inlinekeyboard)
