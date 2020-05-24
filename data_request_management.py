import json
import hashlib
from os import walk
import subprocess

mypath = "content/"

def hashFile(filepath):
    filepath = mypath + filepath
    BLOCKSIZE = 65536
    hasher = hashlib.md5()
    with open(filepath, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return(hasher.hexdigest())

f = []
for (dirpath, dirnames, filenames) in walk(mypath):
    f.extend(filenames)
    print(filenames)
    break

f2data= {}
f2data['data'] = []
with open('resources.json', 'w') as f2:
    for file in filenames:
        f2data['data'].append({
            'filename': file,
            'hash': hashFile(file)
        })
        json.dump(f2data, f2)
        f2data['data'] = []

def have_file(hash):
    if hash in f2data:
        return(True)
