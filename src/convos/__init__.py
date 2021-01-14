from src.paths import SRC_DIR
import os, json
from importlib import import_module
# from src.convos.checkin
# from .checkin import CheckIn

CONVERSATIONS = []
# convo_dir = f'{SRC_DIR}/convos/'
convo_dir = '/home/jacob/PycharmProjects/MyBot/src/convos/'
for file_name in os.listdir(convo_dir):
    if '.json' in file_name:
        with open(f'{convo_dir}/{file_name}') as convo_file:
            CONVERSATIONS.append(json.load(convo_file))

from .checkin import CheckIn
from .morning_routine import MorningRoutine
from .todo import ToDo
from .evening_routine import EveningRoutine
bot_classes =[
    CheckIn, MorningRoutine,ToDo, EveningRoutine
]