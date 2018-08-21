#多进程版本
#!/usr/bin/python
import socket,select
from multiprocessing import Process

def forward_send(data,index,inputs):
    if index==0:
        inputs[1].sendall(data)
    else:
        inputs[0].sendall(data)

def link(inputs):
    while True:
        r_list, w_list, err_list = select.select(inputs,outputs,[])
        for obj in r_list:
            data = obj.recv(1024)
            index = inputs.index(obj)
            if data:
               # mesg[obj].insert(0, data)
                if obj not in outputs:
                    outputs.append(obj)
                print 'recv %s from %s:' % (data, obj.getpeername())
                forward_send(data, index, inputs)
            else:
                print 'end:', obj.getpeername()
                forward_send('your partner offline', index, inputs)
                return

def make_process():
    while True:
        r, w, err = select.select([s, ], [], [])
        if r[0] == s:
            conn, address = s.accept()
            print 'new client connect:', address
            #mesg[conn] = []
            conn.sendall('welcome to connect!')
            global client_list
            client_list.append(conn)
            if len(client_list) == 2:
                print 'one connection got'
                inputs = client_list[:]
                client_list = []
                p=Process(target=link,args=(inputs,))
                p.start()
            else:
                conn.sendall('waiting for your partner connecting...')

port = 8000
server = ('192.168.37.136', port)
s = socket.socket()
s.bind(server)
s.listen(10)
outputs = []
#mesg = {}
client_list = []
make_process()
