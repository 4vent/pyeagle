import json
import warnings
from typing import Any, Literal, Type, TypeVar

UNDEFINED = type('UNDEFINED', (object,), {})
STATUS = Literal['success', 'error']
COLOR = Literal['red', 'orange', 'green', 'yellow',
                'aqua', 'blue', 'purple', 'pink']
ORDER = Literal['CREATEDATE', 'FILESIZE', 'NAME', 'RESOLUTION',
                '-CREATEDATE', '-FILESIZE', '-NAME', '-RESOLUTION']


class EagleJSONEncoder(json.encoder.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, APIResponce):
            newdict = {}
            for k, v in o.__dict__.items():
                if k in [] or v == UNDEFINED:
                    continue

                if k == '_hashKey':
                    newdict['$$hashKey'] = v
                else:
                    newdict[k] = v
            return newdict
        else:
            return super().default(o)


class APIResponce():
    def __init__(self, **kwargs) -> None:

        for k, v in kwargs.items():
            warnings.warn(f'Unknown Key "{k}" in <{type(self).__name__}>. (Module bug or Updated Fanbox API.) '
                          'You can use this key but there is no autocomplete.')
            setattr(self, k, v)


# T = TypeVar('EagleResponce', (_NewFolder, _Palette, _Item, _Styles, _ImagesMappings, _Folder, _Rule))
# T = TypeVar('EagleResponce', APIResponce)


def maplist(_l: list[dict], type: Type[APIResponce]) -> list[APIResponce]:
    if _l == UNDEFINED:
        return UNDEFINED  # type: ignore
    elif _l is None:
        return None  # type: ignore
    else:
        return list(map(lambda x: type(**x), _l))


def mapdict(_d: dict[str, dict], type: type) -> dict[str, Any]:
    if _d == UNDEFINED:
        return UNDEFINED  # type: ignore
    elif _d is None:
        return None  # type: ignore
    else:
        return {k: type(**v) for k, v in _d.items()}


# === Responce Element ===

class _NewFolder(APIResponce):
    def __init__(self, id: str,
                 name: str,
                 images: list,
                 folders: list,
                 modificationTime: int,
                 imagesMappings: dict,
                 tags: list,
                 children: list,
                 isExpand: bool,
                 **kwargs) -> None:
        
        self.id = id
        self.name = name
        self.images = images
        self.folders = folders
        self.modificationTime = modificationTime
        self.imagesMappings = imagesMappings
        self.tags = tags
        self.children = children
        self.isExpand = isExpand

        super().__init__(**kwargs)


class _Palette(APIResponce):
    def __init__(self, color: list[int],
                 ratio: int,
                 **kwargs) -> None:
        
        self.color = color
        self.ratio = ratio

        if '$$hashKey' in kwargs:
            self._hashKey: str = kwargs['$$hashKey']
            del kwargs['$$hashKey']
        else:
            self._hashKey: str = UNDEFINED  # type: ignore
        
        super().__init__(**kwargs)


class _Item(APIResponce):
    def __init__(self, id: str,
                 name: str,
                 size: int,
                 btime: int,
                 mtime: int,
                 ext: str,
                 tags: list[str],
                 folders: list[str],
                 isDeleted: bool,
                 url: str,
                 annotation: str,
                 modificationTime: int,
                 height: int = UNDEFINED,  # type: ignore
                 width: int = UNDEFINED,  # type: ignore
                 palettes: list[dict] = UNDEFINED,  # type: ignore
                 lastModified: int = UNDEFINED,  # type: ignore
                 noThumbnail: bool = UNDEFINED,  # type: ignore
                 deletedTime: int = UNDEFINED,  # type: ignore
                 noPreview: bool = UNDEFINED,  # type: ignore
                 text: str = UNDEFINED,  # type: ignore
                 duration: int = UNDEFINED,  # type: ignore
                 **kwargs) -> None:
        
        self.id = id
        self.name = name
        self.size = size
        self.btime = btime
        self.mtime = mtime
        self.ext = ext
        self.tags = tags
        self.folders = folders
        self.isDeleted = isDeleted
        self.url = url
        self.annotation = annotation
        self.modificationTime = modificationTime
        self.height = height
        self.width = width
        self.palettes: list[_Palette] = maplist(palettes, _Palette)
        self.lastModified = lastModified
        self.noThumbnail = noThumbnail
        self.deletedTime = deletedTime
        self.noPreview = noPreview
        self.text = text
        self.duration = duration

        super().__init__(**kwargs)


class _Styles(APIResponce):
    def __init__(self, depth: int,
                 first: bool,
                 last: bool,
                 **kwargs) -> None:
        
        self.depth = depth
        self.first = first
        self.last = last

        super().__init__(**kwargs)


