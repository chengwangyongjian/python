#单进程版本
import socket,select
from multiprocessing import Process

port=1235
server=('0.0.0.0',port)
s=socket.socket()
s.bind(server)
s.listen(2)

inputs=[s,]
outputs=[]
mesg={}
client_list=[]

def forward_send(data,index):
    if len(inputs) == 3:
        try:
            inputs[index+1].sendall(data)
        except Exception:
            inputs[index-1].sendall(data)
    else:
        inputs[index].sendall('waiting for connecting...')

while True:
    r_list,w_list,err_list=select.select(inputs,outputs,inputs,10)
    for obj in r_list:
        if obj == s:
            conn,address = obj.accept()
            print 'new client connect:',address
            inputs.append(conn)
            mesg[conn]=[]
            conn.sendall('welcome to connect!')
        else:
            try:
                data=obj.recv(1024)
                index=inputs.index(obj)
                mesg[obj].insert(0,data)
                if obj not in outputs:
                    outputs.append(obj)
                print 'recv %s from %s:' % (data, obj.getpeername())
                forward_send(data,index)
            except Exception:
                print 'finish:',obj.getpeername()
                inputs.remove(obj)
                if obj in outputs:
                    outputs.remove(obj)
