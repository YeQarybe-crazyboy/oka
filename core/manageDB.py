from requests import patch, get

class EdgeConfig:
    def __init__(self, id, address, token, bearer):
        self.ID = id
        self.ADDRESS = address+('/' if not address.endswith('/') else str())
        self.API = self.__geturl()+'v1/edge-config/'
        self.TOKEN = token
        self.BEARER = bearer
        self.URL = self.API+self.ID+'/'

    def __create_dict__(self, operation, key, value=None):
        return {'items': [{'operation': operation, 'key': key, 'value': value}]}

    def __geturl(self, api=True):
        return self.ADDRESS.format('api' if api else 'edge-config')

    def __auth__(self, auth_type=True):
        return {'Authorization': 'Bearer '+(self.BEARER if auth_type else self.TOKEN), 'Content-Type': 'application/json'}

    def addItem(self, key, value):
        key = str(key)
        operation = 'update' if self[key] else 'create'
        return patch(self.URL+'items', headers=self.__auth__(), json=self.__create_dict__(operation, key, value)).json()

    def getAll(self):
        return get(self.__geturl(False)+self.ID+'/items', headers=self.__auth__(False)).json()

    def deleteItem(self, key):
        operation = 'delete'
        return patch(self.URL+'items', headers=self.__auth__(), json=self.__create_dict__(operation, key)).json()

    def __add__(self, item):
        return self.addItem(item[0], item[1])

    def __sub__(self, key):
        return self.deleteItem(key)

    def __getitem__(self, item):
        return self.getAll().get(item)