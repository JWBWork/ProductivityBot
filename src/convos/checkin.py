import random
from src.texting import send_message
from src.scripts import load_line
from src.notes import write_note


class CheckIn:
    def begin_check_in(self):
        print('begining check in')
        send_message(load_line("checkin"))
        self.force_state = 'check in/check in response'

    def record_check_in(self, user_input):
        # send_message(f"your user_input: {user_input}")
        input_split = user_input.split(' ')
        input_split.insert(random.randint(0, len(input_split)), '...')
        input_split.insert(random.randint(0, len(input_split)), '...')
        msg = f"Okay cool!, I'll take a note\n{' '.join(input_split)}"
        write_note(user_input, type='checkin')
        send_message(msg)
