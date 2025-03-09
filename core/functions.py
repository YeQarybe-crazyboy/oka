from requests import get
from json import dumps

class ManageBot:
    def __init__(self, token):
        self.__TOKEN = token

    async def sendRequest(self, METHOD, PARAMS=dict()):
        return get('https://api.telegram.org/bot{}/{}'.format(self.__TOKEN, METHOD), params=PARAMS).json()

    async def SendMessage(self, chat_id, text, buttons=None, parse_mode=None, reply_message_id=None):
        return await self.sendRequest('sendmessage', {'chat_id': chat_id, 'text': str(text), 'reply_markup': dumps(buttons) if buttons else None, 'parse_mode': parse_mode, 'reply_to_message_id': reply_message_id})

    async def EditMessage(self, chat_id, text, message_id, buttons=None, parse_mode=None):
        return await self.sendRequest('sendmessage', {'message_id': message_id, 'chat_id': chat_id, 'text': text, 'reply_markup': dumps(buttons) if buttons else None, 'parse_mode': parse_mode})

    async def isJoin(self, channel, user):
        res = await self.sendRequest('getChatMember', {'chat_id': channel, 'user_id': user})
        if res['ok']:
            return res['result']['status'] != 'left'

def getInformation(u):
    if 'message' in u:
        m = u['message']
        return (m['from']['id'], m['text'], m['chat']['type'], m['message_id'], 1)
    elif 'callback_query' in u:
        m = u['callback_query']
        # return (m['from']['id'], m['data'], m['message']['chat']['type'], m['message']['message_id'], 2)
        return (m['from']['id'], m['data'], m['message']['chat']['type'], 'del', 2)

def getJoinText(channels):
    text = "❗️ لطفا اول توی کانال {} جوین شو :\n{}"
    ch = '\n'.join(channels)
    if len(channels) == 1:
        return text.format('های ما', ch)
    return text.format('ما', ch)
