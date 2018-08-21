#!/usr/bin/python
import mysql.connector,functools
import threading

class DBctx(threading.local):
    def __init__(self):
        self.engine=None
        self.cursor=None
        self.should_close=True
    def engine_init(self,e):
        self.engine=e
    def cursor_init(self):
        self.cursor=self.engine.cursor()
    def cursor_close(self):
        self.cursor.close()
    def engine_close(self):
        self.engine=None

dbctx=DBctx()

class DBError(Exception):
    pass

def create_engine(user,password,database,host='192.168.37.129',port=3306):
    global dbctx
    if dbctx.engine:
        dbctx.engine_close()
        raise DBError('Engine is already inited')
    engine=mysql.connector.connect(user=user,password=password,database=database,host='192.168.37.129',port=3306)
    dbctx.engine_init(engine)

class with_conn(object):
    def __enter__(self):
        global dbctx
        dbctx.cursor_init()
    def __exit__(self,types,info,trace):
        global dbctx
        dbctx.cursor_close()
        if dbctx.should_close:
            dbctx.engine_close()

class conn(object):
    def __enter__(self):
        global dbctx
        dbctx.should_close=False
    def __exit__(self, exc_type, exc_val, exc_tb):
        global dbctx
        dbctx.should_close=True
        dbctx.engine_close()

def connection(func):
    @functools.wraps(func)
    def _wrapper(*args,**kwargs):
        with with_conn():
            return func(*args,**kwargs)
    return _wrapper

@connection
def select(sql,*args):
    sql=sql.replace('?','%s')
    dbctx.cursor.execute(sql,args)
    keys=tuple(i[0] for i in dbctx.cursor.description)
    return [dict(zip(keys,j)) for j in dbctx.cursor.fetchall()]

@connection
def update(sql,*args):
    sql = sql.replace('?', '%s')
    dbctx.cursor.execute(sql,args)
    return dbctx.cursor.rowcount

def insert(table,**args):
    key,value=zip(*args.iteritems())
    sql='insert into %s (%s) values(%s)'%(table,','.join(list(key)),','.join(['?' for i in range(len(key))]))
    update(sql,*value)

if __name__=='__main__':
    '''create_engine('root','cheng','test')
    with conn():
        select('select * from em')
        select('select f_name from em')'''
    create_engine('root', 'cheng', 'awesome')
    d=select('select * from User where id=?',1)[0]
    '''def t1():
        create_engine('root', 'cheng', 'test')
        select('select * from em')
    def t2():
        create_engine('root', 'cheng', 'users')
        select('select * from d20171128')
    th1=threading.Thread(target=t1,name='th1')
    th2=threading.Thread(target=t2,name='th2')
    th1.start()
    th2.start()'''
