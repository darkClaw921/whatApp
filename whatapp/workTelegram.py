from telethon import TelegramClient, events
from chat import GPT
from pprint import pprint
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
import os
from helper import Message
from handlersMessage import check_message

# Вставьте ваши данные для подключения к Telegram API
# api_id = 'YOUR_API_ID'
# api_hash = 'YOUR_API_HASH'
api_id =os.getenv('API_ID') 
api_hash = os.getenv('API_HASH')
# phone_number = 'YOUR_PHONE_NUMBER'
gpt=GPT()
# Создайте экземпляр клиента Telegram
client = TelegramClient('session_name', api_id, api_hash, system_version="4.16.30-vxCUSTOM", device_model='Samsung Galaxy S24 Ultra, running Android 14')

# Авторизуйтесь в клиенте

client.start()

# Определите список идентификаторов каналов, из которых вы хотите получать сообщения
# channel_ids = [-1001281274611, -1001747110091,-1001117865178,'SwiftBook','Герасимова и Игорь Новый','-1002010911633',-1002010911633]  # Замените на реальные идентификаторы каналов
# channel_ids = ['SwiftBook','Герасимова и Игорь Новый','-1002010911633',]  # Замените на реальные идентификаторы каналов
#см Разработка бота Афиша/ tg источники
chenalName = [-1001391677315 ,#https://web.telegram.org/a/#-1001391677315
            -1001138391813,# https://web.telegram.org/a/#-1001138391813
            -1001794344203,# https://web.telegram.org/a/#-1001794344203
            -1002136713030,#https://web.telegram.org/a/#-1002136713030
            -1001558069317,#   https://web.telegram.org/a/#-1001558069317
            -1001279459673,#://web.telegram.org/a/#-1001279459673
              ]

chenalNamePrepared=[
   1391677315,
    1138391813,
    1794344203,
    2136713030,
    1558069317,
    1279459673, 
]
 
USERS={}
# @client.on(events.NewMessage())
# @client.on(events.NewMessage(chats=lambda x: x in chenalName))
def check_nickname_for_message(text:str):
    if text is None:
        return None
    if text.find('@')==-1:
        return None
    return text[text.find('@')+1:]

@client.on(events.NewMessage(chats=chenalName))
async def new_message_listener(event:events.newmessage.NewMessage.Event):
    # Обработка новых сообщений
    messageID=event.message.id
    chenalID=event.message.chat.id

    print(f'{chenalID=}') 
    # pprint
    # try:
    # pprint(event.message.chat.__dict__)
    # pprint(event.message.__dict__['_sender'].__dict__)
    print(type(event))
    chenalID=event.message.chat.id

    chenalTitle=event.message.chat.username
    print(f'{chenalTitle=}')
    # chenalID=event.message.chat.
    text=event.message.text
    print(f'1{text=}')
    # pprint(event.message.__dict__)
    photos=[]
    if event.message.media:
        directory = 'downloadsProject/'
        os.makedirs(directory, exist_ok=True) 

        # client.download_media(event.message)
        filePath = await event.message.download_media('downloadsProject/')
        
        print(f'{filePath=}')
        photos.append(filePath)

    userSendID=event.message.from_id.user_id
    
    try:
        userSendNickname=event.message.__dict__['_sender'].__dict__['username']
        # userSendNickname=event.message.sender.username

    except:
        userSendNickname=None
    if userSendNickname is None:
        # pprint(event.message.__dict__)
        userSendNickname=str(userSendID)

    print(f'{userSendID=}')
    print(f'{userSendNickname=}')
    # if len(text) <= 100: return 0
    #Проверяет меняется ли текст мероприятием
    # 1/0
    chenalID=event.message.chat.id
    print(f'{chenalID=}')
    if chenalID in chenalNamePrepared:
        msg=Message(message=text, 
                    chenalTitle=chenalTitle,
                    messageURL=f'https://t.me/{chenalTitle}/{messageID}', 
                    messanger='telegram', 
                    userID=userSendID,
                    userName=userSendNickname,
                    photos=photos if photos!=[] else None,)
        
        answer=await check_message(msg)
        print(f'{answer=}')
        # await client.send_message(-1001957850642, message=f'ответ yandex: {answer}',reply_to=event.message)

        for filePath in photos:
            os.remove(filePath)
        if answer=='0':
            return 0
        promt="""Я отправляю тебе объявление клиента. Он ищет локацию для съемки. Мне надо понять, заполнены ли в нем следующие реквизиты:
- даты съёмки 
- количество смен
- что снимается
- количество людей
- бюджет

Мне нужен ТОЛЬКО список того, что не заполнено.
НЕ ПИШИ что это список. Отправь ТОЛЬКО список того, что надо заполнить"""

        promt = gpt.load_prompt('https://docs.google.com/document/d/1KCl8vHujZIiMX87M3g0ZhcbsYHBukvjQNWYH8DsQaoU/edit?usp=sharing')
        historyList = [
            {'role': 'user', 'content': text},]
        # print(f'{historyList=}')
        
        

        answerText=gpt.answer_yandex(promt, historyList, 0)[0]
        
        
        if check_nickname_for_message(text) is not None:
            userSendID=check_nickname_for_message(text)

        pprint(USERS)    
        if userSendID in USERS and (datetime.now()-USERS[userSendID]).seconds<=86400:
            return 0
        else:
            if len(USERS)>20:
                USERS.remove(0)
            
            USERS[userSendID]=datetime.now()
        # await client.send_message(400923372, message=answerText+'\n\nВаше сообщение в чате: \n'+text)
            print(f'отправляем:{userSendID} => {answerText=}')
            await client.send_message(userSendID, message=answerText+'\n\nВаше сообщение в чате: \n'+text)
    # if chenalID == 2010911633:
        # await client.send_message(-1002010911633, message=answer,reply_to=event.message)

    # messageID=event.message.id
    # chenalID=event.message.chat.id
   

    
    #chenalID записывается без -100 в начале -1002010911633

# Запустите прослушивание новых сообщений
print('[OK]')
while True:
    # try:
    client.run_until_disconnected()
    
    # except:
        # print('Повоторный запуск')