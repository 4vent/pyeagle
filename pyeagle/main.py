import requests


class EagleAPI():
    def __init__(self) -> None:
        self.APPLICATION = _API_APPLICATION(self)
        self.FOLDER = _API_FOLDER(self)
        self.ITEM = _API_ITEM(self)
        self.LIBRARY = _API_LIBRARY(self)

    def get(self, _url: str, **query) -> dict:
        if not _url.startswith('https://'):
            _url = 'http://localhost:41595/api' + _url
        return requests.get(_url).json()
    

class _CHILD_API():
    def __init__(self, api: EagleAPI) -> None:
        self._api = api


class _API_APPLICATION(_CHILD_API):
    def info(self):
        return self._api.get('/application/info')


class _API_FOLDER(_CHILD_API):
    def create(self):
        return self._api.get('/folder/create')
        
    def rename(self):
        return self._api.get('/folder/rename')
        
    def update(self):
        return self._api.get('/folder/update')
        
    def list(self):
        return self._api.get('/folder/list')
        
    def listRecent(self):
        return self._api.get('/folder/listRecent')
        

class _API_ITEM(_CHILD_API):
    def addFromURL(self):
        return self._api.get('/item/addFromURL')

    def addFromURLs(self):
        return self._api.get('/item/addFromURLs')

    def addFromPath(self):
        return self._api.get('/item/addFromPath')

    def addFromPaths(self):
        return self._api.get('/item/addFromPaths')

    def addBookmark(self):
        return self._api.get('/item/addBookmark')

    def info(self):
        return self._api.get('/item/info')

    def thumbnail(self):
        return self._api.get('/item/thumbnail')

    def list(self):
        return self._api.get('/item/list')

    def moveToTrash(self):
        return self._api.get('/item/moveToTrash')

    def refreshPalette(self):
        return self._api.get('/item/refreshPalette')

    def refreshThumbnail(self):
        return self._api.get('/item/refreshThumbnail')

    def update(self):
        return self._api.get('/item/update')



class _API_LIBRARY(_CHILD_API):
    def info(self):
        return self._api.get('/library/info')
        
    def history(self):
        return self._api.get('/library/history')
        
    def switch(self):
        return self._api.get('/library/switch')
        
