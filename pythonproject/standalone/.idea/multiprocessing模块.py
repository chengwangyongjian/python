# -*- coding: utf-8 -*
__author__ = 'zni.feng'
import  sys
reload (sys)
sys.setdefaultencoding('utf-8')

from multiprocessing import Process,Lock,Queue
import random,time,os
def write(q,lock,name):
    print '%s process start'%name
    lock.acquire()
    for value in ['a','b','c']:
        print 'put %s to queue...'%value
        q.put(value)
        time.sleep(random.random())
    lock.release()
    print '%s process ends'%name
def read(q,name,who):
    print '%s %s process start'%(who,name)
    while True:
        v=q.get()
        print '%s get %s from queue...'%(who,v)
        time.sleep(2)
    print 'process %s end'%name

if __name__=="__main__":
    q=Queue()
    lock=Lock()
    pw=Process(target=write,args=(q,lock,'write',))
    pr1=Process(target=read,args=(q,'read','pr1'))
    pr2=Process(target=read,args=(q,'read','pr2'))
    pw.start()
    pr1.start()
    pr2.start()