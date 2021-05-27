import json
import hashlib
import os

files = {}
download_path = "content/"


def hashFile(filepath):
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as afile:
            buf = afile.read()
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read()
        return(hasher.hexdigest())
    except:
        print("Couldn't find/hash file " + filepath)


def refresh():
    f = []
    for (dirpath, dirnames, filenames) in os.walk(download_path):
        f.extend(filenames)
        for file in filenames:
            addfile(download_path + file)
    for i in list(files):
        if files[i]["path"] != None:
            if not os.path.exists(files[i]["path"]):
                del files[i]

def addfile(path):
    name = os.path.basename(path)
    h = hashFile(path)
    files[h] = {"name" : name, "path" : path}
    return(h)

def have_file(hash):
    refresh()
    if hash in files:
        return(True)

def getallfiles():
    return(files)

refresh()
