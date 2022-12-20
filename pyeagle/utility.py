from glob import glob
import json
import os
from datetime import datetime
from typing import TYPE_CHECKING, Literal, Type, overload

from . import types

if TYPE_CHECKING:
    from .main import EagleAPI

from .types import UNDEFINED, _Folder


class Backup():
    def __init__(self) -> None:
        self.backups = {}

    def backup(self, *paths):
        for path in paths:
            abspath = os.path.abspath(path)
            with open(abspath, 'rb') as f:
                self.backups[abspath] = f.read()

    def restore(self):
        for k, v in self.backups:
            with open(k, 'wb') as f:
                f.write(v)


class Utility():
    def __init__(self, eapi: 'EagleAPI') -> None:
        self.__eapi = eapi
    
    @staticmethod
    def __recGetFolderByID(folder: types._Folder, id: str) -> types._Folder | None:
        if folder.id == id:
            return folder
        else:
            for child in folder.children:
                result = Utility.__recGetFolderByID(child, id)
                if result is not None:
                    return result
            return None
    
    @overload
    def getFolderByID(self, id: str) -> types._Folder | None: ...
    @overload
    def getFolderByID(self, id: str, raise_error: Literal[True] = True) -> types._Folder: ...
    @overload
    def getFolderByID(self, id: str, raise_error: Literal[False] = False) -> types._Folder | None: ...

    def getFolderByID(self, id: str, raise_error=False) -> types._Folder | None:
        folders = self.__eapi.FOLDER.list()
        for folder in folders:
            result = Utility.__recGetFolderByID(folder, id)
            if result is not None:
                return result
        if raise_error:
            raise KeyError(f'folder id {id} is not found.')
        else:
            return None
    
    @staticmethod
    def __recGetFoldersByName(folder: types._Folder, name: str) -> list[types._Folder]:
        founded = []
        if folder.name == name:
            founded.append(folder)
        
        for child in folder.children:
            founded.extend(Utility.__recGetFoldersByName(child, name))
        return founded
    
    def getFoldersByName(self, name: str, parent: types._Folder | None = None) -> list[types._Folder]:
        """
        Find Eagle Folders by using folder name. (Perfect matching)

        Return is list of EagleFolder.

        Parameters
        ----------
        name : str

        parent : types._Folder | None, optional
            None -> Find from all folders
            _Folder() -> Find from Children.

        Returns
        -------
        list[types._Folder]

        """
        if parent is None:
            folders = self.__eapi.FOLDER.list()
        else:
            folders = [parent]
        founded = []
        for folder in folders:
            founded.extend(Utility.__recGetFoldersByName(folder, name))
        return founded
    
    @staticmethod
    def __open_json(path: str, limit=30, sleep=0.1):
        for _ in range(limit):
            try:
                with open(path) as f:
                    data = json.load(f)
                break
            except json.JSONDecodeError as err:
                error = err
        else:
            raise error
        
        return data
    
    def renameItem(self, fileid: str, new_name: str):
        """rename eagle file

        Warning!
        --------
        This method work without eagle api

        I will not bear full responsibility for using this.

        Parameters
        ----------
        fileid : str
            
        new_name : str
            new name without extention.
        """
        backup = Backup()
        try:
            # prepare variables
            timestamp = int(datetime.utcnow().timestamp() * 1000)
            item_dir = f'{self.__eapi.__libpath__}\\images\\{fileid}.info'

            # load metadata
            meta_path = item_dir + '\\metadata.json'
            metadata = Utility.__open_json(meta_path)
            backup.backup(meta_path)
            
            mtime_path = self.__eapi.__libpath__ + '\\mtime.json'
            mtime = Utility.__open_json(mtime_path)
            backup.backup(mtime_path)

            # rename files
            old_name = metadata['name']
            old_ext = metadata['ext']

            old_path = f'{item_dir}\\{old_name}.{old_ext}'
            old_thumb_path = f'{item_dir}\\{old_name}_thumbnail.png'
            new_path = f'{item_dir}\\{new_name}.{old_ext}'
            new_thumb_path = f'{item_dir}\\{new_name}_thumbnail.png'

            if os.path.exists(old_path):
                os.rename(old_path, new_path)
            if os.path.exists(old_thumb_path):
                os.rename(old_thumb_path, new_thumb_path)

            # update metadata
            metadata['name'] = new_name
            metadata['lastModified'] = timestamp

            mtime[fileid] = timestamp

            # write metadata
            with open(mtime_path, 'w') as f:
                json.dump(mtime, f)
            with open(meta_path, 'w') as f:
                json.dump(metadata, f, ensure_ascii=False)
            
        except:  # noqa: E722
            backup.restore()
            if 'new_path' in locals() and os.path.exists(new_path):
                os.rename(new_path, old_path)
            if 'new_thumb_path' in locals() and os.path.exists(new_thumb_path):
                os.rename(new_thumb_path, old_thumb_path)
            
            raise
    @overload
    def itemOriginalFilePath(self, item: types._Item) -> str: ...
    @overload
    def itemOriginalFilePath(self, id: str, filename: str) -> str: ...
    @overload
    def itemOriginalFilePath(self, id: str, filestem: str, ext: str) -> str: ...
    
    def itemOriginalFilePath(self, *args, **kwargs) -> str:
        if isinstance(args[0], types._Item):
            return self.__eapi.__libpath__ + '\\images\\' + args[0].id + '.info\\' + args[0].name + '.' + args[0].ext
        elif len(args) == 2:
            return self.__eapi.__libpath__ + '\\images\\' + args[0] + '.info\\' + args[1]
        else:
            return self.__eapi.__libpath__ + '\\images\\' + args[0] + '.info\\' + args[1] + '.' + args[2]
        
    def itemThumbnailFilePath(self, item: types._Item):
        return self.__eapi.__libpath__ + '\\images\\' + item.id + '.info\\' + item.name + '_thumbnail.png'
    
    def importFolder(self, src: str, name: str | None = None,
                     parent: str | None = None,
                     website: str | Type[UNDEFINED] = UNDEFINED,
                     tags: list[str] | Type[UNDEFINED] = UNDEFINED,
                     annotation: str | Type[UNDEFINED] = UNDEFINED):
        if not name:
            name = os.path.basename(src)
        pfolder = self.__eapi.FOLDER.create(name, parent)
        if not isinstance(pfolder, types._NewFolder):
            raise RuntimeError('Create Folder Faild')

        paths = glob(src + '\\*')
        for dir in [p for p in paths if os.path.isdir(p)]:
            self.importFolder(dir, None, pfolder.id, website, tags, annotation)
        append_files: list[types.OfflineItem] = []
        for file in [p for p in paths if os.path.isfile(p)]:
            append_files.append(types.OfflineItem(
                os.path.abspath(file),
                '.'.join(os.path.basename(file).split('.')[:-1]),
                website=website,
                tags=tags,
                annotation=annotation
            ))
        if len(append_files) > 0:
            self.__eapi.ITEM.addFromPaths(append_files, pfolder.id)


    @staticmethod
    def recursive_get_parents(target_id: str, parent: _Folder) -> list[_Folder] | None:
        if target_id in [c.id for c in parent.children]:
            return [parent] + [c for c in parent.children if c.id == target_id]
        elif target_id == parent.id:
            return [parent]
        
        for child in parent.children:
            parents = Utility.recursive_get_parents(target_id, child)
            if isinstance(parents, list):
                return [parent] + parents
            else:
                pass
        
        return None
    
    def get_parents(self, target_id: str, root_parent: _Folder):
        parents = Utility.recursive_get_parents(target_id, root_parent)

        if parents is None:
            raise KeyError(f'Folder "{target_id}" '
                           f'is not grandchild of '
                           f'Folder "{root_parent.id}"')
                           
        return parents


if __name__ == "__main__":
    pass
    