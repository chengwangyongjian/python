# -*-coding:utf-8 -*-
import MySQLdb,sys
reload(sys)
sys.setdefaultencoding('utf-8')

class mysql:
    def __init__(self):
        try:
            self.db=MySQLdb.connect('127.0.0.1','root','cheng','ask')
            self.cursor = self.db.cursor()
        except MySQLdb.Error,e:
            print 'error,reason%d:%s'%(e.args[0],e.args[1])
    def check_exist(self,table,title):
        sql='SELECT title FROM %s'%table
        self.cursor.execute(sql)
        result=self.cursor.fetchall()
       # print result[0][0].decode('utf-8')
        for i in result:
            if title in i[0].decode('utf-8'):
                return False
        return True
    def insert_data(self,table,my_dict):
            try:
                self.db.set_character_set('utf8')
                col=','.join(my_dict.keys())
                value='","'.join(my_dict.values())
                sql="INSERT INTO %s(%s) VALUES(%s)" %(table,col,'"'+value+'"')
                if self.check_exist(table,my_dict['title']):
                    self.cursor.execute(sql)
                    self.db.commit()
                else:print my_dict['title']+' has existed!'
            except MySQLdb.Error,e:
                print e,"creating..."
                sql='CREATE TABLE IF NOT EXISTS question(\
                    title varchar(1000),\
                    addr varchar(200),\
                    answer varchar(1000)\
                    )'
                self.cursor.execute(sql)
                print 'create finish'
                print 'start insert'
                self.insert_data(table,my_dict)





