import optparse
import nmap
def main():
    parser= optparse.OptionParser('usage:python portmon.py -H <target host> -p <target port>')
    parser.add_option('-H',dest='tgthost',type='string',help='Specify target ip address')
    parser.add_option('-p',dest='tgtport',type='string',help='Specify target port')
    (options,args)=parser.parse_args()
    tgthost=options.tgthost
    tgtport=options.tgtport
    if (tgthost == None) | (tgtport == None):
        print (parser.usage)
        exit(0)
    tgtport=tgtport.split(',')
    for TgtPort in tgtport:
        nmapScan(tgthost,TgtPort)


def nmapScan(tgthost,TgtPort):
    nmscan=nmap.PortScanner()
    nmscan.scan(tgthost,TgtPort)
    state=nmscan[tgthost]['tcp'][int(TgtPort)]['state']
    print('[+] '+ tgthost + 'TCP/' + TgtPort + ' : ' + state)

if __name__=="__main__":
    main()
