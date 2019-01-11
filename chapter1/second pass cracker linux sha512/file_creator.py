import hashlib
import uuid
for i in range(0,10):
        user=raw_input("Enter: ")
        pf=open("passfile.txt","a")
        salt=uuid.uuid4().hex
        pf.write(user+":"+hashlib.sha512(salt.encode()+user.encode()).hexdigest()+":"+salt+"\n")
        df=open("dictfile.txt","a")
        df.write(user+"\n")
