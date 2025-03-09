from hashlib import md5
from core import *

@app.post('/')
async def Bot(key: str, update: dict = Body(...,embed=False)):
    if md5(key.encode()).hexdigest() != KEY:
        return
    user, text, chat_type, message_id, utype = getInformation(update)
    if not db[user]:
        db+[user, {'step': str(), 'm': int()}]

    userInfo = db[user]
    step = userInfo.get('step')
    m_id = userInfo.get('m')
    channels = db['channels']

    if chat_type != 'private':
        return

    match utype:
        case 1:
            if user == ADMIN:
                if step == 'addchannel':
                    channels.append(text)
                    db+['channels', channels]
                    await bot.deleteMessage(user, message_id)
                    await bot.EditMessage(user, f'✅ کانال {text} با موفقیت اضافه شد\nاز دکمه های زیر استفاده کن :', message_id, buttons['panel'])
                    await updateStep(user, str(), 0)

            else:
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
                    await updateStep(user, text, x['result']['message_id'])