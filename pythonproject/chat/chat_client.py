#select模块对stdin的监听无法在windows运行
#！/usr/bin/python
from socket import *
import select,sys,datetime

port=1235
server='127.0.0.1'
client=socket(AF_INET,SOCK_STREAM)
client.connect((server,port))

def prompt():
    sys.stdout.write('send:')
    sys.stdout.flush()

while True:
    r_list = [sys.stdin, client]
    r_socket,w_socket,err_socket=select.select(r_list,[],[])
    for obj in r_socket:
        if obj==client:
            data=client.recv(1024)
            print 'recive:%s\n%s' % (datetime.datetime.now(),data.rstrip())
            prompt()
        else:
            prompt()
            data=sys.stdin.readline().rstrip()
            client.sendall(data)


