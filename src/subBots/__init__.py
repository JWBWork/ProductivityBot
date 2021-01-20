import os, json


# from src.convos.checkin
# from .checkin import CheckIn


def load_convos():
    convos = []
    convo_dir = '/home/jacob/PycharmProjects/MyBot/src/convos/'
    for file_name in os.listdir(convo_dir):
        if '.json' in file_name:
            with open(f'{convo_dir}/{file_name}') as convo_file:
                convos.append(json.load(convo_file))
    return convos


CONVERSATIONS = load_convos()

from src.subBots.checkin import CheckIn
from src.subBots.morning_routine import MorningRoutine
from src.subBots.todo import ToDo
from src.subBots.evening_routine import EveningRoutine
from .schedule import ScheduleBot
bot_classes = [
    CheckIn, MorningRoutine, ToDo, EveningRoutine
]
