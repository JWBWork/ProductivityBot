from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import AndTrigger, OrTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import atexit
from src.convos import CONVERSATIONS
from src.bot import my_bot

trigger_map = {
    'cron': CronTrigger,
    'interval': IntervalTrigger
}


def trigger_fact(schedule):
    trigs = []
    for t in schedule['triggers']:
        trig_init = trigger_map[t['trigger']]
        del t['trigger']
        trigs.append(trig_init(**t))
    trigger_type = schedule.get('type', 'and')
    if trigger_type == 'and':
        return AndTrigger(trigs)
    elif trigger_type == "or":
        return OrTrigger(trigs)


class ScheduleBot:
    def __init__(self):
        self.scheduler = self._load_schedules()

    def reload_schedules(self):
        self.scheduler = self._load_schedules()

    def _load_schedules(self):
        # TODO: update schedules ?
        scheduler = BackgroundScheduler()
        for c in CONVERSATIONS:
            if c.get('schedule'):
                print(f"scheduling {c['name']}")
                scheduler.add_job(
                    func=getattr(my_bot, c['function']),
                    trigger=trigger_fact(c['schedule'])
                )
        atexit.register(lambda: scheduler.shutdown())
        scheduler.start()
        return scheduler
