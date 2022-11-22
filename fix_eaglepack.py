from glob import glob
import json
import os
import shutil
from zipfile import ZipFile

unpacked_eaglepack_path = r"D:\Users\kent\Desktop\tmp\1667946958-1668978557"

paths = glob(unpacked_eaglepack_path + '\\*')
pack = {'images': []}
for path in [p for p in paths if os.path.isdir(p)]:
    basename = os.path.basename(path)
    if not basename.endswith('.info'):
        continue

    try:
        with open(path + '\\metadata.json') as f:
            data = json.load(f)
        pack['images'].append(data)
    except FileNotFoundError:
        print('"' + path + '\\metadata.json" is not founded.')

with open(unpacked_eaglepack_path + '\\pack.json', 'w') as f:
    json.dump(pack, f, ensure_ascii=False)

shutil.make_archive(unpacked_eaglepack_path, 'zip', unpacked_eaglepack_path)
shutil.move(unpacked_eaglepack_path + '.zip', unpacked_eaglepack_path + '.eaglepack')