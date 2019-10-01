#import libraries
import crypt
#loop statements
for i in range(10):
        f=raw_input("Enter u:")
        s=raw_input("Enter salt:")
        passfile=open("passfile.txt","a")
        passfile.write(f+":"+crypt.crypt(f,s)+"\n")
        dicti=open("dict.txt","a")
        dicti.write(f)
        
        
