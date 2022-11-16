from . import types
from .main import EagleAPI


class EagleAPIEx(EagleAPI):
    def __init__(self, url='http://localhost:41595') -> None:
        super().__init__(url)
    
    @staticmethod
    def __recGetFolderByID(folder: types._Folder, id: str):
        if folder.id == id:
            return folder
        else:
            for child in folder.children:
                result = EagleAPIEx.__recGetFolderByID(child, id)
                if result is not None:
                    return result
            return None
    
    def getFolderByID(self, id: str):
        folders = self.FOLDER.list()
        for folder in folders:
            result = EagleAPIEx.__recGetFolderByID(folder, id)
            if result is not None:
                return result
        return None
    
    @staticmethod
    def __recGetFoldersByName(folder: types._Folder, name: str):
        founded = []
        if folder.name == name:
            founded.append(folder)
        
        for child in folder.children:
            founded.extend(EagleAPIEx.__recGetFoldersByName(child, name))
        return founded
    
    def getFoldersByName(self, name: str, parent: types._Folder | None = None):
        if parent is None:
            folders = self.FOLDER.list()
        else:
            folders = [parent]
        founded = []
        for folder in folders:
            founded.extend(EagleAPIEx.__recGetFoldersByName(folder, name))
        return founded


if __name__ == "__main__":
    apiex = EagleAPiEx()
    