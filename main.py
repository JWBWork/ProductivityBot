import os
from src import *
from src.bot import test_bot
from src.config import config

if __name__ == '__main__':
    init_scheduler()
    if not config['testing']:
        app.run(debug=False)
    else:
        test_bot()
