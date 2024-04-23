import json

class NotificationEvent:
    id: str
    status: str
    
    def __init__(self, id: str, status:str,):
        self.id = id 
        self.status = status
    
    def to_byte(self):
        return json.dumps(self.__dict__).encode('utf-8')