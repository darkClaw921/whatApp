from curses.ascii import isdigit
from chat import GPT
from helper import Message
from workBitrix import create_lead, find_lead
gpt=GPT()

promt = gpt.load_prompt('https://docs.google.com/document/d/17sjZBzz3GZnup1CrZPl5YuJjiughs7VcOCoT70jKupA/edit?usp=sharing')

USERS={}
async def check_message(Message):
    text=Message.message
    if text=='':
        return '0'
    # if text=='' and Message.photos is not None:
    #     print('создаем лид c фото')
    #     lead= await find_lead(f'{Message.userID}')
    #     if lead is None:
    #         await create_lead(Message, isNeedCreate=True)
    #     else:
    #         await create_lead(Message, lead=lead)
    #     return '0'
    
    historyList = [
        {'role': 'user', 'content': text},]
    print(f'{historyList=}')
    answerText=gpt.answer_yandex(promt, historyList, 0)[0]
    print(f'{answerText=}')
    
    answerText=answerText.lower() 
    if answerText=='1' or answerText.find('запрос клиента')!=-1:
        print('создаем лид из ответа')
        # lead= await find_lead(f'{Message.userID}')
        # print(f'aaaaaaaaaaaaaaaa')
        # print(f'{lead=}')
        # if lead is None:
        await create_lead(Message, isNeedCreate=True)
        # else:
        #     await create_lead(Message, lead=lead)
    
        return answerText
    return answerText
    # if answerText.find('ТВОЙ ОТВЕТ:') == -1:
    #     return '0'
    # else:
    #     return answerText

# text = """Ищем квартиру для съемок Промо с подобным интерьером или с возможностью задекорировать под референсы

# Дата: 16 марта

# В квартире должна быть: Стиральная машинка, посудомоечная машинка, диван"""
# mes=Message(text, 1, 'telegram', 1)
# a=check_message(mes)
# print(a)
