import hashlib
import os

files = {}
download_path = ""


def hash_data(data):
    hasher = hashlib.md5()
    hasher.update(data)
    return str(hasher.hexdigest())


def hashFile(filepath):
    hasher = hashlib.md5()
    try:
        with open(filepath, "rb") as afile:
            buf = afile.read()
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read()
        return hasher.hexdigest()
    except:
        print("Couldn't find/hash file " + filepath)


def refresh():
    for i in list(files):
        if files[i]["path"] != None:
            if not os.path.exists(files[i]["path"]):
                print("Removing file that no longer exists: " + str(files[i]["path"]))
                del files[i]


def addfile(path):
    name = os.path.basename(path)
    h = hashFile(path)
    files[h] = {"name": name, "path": path}
    return str(h)


def have_file(hash):
    refresh()
    if hash in files:
        return True


def getallfiles():
    refresh()
    return files
