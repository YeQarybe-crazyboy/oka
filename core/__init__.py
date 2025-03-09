from json import load
from os import getenv
from fastapi import FastAPI, Body
from .manageDB import EdgeConfig
from .functions import *

with open('keyboards.json') as i:
    buttons = load(i)

KEY = getenv('KEY')
ADMIN = getenv('ADMIN')
db = EdgeConfig(getenv('ID'), 'https://{}.vercel.com/', getenv('TOKEN'), getenv('BEARER'))
db+['posts', []]
db+['channels', ['@FuckingDaily']]
app = FastAPI()
bot = ManageBot(getenv('BOT'))