from emoji import emojize
task_list: list = [{'name': 'Утренняя зарядка', 'time': '06:00', 'done': True},
                   {'name': 'Уроки Python', 'done': False},
                   {'name': 'Уроки English', 'done': False},
                   {'name': 'Слова English', 'done': True},
                   {'name': 'Лекарства', 'time': '12:15', 'done': False}
                   ]

emoji_todo = ':white_medium_square:'
emoji_done = ':white_check_mark:'


async def show_tasks_list(update, context):
    text: str = 'Задачи на сегодня:\n\n'
    for index, task in enumerate(task_list, start=1):
        text += str(index)
        time = task.get('time', '')
        if task['done']:
            text += f' {emojize(emoji_done, language="alias")} ~{time} {task["name"]}~\n'
        else:
            text += f' {emojize(emoji_todo, language="alias")} {time} {task["name"]}\n'
    text += '\nВыберите номер задачи для просмотра'
    await update.message.reply_markdown_v2(text)


async def test(update, context):
    text1 = '~text1~'
    text2 = '--(text2)--'
    await update.message.reply_markdown_v2(text1, text2)
