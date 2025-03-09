from hashlib import md5
from core import *

async def checkJoin(user, channels):
    ch = list()
    for channel in channels:
        if not (await bot.isJoin(channel, user)):
            ch.append(channel)
    return ch

@app.post('/')
async def Bot(key: str, update: dict = Body(...,embed=False)):
    if md5(key.encode()).hexdigest() != KEY:
        return
    user, text, chat_type, message_id, utype = getInformation(update)
    if not db[user]:
        db+[user, str()]
    channels = db['channels']

    if chat_type != 'private':
        return

    match utype:
        case 1:
            ch = await checkJoin(user, channels)
            if ch:
                await bot.SendMessage(user, getJoinText(ch), buttons['submit'], reply_message_id=message_id)
                return
            elif text == '/start':
                await bot.SendMessage(user, ' ✅عضویت شما تایید شد.\n👇🏼 از دکمه های زیر استفاده کن', buttons['menu'], reply_message_id=message_id)
            elif text.lower() in ('پنل', 'panel', '/panel') and user == ADMIN:
                await bot.SendMessage(user, '⚙️ از دکمه های زیر برای مدیریت ربات استفاده کن', buttons['panel'], reply_message_id=message_id)
        case 2:
            match text:
                case 'submit':
                    ch = await checkJoin(user, channels)
                    if ch:
                        await bot.sendRequest('answerCallbackQuery', {'callback_query_id': update['callback_query']['id'], 'text': '❌ هنوز جوین نشدی'})
                        return
                    else:
                        await bot.EditMessage(user, ' ✅عضویت شما تایید شد.\n👇🏼 از دکمه های زیر استفاده کن', message_id, buttons=buttons['menu'])
                
                case 'addchannel':
                    x = await bot.EditMessage(user, '♻️ یوزرنیم کانالی که میخوای اضافه کنی رو بفرست و منو توش ادمین کن', message_id, buttons['back'])
                    await bot.SendMessage(user, x)