from fast_bitrix24 import Bitrix
import os
from dotenv import load_dotenv
from pprint import pprint
from dataclasses import dataclass
from datetime import datetime
# import urllib3
import urllib.request
import time
from helper import Message, read_file_as_base64
import asyncio
load_dotenv()
webhook = os.getenv('WEBHOOK')
bit = Bitrix(webhook)

@dataclass
class Lead:
    userName:str
    title:str='TITLE'
    userID:str='UF_CRM_1709220784686'
    photos:str='UF_CRM_1709223951925'
    urlUser:str='UF_CRM_1709224894080'
    messageURL:str='UF_CRM_1709293438392'

    # userID:str='UF_CRM_1709231051797'
    # photos:str='UF_CRM_1709231043105'
    # urlUser:str='UF_CRM_1709231060509'
    # messageURL:str='UF_CRM_1709235024346'
    description:str='COMMENTS'
# LEAD_T=False

def create_task():
    param = {'fields':{
        'TITLE':'',

    }}
    task = bit.call('tasks.task.add',params=param)
    return task


# async def te

async def find_lead(userID:str):
    lead = await bit.get_all(
        'crm.lead.list',
        params={
            'select': ['*', 'UF_*'],
            'filter': {Lead.userID: f'{userID}'}
    },)
    pprint(lead)
    if lead==[]:
        return None
    else:
        print('лид уже есть')
        # pprint(lead)
        lead=lead[-1]
        return lead

async def create_lead(Message:Message, isNeedCreate:bool=False,lead=None):
    # a=await find_lead('400923372')
    # print(a) 
    global LEAD_T
    userName = Message.userName
    chenallTitle = Message.chenalTitle
    
    files=Message.photos
    # leadID=None
    uploadFiles = []
    dateNow = datetime.now().strftime("%Y-%m-%d %H:%M")
    if files is not None:
        for fileName in files:
            file_path = f'{fileName}'
            file_base64 = read_file_as_base64(file_path)
            uploadFiles.append({'fileData':[fileName, file_base64]})

     #'UF_CRM_1690904694646': [{'fileData':["Задача_Запрос_в_СТП__Доступ_РДП.png", file_base64]}]
    if Message.message=='':
        description=' '
    else:
        description = f'{dateNow} -> {Message.message} - {Message.chenalTitle}\n'
    
    param = {'fields':{
        Lead.title: f'Заявка от {chenallTitle}, {Message.messanger}',
        Lead.userID: Message.userID,
        Lead.photos: uploadFiles if uploadFiles !=[] else None,
        Lead.description: description,
        # Lead.urlUser: f'https://t.me/{userName}', #TODO добавить ссылку на пользователя на уровень выше
        Lead.messageURL: Message.messageURL,
        
    }}
    # pprint(param)
    # pprint(uploadFiles)
    # lead = bit.call('crm.lead.add', param, raw=True)
    if isNeedCreate:
        lead = bit.call('crm.lead.add', param, raw=True)
        return 'ok'
    else:
        print('--------------------------')
        print('обновляем лид')
        update_lead(lead, uploadFiles, Message.message)
         
    # lead= await find_lead(f'{Message.userID}')
    # # print(f'{lead=}')
    # await asyncio.sleep(1)
    # if lead is None:
    # # if LEAD_T==False:
    #     print('создаем лид')
    #     # pass
    #     # lead = bit.call('crm.lead.add', param, raw=True)
    #     print('+++++++++++++++++++++++++')
        
    #     print(f'{lead=}')
    #     # LEAD_T=True
    # else:
    #     print('--------------------------')
    #     print('обновляем лид')
    #     update_lead(lead, uploadFiles, Message.message)
        
    # return lead['ID']

def update_lead(lead, photos:list[dict], descriptionNew:str):
   
    leadID = lead['ID']
    description = lead['COMMENTS']
    dateNow = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    photosLead=lead[Lead.photos]
    pprint(photosLead)
    photosLead=download_files_bitrix(photosLead)
    photos.extend(photosLead)

    if descriptionNew!='':
        description=f'{description} \n{dateNow} -> {descriptionNew}\n'
    param = {
        'ID': leadID,
        'fields':{
        Lead.photos: photos,
        Lead.description: description,
        #'': fields[''],
    }}
    
    lead = bit.call('crm.lead.update', param)
    return 'ok' 

def extract_filename_from_url(url):
    path = urllib.parse.urlparse(url).path
    return os.path.split(path)[-1]

def download_file(url):
    directory = 'downloadsProject/'
    os.makedirs(directory, exist_ok=True) # Создаем папку, если её не существует
    timeEpoch=int(time.time())
    filename = f'{timeEpoch}.jpg'  # Извлекаем имя файла из ссылки
    full_path = os.path.join(directory, filename)  # Формируем полный путь для сохранения файла
    urllib.request.urlretrieve(url, full_path)  # Скачиваем файл по ссылке и сохраняем его по указанному пути
    # res = urllib.request.urlretrieve(url, os.path.join(
        # directory, extract_filename_from_url(url)))
    # print(f'{res=}')
    return full_path

def download_files_bitrix(lst:list):
    files = []
    for l in lst:
        # https://b24-cii3on.bitrix24.ru/rest/1/cxt6r20imcu158yl/
        # filebit = download_file(f"https://ymb.bitrix24.ru{l['downloadUrl']}")
        filebit = download_file(f"https://b24-cii3on.bitrix24.ru{l['downloadUrl']}")

        file_base64 = read_file_as_base64(filebit)
        files.append({'fileData':[filebit, file_base64]})
    return files

def find_contact(phone:str):
    contact = bit.get_all(
    'crm.contact.list',
    params={
        'select': ['*', 'UF_*'],
        'filter': {'PHONE': phone}
    },)
    pprint(contact)
    if contact==[]:
        return None
    else:
        return contact[0]



def create_contact(fields):
    """Domofon
NoteAddress 
UrlFileAddress 
FullNameContact
Phone
    """
    params ={
        'fields':{
            'NAME':fields['FullNameContact'],
            'PHONE': [{'VALUE': fields['Phone'], 'VALUE_TYPE': 'WORK'}],
            'UF_CRM_1626798986': fields['Domofon'],
            'UF_CRM_1626799002': fields['NoteAddress'],
            'UF_CRM_1626799017': fields['UrlFileAddress'],
            'UF_CRM_1626799032': fields['FullNameContact'],
            'UF_CRM_1626799047': fields['Phone'],
        }
    }
    contactID = bit.call('crm.contact.add', params=params)
    return contactID

# a=find_lead(400923372)
# print(a)
# create_lead(Message('test', 1, 'telegram', 1,1))