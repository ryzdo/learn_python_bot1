import logging
from random import choice, randint

from emoji import emojize
from telegram import KeyboardButton, ReplyKeyboardMarkup
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc, resources_pb2, service_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2
from settings import CLARIFAI_API_KEY

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
        ['Когда ближайшее полнолуние?', KeyboardButton('Мои координаты', request_location=True)],
        ['/task', '/test']
    ])


def has_object_on_image(file_name, object_name):
    channel = ClarifaiChannel.get_grpc_channel()
    app = service_pb2_grpc.V2Stub(channel)
    metadata = (('authorization', f'Key {CLARIFAI_API_KEY}'),)

    with open(file_name, 'rb') as f:
        file_data = f.read()
        image = resources_pb2.Image(base64=file_data)

    request = service_pb2.PostModelOutputsRequest(
        model_id='aaa03c23b3724a16a56b629203edc62c',
        inputs=[
            resources_pb2.Input(data=resources_pb2.Data(image=image))
        ])

    response = app.PostModelOutputs(request, metadata=metadata)
    return check_responce_for_object(response, object_name=object_name)


def check_responce_for_cat(response):
    if response.status.code == status_code_pb2.SUCCESS:
        for concept in response.outputs[0].data.concepts:
            if concept.name == 'cat' and concept.value >= 0.85:
                return True
    else:
        print(f"Ошибка распознавания: {response.outputs[0].status.details}")

    return False


def check_responce_for_object(response, object_name):
    if response.status.code == status_code_pb2.SUCCESS:
        for concept in response.outputs[0].data.concepts:
            if concept.name == object_name and concept.value >= 0.85:
                return True
    else:
        print(f"Ошибка распознавания: {response.outputs[0].status.details}")

    return False


if __name__ == "__main__":
    print(has_object_on_image('images/cat1.jpg', 'cat'))
