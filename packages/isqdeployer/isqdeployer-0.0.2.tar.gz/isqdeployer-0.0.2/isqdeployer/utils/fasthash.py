import hashlib



def fasthash(string):
    hashlib.md5(string.encode("utf-8")).hexdigest()

