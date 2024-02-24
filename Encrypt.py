class Encryptor:
    def Encrypt(msg):
        encmsg = ""
        for ch in msg:
            asc = ord(ch) + 3
            ench = chr(asc)
            encmsg += ench
        return encmsg
        
    def Decrypt(msg):
        uncmsg = ""
        for ch in msg:
            asc = ord(ch) - 3
            ench = chr(asc)
            uncmsg += ench
        return uncmsg