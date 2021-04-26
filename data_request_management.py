import json
import hashlib
from os import walk
import subprocess

mypath = "content/"
filenamess = []

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
def refresh():
    for (dirpath, dirnames, filenames) in walk(mypath):
        f.extend(filenames)
        filenamess = filenames
        break

f2data= {}

with open('resources.json', 'w') as f2:
    for file in filenamess:
        f2data[hashFile(file)] = file
        json.dump(f2data, f2)

def have_file(hash):
    if hash in f2data:
        return(True)

refresh()
