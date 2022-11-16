import json
from typing import Literal

import requests

from . import types


class EagleAPI():
    def __init__(self, url='http://localhost:41595') -> None:
        self.eagle_host = url
        self.APPLICATION = _API_APPLICATION(self)
        self.FOLDER = _API_FOLDER(self)
        self.ITEM = _API_ITEM(self)
        self.LIBRARY = _API_LIBRARY(self)

    def get(self, _url: str, **query) -> dict:
        if not _url.startswith('https://'):
            _url = self.eagle_host + '/api' + _url
        return requests.get(_url, params=query).json()

    def post(self, _url: str, **query) -> dict:
        if not _url.startswith('https://'):
            _url = self.eagle_host + '/api' + _url
        return requests.post(_url, data=json.dumps(query, cls=types.EagleJSONEncoder)).json()
    

class _CHILD_API():
    def __init__(self, api: EagleAPI) -> None:
        self._api = api


class _API_APPLICATION(_CHILD_API):
    def info(self):
        res = self._api.get('/application/info')
        return (types._ApplicationInfo(**res['data'])
                if res['status'] == 'success' else res)


class _API_FOLDER(_CHILD_API):
    def create(self, folderName: str, parent: str | None = None):
        res = self._api.post('/folder/create', folderName=folderName, parent=parent)
        return (types._NewFolder(**res['data'])
                if res['status'] == 'success' else res)
        
    def rename(self, folderId: str, newName: str):
        res = self._api.post('/folder/rename', folderId=folderId, newName=newName)
        return (types._Folder(**res['data'])
                if res['status'] == 'success' else res)
        
    def update(self, folderId: str, newName: str | None = None,
               newDescription: str | None = None,
               newColor: types.COLOR | None = None):
        res = self._api.post('/folder/update', folderId=folderId, newName=newName,
                             newDescription=newDescription, newColor=newColor)
        return (types._Folder(**res['data'])
                if res['status'] == 'success' else res)
        
    def listRecent(self) -> list[types._Folder] | dict:
        res = self._api.get('/folder/listRecent')
        return (types.maplist(res['data'], types._Folder)
                if res['status'] == 'success' else res)
        
    def list(self) -> list[types._Folder] | dict:
        res = self._api.get('/folder/list')
        return (types.maplist(res['data'], types._Folder)
                if res['status'] == 'success' else res)
        

class _API_ITEM(_CHILD_API):
    def addFromURL(self, url: str, name: str, *, website: str | None = None,
                   tags: list[str] | None = None, annotation: str | None = None,
                   modificationTime: int | None = None,
                   folderId: str | None = None, headers: dict = {}):
        res = self._api.post('/item/addFromURL', url=url, name=name,
                             website=website, tags=tags, annotation=annotation,
                             modificationTime=modificationTime,
                             folderId=folderId, headers=headers)
        return res

    def addFromURLs(self, items: list[types.OnlineItem], folderId: str | None = None):
        res = self._api.post('/item/addFromURLs', items=items, folderId=folderId)
        return res

    def addFromPath(self, path: str, name: str, *, website: str | None = None,
                    tags: list[str] | None = None, annotation: str | None = None,
                    folderId: str | None = None, headers: dict = {}):
        res = self._api.post('/item/addFromPath', path=path, name=name,
                             website=website, tags=tags, annotation=annotation,
                             folderId=folderId, headers=headers)
        return res

    def addFromPaths(self, items: list[types.OfflineItem], folderId: str | None = None):
        res = self._api.post('/item/addFromPaths', items=items, folderId=folderId)
        return res

    def addBookmark(self, url: str, name: str, *, base64: str | None = None,
                    tags: list[str] | None = None,
                    modificationTime: int | None = None,
                    folderId: str | None = None):
        res = self._api.post('/item/addBookmark', url=url, name=name,
                             base64=base64, tags=tags,
                             modificationTime=modificationTime,
                             folderId=folderId)
        return res

    def info(self, id: str):
        res = self._api.get('/item/info', id=id)
        return (types._Item(**res['data'])
                if res['status'] == 'success' else res)

    def thumbnail(self, id: str) -> str | dict:
        res = self._api.get('/item/thumbnail', id=id)
        return res['data'] if res['status'] == 'success' else res

    def moveToTrash(self, itemIds: list[str]):
        res = self._api.post('/item/moveToTrash', itemIds=itemIds)
        return res

    def refreshPalette(self, id: str):
        res = self._api.post('/item/refreshPalette', id=id)
        return res

    def refreshThumbnail(self, id: str):
        res = self._api.post('/item/refreshThumbnail', id=id)
        return res

    def update(self, id: str, *, tags: list[str] | None = None,
               annotation: str | None = None, url: str | None = None,
               star: Literal[0, 1, 2, 3, 4, 5] | None = None):
        res = self._api.post('/item/update', id=id, tags=tags,
                             annotation=annotation, url=url, star=star)
        return (types._Item(**res['data'])
                if res['status'] == 'success' else res)

    def list(self, *, keyword: str | None = None, ext: str | None = None,
             orderBy: types.ORDER | None = None, limit: int = 200, offset: int = 0,
             tags: list[str] = [], folders: list[str] = []) -> list[types._Item] | dict:
        res = self._api.get('/item/list', keyword=keyword, ext=ext,
                            orderBy=orderBy, limit=limit, offset=offset,
                            tags=','.join(tags), folders=','.join(folders))
        return (types.maplist(res['data'], types._Item)
                if res['status'] == 'success' else res)


class _API_LIBRARY(_CHILD_API):
    def info(self):
        res = self._api.get('/library/info')
        return (types._LibraryInfo(**res['data'])
                if res['status'] == 'success' else res)

    def history(self):
        res = self._api.get('/library/history')
        return res['data'] if res['status'] == 'success' else res

    def switch(self, libraryPath: str):
        res = self._api.post('/library/switch', libraryPath=libraryPath)
        return res