class _ImagesMappings(APIResponce):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class _Folder(APIResponce):
    def __init__(self, id: str,
                 name: str,
                 description: str,
                 children: list[dict],
                 modificationTime: int,
                 tags: list[str], *,
                 imageCount: int = UNDEFINED,  # type: ignore
                 descendantImageCount: int = UNDEFINED,  # type: ignore
                 pinyin: str = UNDEFINED,  # type: ignore
                 extendTags: list[str] = UNDEFINED,  # type: ignore
                 password: str = UNDEFINED,  # type: ignore
                 passwordTips: str = UNDEFINED,  # type: ignore
                 parent: str = UNDEFINED,  # type: ignore
                 isExpand: bool = UNDEFINED,  # type: ignore
                 images: list[dict] = UNDEFINED,  # type: ignore
                 size: int = UNDEFINED,  # type: ignore
                 vstype: Literal['folder'] = UNDEFINED,  # type: ignore
                 styles: dict = UNDEFINED,  # type: ignore
                 isVisible: bool = UNDEFINED,  # type: ignore
                 imagesMappings: dict = UNDEFINED,  # type: ignore
                 covers: list[str] = UNDEFINED,  # type: ignore
                 index: int = UNDEFINED,  # type: ignore
                 newFolderName: str = UNDEFINED,  # type: ignore
                 editable: bool = UNDEFINED,  # type: ignore
                 iconColor: str = UNDEFINED,  # type: ignore
                 icon: str = UNDEFINED,  # type: ignore
                 coverId: str = UNDEFINED,  # type: ignore
                 orderBy: str = UNDEFINED,  # type: ignore
                 sortIncrease: bool = UNDEFINED,  # type: ignore
                 isSelected: bool = UNDEFINED,  # type: ignore
                 **kwargs) -> None:
        
        self.id = id
        self.name = name
        self.description = description
        self.children: list[_Folder] = maplist(children, _Folder)
        self.modificationTime = modificationTime
        self.tags = tags
        self.password = password
        self.passwordTips = passwordTips
        self.parent = parent
        self.isExpand = isExpand
        self.images: list[_Item] = maplist(images, _Item)
        self.size = size
        self.vstype = vstype
        self.styles = _Styles(**styles) if styles is not UNDEFINED else UNDEFINED
        self.isVisible = isVisible
        self.index = index
        self.newFolderName = newFolderName
        self.imagesMappings = _ImagesMappings(**imagesMappings) if imagesMappings is not UNDEFINED else UNDEFINED
        self.imageCount = imageCount
        self.descendantImageCount = descendantImageCount
        self.pinyin = pinyin
        self.extendTags = extendTags
        self.covers = covers
        self.editable = editable
        self.iconColor = iconColor
        self.icon = icon
        self.coverId = coverId
        self.orderBy = orderBy
        self.sortIncrease = sortIncrease
        self.isSelected = isSelected

        if '$$hashKey' in kwargs:
            self._hashKey: str = kwargs['$$hashKey']
            del kwargs['$$hashKey']
        else:
            self._hashKey: str = UNDEFINED  # type: ignore

        super().__init__(**kwargs)


class _Rule(APIResponce):
    def __init__(self, property: str,
                 method: str,
                 value: str,
                 **kwargs) -> None:
        
        self.property = property
        self.method = method
        self.value = value

        if '$$hashKey' in kwargs:
            self._hashKey: str = kwargs['$$hashKey']
            del kwargs['$$hashKey']
        else:
            self._hashKey: str = UNDEFINED  # type: ignore

        super().__init__(**kwargs)


class _Condition(APIResponce):
    def __init__(self, rules: list[dict],
                 match: Literal['AND', 'OR'],
                 boolean: Literal['TRUE', 'FALSE'],
                 **kwargs) -> None:
        
        self.rules: list[_Rule] = maplist(rules, _Rule)
        self.match = match
        self.boolean = boolean

        if '$$hashKey' in kwargs:
            self._hashKey: str = kwargs['$$hashKey']
            del kwargs['$$hashKey']
        else:
            self._hashKey: str = UNDEFINED  # type: ignore
        
        super().__init__(**kwargs)


