import base64
class Message():

    def __init__(self, message:str, chenalTitle:int, messanger:str, userName:str,
                 userID:int, photos:None|str=None, messageURL:None|str=None,):
        self.message=message
        self.chenalTitle=chenalTitle
        self.messanger=messanger
        self.userName=userName
        self.photos=photos
        self.userID=userID
        self.messageURL=messageURL 



def read_file_as_base64(file_path):
    
    with open(file_path, 'rb') as file:
        file_data = file.read()
        if file_data:
            file_base64 = base64.b64encode(file_data).decode('utf-8')
            return file_base64
        else:
            print("Файл пуст.")
            return None