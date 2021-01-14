import os
from src import *
from src.bot import test_bot

if __name__ == '__main__':
    init_scheduler()
    app.run(debug=False)
    # test_bot()
