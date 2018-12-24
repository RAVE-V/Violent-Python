import crypt
def testpass(cryptpass):
        salt=cryptpass[0:2]
        dictfile=open("dict.txt","r")
        for word in dictfile.readlines():
                word=word.strip("\n")
                cryptword=crypt.crypt(word,salt)
                if (cryptword==cryptpass):
                        print("[+] Password Found",cryptword," = ",word)
                        return
        print("[-] Password not found")
def main():
        passfile=open("passfile.txt","r")
        for line in passfile.readlines():
                line=line.strip("\n")
                if ":" in line:
                        user=line.split(":")[0]
                        cryptpass=line.split(":")[1]
                        print("[+] Cracking user :",user)
                        testpass(cryptpass)
if __name__=="__main__":
        main()
                
                