class _SmartFolder(_Folder):
    def __init__(self, conditions: list[dict],
                 id: str,
                 name: str,
                 description: str,
                 children: list[dict],
                 modificationTime: int, *,
                 tags: list[str] = UNDEFINED,  # type: ignore
                 imageCount: int = UNDEFINED,  # type: ignore
                 descendantImageCount: int = UNDEFINED,  # type: ignore
                 pinyin: str = UNDEFINED,  # type: ignore
                 extendTags: list[str] = UNDEFINED,  # type: ignore
                 password: str = UNDEFINED,  # type: ignore
                 passwordTips: str = UNDEFINED,  # type: ignore
                 parent: str = UNDEFINED,  # type: ignore
                 isExpand: bool = UNDEFINED,  # type: ignore
                 images: list[dict] = UNDEFINED,  # type: ignore
                 size: int = UNDEFINED,  # type: ignore
                 vstype: Literal['folder'] = UNDEFINED,  # type: ignore
                 styles: dict = UNDEFINED,  # type: ignore
                 isVisible: bool = UNDEFINED,  # type: ignore
                 imagesMappings: dict = UNDEFINED,  # type: ignore
                 covers: list[str] = UNDEFINED,  # type: ignore
                 index: int = UNDEFINED,  # type: ignore
                 newFolderName: str = UNDEFINED,  # type: ignore
                 editable: bool = UNDEFINED,  # type: ignore
                 iconColor: str = UNDEFINED,  # type: ignore
                 icon: str = UNDEFINED,  # type: ignore
                 coverId: str = UNDEFINED,  # type: ignore
                 orderBy: str = UNDEFINED,  # type: ignore
                 sortIncrease: bool = UNDEFINED,  # type: ignore
                 **kwargs) -> None:
        
        self.conditions: list[_Condition] = maplist(conditions, _Condition)

        super().__init__(id, name, description, children, modificationTime, tags,
                         imageCount=imageCount, descendantImageCount=descendantImageCount,
                         pinyin=pinyin, extendTags=extendTags,
                         password=password, passwordTips=passwordTips,
                         parent=parent, isExpand=isExpand, images=images,
                         size=size, vstype=vstype, styles=styles,
                         isVisible=isVisible, imagesMappings=imagesMappings,
                         covers=covers, index=index, newFolderName=newFolderName,
                         editable=editable, iconColor=iconColor, icon=icon,
                         coverId=coverId, orderBy=orderBy,
                         sortIncrease=sortIncrease, **kwargs)


class _TagsGroup(APIResponce):
    def __init__(self, id: str,
                 name: str,
                 tags: list[str],
                 color: str,
                 **kwargs) -> None:

        self.id = id
        self.name = name
        self.tags = tags
        self.color = color

        super().__init__(**kwargs)


# === Eagle API Responce ===

class _ApplicationInfo(APIResponce):
    def __init__(self, version: str,
                 prereleaseVersion: str | None,
                 buildVersion: str,
                 execPath: str,
                 platform: str,
                 **kwargs) -> None:
        
        self.version = version
        self.prereleaseVersion = prereleaseVersion
        self.buildVersion = buildVersion
        self.execPath = execPath
        self.platform = platform

        super().__init__(**kwargs)


class _LibraryInfo(APIResponce):
    def __init__(self, folders: list[dict],
                 smartFolders: list[dict],
                 quickAccess: list[Any],
                 tagsGroups: list[dict],
                 modificationTime: int,
                 applicationVersion: str,
                 library: dict,
                 **kwargs) -> None:

        self.folders: list[_Folder] = maplist(folders, _Folder)
        self.smartFolders: list[_SmartFolder] = maplist(smartFolders, _SmartFolder)
        self.quickAccess: list[APIResponce] = maplist(quickAccess, APIResponce)
        self.tagsGroups: list[_TagsGroup] = maplist(tagsGroups, _TagsGroup)
        self.modificationTime = modificationTime
        self.applicationVersion = applicationVersion
        self.library = library

        super().__init__(**kwargs)


# ===

class OnlineItem(APIResponce):
    def __init__(self, url: str,
                 name: str, *,
                 website: str = UNDEFINED,  # type: ignore
                 tags: list[str] = UNDEFINED,  # type: ignore
                 annotation: str = UNDEFINED,  # type: ignore
                 modificationTime: int = UNDEFINED,  # type: ignore
                 headers: dict = UNDEFINED,  # type: ignore
                 **kwargs) -> None:

        self.url = url
        self.name = name
        self.website = website
        self.tags = tags
        self.annotation = annotation
        self.modificationTime = modificationTime
        self.headers = headers

        super().__init__(**kwargs)


class OfflineItem(APIResponce):
    def __init__(self, path: str,
                 name: str, *,
                 website: str = UNDEFINED,  # type: ignore
                 tags: list[str] = UNDEFINED,  # type: ignore
                 annotation: str = UNDEFINED,  # type: ignore
                 headers: dict = UNDEFINED,  # type: ignore
                 **kwargs) -> None:

        self.path = path
        self.name = name
        self.website = website
        self.tags = tags
        self.annotation = annotation
        self.headers = headers

        super().__init__(**kwargs)