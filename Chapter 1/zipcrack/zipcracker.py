import zipfile
import optparse
from threading import Thread

def extractFile(zfile,passwd):
    print passwd
    try:
        zfile.extractall(pwd=passwd)
        print'[+] Found Password '+passwd+'\n'
    except Exception,e:
        print e
        pass

def main():
    parser=optparse.OptionParser("Usage : zipcracker.py -f <zipfile> -d <dictionary>")
    parser.add_option('-f',dest='zname',type='string',help='specify zip file')
    parser.add_option('-d',dest='dname',type='string',help='specify dictionary file')
    (options,args)=parser.parse_args()
    if(options.zname == None) | (options.dname== None):
        print(parser.usage)
        exit(0)
    else:
        zname=options.zname
        dname=options.dname
        zfile=zipfile.ZipFile(zname)
        passfile=open(dname)
        for line in passfile.readlines():
            password=line.strip('\n')
            print 'trying '+password
            t=Thread(target=extractFile, args=(zfile,password))
            t.start()
if __name__=='__main__':
    main()
