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
client = TelegramClient('session_name', api_id, api_hash)

# Авторизуйтесь в клиенте

client.start()

# Определите список идентификаторов каналов, из которых вы хотите получать сообщения
# channel_ids = [-1001281274611, -1001747110091,-1001117865178,'SwiftBook','Герасимова и Игорь Новый','-1002010911633',-1002010911633]  # Замените на реальные идентификаторы каналов
# channel_ids = ['SwiftBook','Герасимова и Игорь Новый','-1002010911633',]  # Замените на реальные идентификаторы каналов
#см Разработка бота Афиша/ tg источники
chenalName = [ -1001957850642,
              -1001279459673] 
# @client.on(events.NewMessage())
# @client.on(events.NewMessage(chats=lambda x: x in chenalName))
@client.on(events.NewMessage(chats=chenalName))
async def new_message_listener(event:events.newmessage.NewMessage.Event):
    # Обработка новых сообщений
    messageID=event.message.id
    # try:
    pprint(event.message.chat.__dict__)
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
        userSendNickname=event.message.sender.username
    except:
        userSendNickname=None
    if userSendNickname is None:
        pprint(event.message.__dict__)
        userSendNickname=str(userSendID)

    print(f'{userSendID=}')
    print(f'{userSendNickname=}')
    # if len(text) <= 100: return 0
    #Проверяет меняется ли текст мероприятием
    # 1/0
    chenalID=event.message.chat.id
    print(f'{chenalID=}')
    if chenalID == 1957850642 or chenalID == 1279459673:
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

    # if chenalID == 2010911633:
        # await client.send_message(-1002010911633, message=answer,reply_to=event.message)

    # messageID=event.message.id
    # chenalID=event.message.chat.id
   

    
    #chenalID записывается без -100 в начале -1002010911633

# Запустите прослушивание новых сообщений
print('[OK]')
while True:
    try:
        client.run_until_disconnected()
    except:
        print('Повоторный запуск')