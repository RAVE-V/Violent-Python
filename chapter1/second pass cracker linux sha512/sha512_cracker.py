import hashlib
def hashchecker(user,hashpass,salt):
        d=open("dictfile.txt","r")
        for word in d.readlines():
                word=word.strip("\n")
                hword=hashlib.sha512(salt.encode()+word.encode()).hexdigest()
                if hword == hashpass:
                        print("[+] Cracked \n\tuser :"+user+"\n\tpassword :"+word+"\n\thash :"+hashpass+"\n")
                        return
        return
        
def main():
        f=open("passfile.txt","r")
        for line in f.readlines():
                line=line.strip("\n")
                if ":" in line:
                        user=line.split(":")[0]
                        hashpass=line.split(":")[1]
                        salt=line.split(":")[2]
                        print("[!] Cracking password for "+user+"\n")
                        hashchecker(user,hashpass,salt)
                        
if __name__=="__main__":
        main()
