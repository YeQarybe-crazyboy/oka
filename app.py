from hashlib import md5
from core import *

async def checkJoin(user):
    ch = list()
    for channel in db['channels']:
        if not (await bot.isJoin(channel, user)):
            ch.append(channel)
    return ch

@app.post('/')
async def Bot(key: str, update: dict = Body(...,embed=False)):
    if md5(key.encode()).hexdigest() != KEY:
        return
    user, text, chat_type, message_id, utype = getInformation(update)
    await bot.SendMessage(user, 'message_id '+str(message_id))

    if chat_type != 'private':
        return

    match utype:
        case 1:
            ch = await checkJoin(user)
            if ch:
                await bot.SendMessage(user, getJoinText(ch), buttons['submit'], reply_message_id=message_id)
                return
            elif text == '/start':
                await bot.SendMessage(user, ' ✅عضویت شما تایید شد.\n👇🏼 از دکمه های زیر استفاده کن', buttons['menu'], reply_message_id=message_id)
        case 2:
            if text == 'submit':
                ch = await checkJoin(user)
                if ch:
                    await bot.sendRequest('answerCallbackQuery', {'callback_query_id': update['callback_query']['id'], 'text': '❌ هنوز جوین نشدی'})
                    return
                else:
                    await bot.EditMessage(user, ' ✅عضویت شما تایید شد.\n👇🏼 از دکمه های زیر استفاده کن', buttons=buttons['menu'])