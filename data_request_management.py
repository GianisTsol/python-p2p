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
        with open('resources.json', 'w') as f2:
            json.dump(files, f2)

def addfile(path):
    name = os.path.basename(path)
    files[hashFile(path)] = {"name" : name, "path" : path}

def have_file(hash):
    refresh()
    if hash in files:
        return(True)

refresh()
