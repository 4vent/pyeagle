import json
import os
import pathlib
import random
import time
import zipfile

import chardet
from numpy import base_repr

TYPE_IMAGE =  ['bmp', 'eps', 'gif', 'heic', 'ico', 'jpeg', 'jpg', 'png', 'svg',  # noqa: E222
               'tif', 'tiff', 'ttf', 'webp', 'base64']
TYPE_3D =     ['fbx', 'obj', 'dds', 'exr', 'hdr', 'tga', 'blend']  # noqa: E222
TYPE_SOURCE = ['afdesign', 'afphoto', 'afpub', 'ai', 'c4d', 'cdr', 'clip',
               'dwg', 'graffle', 'idml', 'indd', 'indt', 'psb', 'psd', 'skp',
               'xd', 'xmind']
TYPE_VIDEO =  ['m4v', 'mp4', 'webm', 'wmv', 'avi', 'mov']  # noqa: E222
TYPE_AUDIO =  ['aac', 'flac', 'm4a', 'mp3', 'ogg', 'wav']  # noqa: E222
TYPE_FONT =   ['ttf', 'ttc', 'otf', 'woff']  # noqa: E222
TYPE_OFFICE = ['txt', 'pdf', 'potx', 'ppt', 'pptx', 'xls', 'xlsx', 'doc',
               'docx', 'eddx', 'emmx']
CANPREVIEW =  (TYPE_IMAGE + TYPE_3D + TYPE_SOURCE + TYPE_VIDEO  # noqa: E222
               + TYPE_AUDIO + TYPE_FONT + TYPE_OFFICE)


class EagleItem():
    id_str = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def __init__(self, path: str, *, name: str | None = None, tags: list[str] = [],
                 folders: list[str] = [], isDeleted: bool = False,
                 url: str = '', annotation: str = '') -> None:
        self.path = path
        self.purepath = pathlib.PurePath(path.replace('\\', '/'))
        file_stat = os.stat(self.path)

        now_ms = int(time.time() * 1000)
        self.id = base_repr(now_ms, 36) + ''.join(random.choices(self.id_str, k=5))

        self.name = name if name else self.purepath.stem
        self.size = os.path.getsize(path)

        mtime = file_stat.st_mtime
        try:
            btime = file_stat.st_ctime if os.name == 'nt' else file_stat.st_birthtime
        except AttributeError:
            btime = file_stat.st_mtime
        self.mtime = int(mtime * 1000)
        self.btime = int(btime * 1000)

        ext = self.purepath.suffix[1:].lower()
        self.ext = ext if not ext == 'jpeg' else 'jpg'

        self.tags = tags
        self.folders = folders
        self.isDeleted = isDeleted
        self.url = url
        self.annotation = annotation
        self.modificationTime = now_ms
        self.lastModified = now_ms

        self.text = None
        self.palettes = None
        self.noPreview = False
        self.check_text()
        self.check_preview()
    
    def check_text(self):
        if not self.ext == 'txt':
            return
        
        with open(self.path, 'rb') as f:
            data = f.read()
            try:
                self.text = data.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    self.text = data.decode('shift-jis')
                except UnicodeDecodeError:
                    encoding = chardet.detect(data)['encoding']
                    self.text = data.decode(encoding=encoding, errors='replace')
            del data

    def check_preview(self):
        if self.ext in CANPREVIEW:
            self.palettes = []
        else:
            self.noPreview = True
    
    def get_metadata_dict(self):
        result = {
            'id': self.id,
            'name': self.name,
            'size': self.size,
            'mtime': self.mtime,
            'btime': self.btime,
            'ext': self.ext,
            'tags': self.tags,
            'folders': self.folders,
            'isDeleted': self.isDeleted,
            'url': self.url,
            'annotation': self.annotation,
            'modificationTime': self.modificationTime,
            'lastModified': self.lastModified
        }
        if self.text is not None:
            result['text'] = self.text
        if self.palettes is not None:
            result['palettes'] = self.palettes
        if self.noPreview is True:
            result['noPreview'] = self.noPreview
        
        return result


class EaglePack():
    def __init__(self, items: list[EagleItem] | None = None) -> None:
        self.items = items if items else []
    
    def appendItem(self, item: EagleItem):
        self.items.append(item)
    
    def appendItems(self, items: list[EagleItem]):
        self.items.extend(items)
    
    def exportEaglePack(self, dst):
        with zipfile.ZipFile(dst, 'w', zipfile.ZIP_STORED, ) as zf:
            images = []
            for item in self.items:
                metadata = item.get_metadata_dict()
                zf.write(item.path, arcname=f'{item.id}.info\\{item.name}.{item.ext}')
                zf.writestr(f'{item.id}.info\\metadata.json', json.dumps(metadata, ensure_ascii=False))
                images.append(metadata)
            zf.writestr('pack.json', json.dumps({'images': images}, ensure_ascii=False))