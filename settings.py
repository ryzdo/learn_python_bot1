from environs import Env

env: Env = Env()
env.read_env()

TG_TOKEN = env('TG_TOKEN')
CLARIFAI_API_KEY = env('CLARIFAI_API_KEY')
