import os, pickle
from src.paths import TMP_DIR

goals_path = os.path.join(TMP_DIR, 'goals.pk')

if os.path.isfile(goals_path):
    with open(goals_path, 'rb') as goals_file:
        goals = pickle.load(goals_file)
else:
    goals = {
        'Day': [],
        'Week': [],
        'Month': [],
        'Hist': {
            'Day': None,
            'Week': None,
            'Month': None
        }
    }


def save_goals(goal_list, timeframe=None):
    timeframe = timeframe or "Day"
    goals[timeframe] = goal_list
    with open(goals_path, 'wb+') as goals_file:
        pickle.dump(goals, goals_file)
    return goals
