from src.paths import TMP_DIR
from src.merge import merge
import os
import json
from datetime import datetime
import pickle

bot_pickle_path = f'{TMP_DIR}/Notes.pk'
if os.path.isfile(bot_pickle_path):
    with open(bot_pickle_path, 'rb') as pickle_file:
        bot_pickle = pickle.load(pickle_file)
else:
    bot_pickle = {
        'Notes': [],
    }


def write_note(user_input, type=None):
    # json_path = f'{NOTES_DIR}/Note.json'
    date = datetime.today().strftime('%D')
    time = datetime.now().strftime('%H:%M')
    note_dict = {
        'type': type,
        'Date': date,
        'Time': time,
        'Body': user_input,
    }
    bot_pickle['Notes'].append(note_dict)
    with open(f'{TMP_DIR}/Notes.pk', 'wb+') as notes_pkl:
        pickle.dump(bot_pickle, notes_pkl)
