from datetime import datetime
from src.texting import send_message
from src.scripts import load_line
from src.goals import save_goals


class MorningRoutine:
    def morning_routine(self):
        print('starting morning routine')
        now = datetime.now()

        # constructing morning routine list
        morn_routine = [
            'Take welbutrin 💊',
            'Feed Gem 😻',
            'Coffee ☕',
            'Make bed 🛏',
        ]
        if now.weekday() != 6:
            morn_routine.append('Workout 💪')
        morn_routine += [
            'Shower 🚿',
            'brush teeth! 😁✨',
            'Get dressed 👖',
        ]
        morning_routine_str = '\n-' + f'\n-'.join(morn_routine)

        week_day_str = "It's a weekday! Let's try to get some" \
                       " shit done today 😤" if now.weekday() in \
                                                range(0, 6) else ""

        msg = f"""
{load_line('morning_greeting')}

It's {now.strftime("%H:%M, %A %B %d")}

Here's your morning routine for {now.strftime('%A')}
{morning_routine_str}
{week_day_str}

Remember you're fasting until 12! no calories until then!

Let me know whn you've finished your routine ❤
"""
        send_message(msg)
        self.expected_state = "morning routine/finished routine tasks"

    def finish_routine(self):
        send_message('NICE! good work ❤\n'
                     'What are your goals for today?')

    # def set_morning_goals(self, user_input):
    #     goals = user_input.split('\n\n')
    #     save_goals(goals)
    #     send_message('Cool!')
