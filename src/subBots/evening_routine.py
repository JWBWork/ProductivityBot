import pickle
import os
from src.paths import TMP_DIR
from src.texting import send_message
from datetime import datetime
from src.notes import write_note
import calendar
from src.goals import goals, save_goals
from collections import defaultdict

# goals_path = os.path.join(TMP_DIR, 'goals.pk')
# print(f"GOALS PATH: {goals_path}")

# if os.path.isfile(goals_path):
#     with open(goals_path, 'rb') as goals_file:
#         goals = pickle.load(goals_file)
# else:
#     goals = {
#         'Day': [],
#         'Week': [],
#         'Month': [],
#         'Hist': {
#             'Day': None,
#             'Week': None,
#             'Month': None
#         }
#     }


class EveningRoutine:
    # time: 9pm daily mon-fri,sun
    #
    # list/update goals
    #   every evening ask if daily goals met
    #
    #   every sunday evening ask if weekly goals met
    #       diff response to yes/no/some/all/none
    #       ask for note + set new goals
    #
    #   end of month ask if monthly goals met
    #       diff response to yes/no/some/all/none
    #       ask for note + set new goals
    #
    # review provided todos
    #   Not sure how to handle this, might just show list
    #
    # set tomorrows goals
    #   ux here tricky - think it'll be hardcoded for separation by line break
    #
    def __init__(self):
        # overwritten by bot class to defaultdict
        self.temp = None

    def _set_history(self, timeframe, date):
        goals['Hist'][timeframe] = date

    def _needs_review(self, timeframe=None, date=None):
        timeframe = timeframe or "Day"
        date = date or datetime.now().strftime('%D')
        now = datetime.now()
        if timeframe == "Day":
            return goals['Hist']['Day'] != date
        elif timeframe == "Week":
            return now.day == calendar.monthrange(
                now.year, now.month
            ) and goals['Hist']['Month'] != date
        elif timeframe == "Month":
            return now.day == calendar.monthrange(
                now.year, now.month
            ) and goals['Hist']['Month'] != date

    def evening_routine(self, **kwargs):
        date = datetime.now().strftime('%D')
        if self._needs_review('Day', date):
            self._daily_goals_check()
            self._set_history('Day', date)
            self.temp['timeframe'] = 'Day'
        elif self._needs_review('Week', date):
            self._weekly_goals_check()
            self._set_history('Week', date)
            self.temp['timeframe'] = 'Week'
        elif self._needs_review('Month', date):
            self._monthly_goals_check()
            self._set_history('Month', date)
            self.temp['timeframe'] = 'Month'

    def _daily_goals_check(self):
        msg = ["Hey! do you have time to review?\n",
               "Did we meet our goals today?\n\n"]
        if goals['Day']:
            msg += [f"{i}. {goal}\n"
                    for i, goal in enumerate(goals['Day'])]
        send_message(msg)
        self.expected_state = [
            'evening_routine/goals_all',
            'evening_routine/goals_none',
            'evening_routine/goals_some',
        ]

    def _weekly_goals_check(self):
        send_message("TODO: weekly review 😬")

    def _monthly_goals_check(self):
        send_message("TODO: Monthly review 😬")

    def meet_goals(self, **kwargs):
        success = kwargs['success']
        if success == "all":
            send_message("ayyyyyy nice boi 😁, tell me about it")
            pass
        elif success == "some":
            send_message("ok cool! what went right and wrong?")
            pass
        elif success == "none":
            send_message("Oh no! 😥 What went wrong?")
            pass
        self.force_state = "evening_routine/get_review_notes"

    def save_review_note(self, user_note):
        write_note(user_note, type="EveningReview")
        self.request_goals()

    def request_goals(self):
        for timeframe in ['Day', 'Week', 'Month']:
            if self.temp['timeframe'] == timeframe:
                send_message(
                    f"noted 📋 - what are your goals for the {timeframe}?"
                )
                self.force_state = "evening_routine/receive_goals"

    def save_goals(self, user_goals):
        timeframe = self.temp.get('timeframe')
        user_goals = user_goals.split("\n\n")
        save_goals(user_goals)
        send_message(f"great! I've update your goals for {timeframe}!")
        self.temp['timeframe'] = None
        self.evening_routine()


