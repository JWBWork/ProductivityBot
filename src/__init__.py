from flask import Flask

app = Flask(__name__)

from .api import *
from .schedule import *
