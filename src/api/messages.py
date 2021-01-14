from flask import request
from flask_restful import Resource, Api
from src.api import flask_api
from src.texting import send_message
from src.bot import Bot
from pprint import pprint
from src.bot import Bot
# bot = Bot()


class Messages(Resource):
    def __init__(self):
        self.bot = Bot()

    def post(self):
        # pprint(request.values)
        self.bot.parse(request.values["Body"])
        # send_message("default response")


flask_api.add_resource(Messages, '/Messages')
