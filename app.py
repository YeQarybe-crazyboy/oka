from hashlib import md5
from os import getenv
from core import *

@app.post('/')
async def Bot(key: str, update: dict = Body(...,embed=False)):
    if md5(key.encode()).hexdigest() != getenv('KEY'):
        return
    user, text, chat_type, message_id, utype = getInformation(update)
    await bot.SendMessage(user, 'okaaaaaa')
    if chat_type != 'private':
        return
    ch = list()
    for channel in db['channels']:
        await bot.SendMessage(user, (await bot.isJoin(channel, user)))
        if not (await bot.isJoin(channel, user)):
            ch.append(channel)
    if ch:
        await bot.SendMessage(user, getJoinText(ch), buttons['submit'], reply_message_id=message_id)
        return
    else:
        await bot.SendMessage(user, 'ok')