import ftplib

def check(ftp):
    try:
        dirList=ftp.nlst()
    except Exception as e:
        print(e)
        dirList=[]
        print('Could not list the directory contents')
        return dirList
    retList=[]
    for fileName in dirList:
        fn=fileName.lower()
        if '.php' in fn or '.htm' in fn or '.png' in fn or '.txt' in fn:
            print('[+] Found Defalt page: '+fileName)
            retList.append(fileName)
    return retList


host='test.rebex.net'
username='demo'
password='password'
ftp=ftplib.FTP(host)
ftp.login(username,password)
r=check(ftp)
print(r)