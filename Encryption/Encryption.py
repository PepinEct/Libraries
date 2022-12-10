import json, random, gzip
class Key:
    __EncAlph__ = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 !@#$%^&*()-={}[];:<>,.?"
    __EncChars__ = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()"
    __DefFileName__="Key"
    key = {}
    def __init__(self, MINlen:int=5, MAXlen:int=10, AddChars:str="") -> None:
        self.MINlen = MINlen
        self.MAXlen = MAXlen
        for char in AddChars:
            self.__EncAlph__+=char
        if MINlen < 1:
            raise IndexError("MINlen can't be less than 1")
    def make(self):
        for char in self.__EncAlph__:
            out = ""
            ranLen = random.randint(self.MINlen, self.MAXlen)
            for x in range(ranLen):
                out+=self.__EncChars__[random.randint(0, len(self.__EncChars__)-1)]
            self.key[char] = out
    def write(self, filename=__DefFileName__):
        if len(self.key) == 0:
            raise Exception("Empty Key Error")
        data = gzip.compress(json.dumps(self.key).encode(), 9)
        with open(filename, 'wb')as file:
            file.write(data)
    def load(self, filename=__DefFileName__):
        with open(filename, 'rb') as file:
            data = file.read()
        self.key = json.loads(gzip.decompress(data).decode())
def Encrypt(key:Key, msg:str):
    if type(key) != Key:
        raise(TypeError)
    out=""
    for char in msg:
        out+=key.key[char]
    return out
def DeEncrypt(key:Key, msg:str):
    if type(key)!=Key:
        raise(TypeError)
    out = ""
    temp = ""
    for char in msg:
        temp+=char
        for x in key.key:
            if temp == key.key[x]:
                out+=x
                temp = ""
                break    
    return out