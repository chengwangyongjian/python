import MySQLdb

class get_data():
    def __init__(self):
        self.db = MySQLdb.connect('192.168.37.129', 'root', 'cheng', 'users')
        self.cursor=self.db.cursor()
        self.cursor.execute('show tables')
        self.alarm_list=self.cursor.fetchall()[:-1]
    def t_to_l(self,t1):
        t=()
        for i in range(len(t1)):
            t+=t1[i]
        return list(t)
    def get_date(self):
       return self.t_to_l(self.alarm_list)
    def get_person(self):
        d={}
        for item in self.alarm_list:
            SQL='select distinct submit_person from '+item[0]
            self.cursor.execute(SQL)
            t1=self.cursor.fetchall()
            l=self.t_to_l(t1)
            d[item[0]]=l
        return d
    def get_data(self):
        base_alarm=["'disk'","'raid'","'time'"]
        app_alarm=["'down'"]
        lose_alarm=["'lose'"]
        d1={}
        for table in self.t_to_l(self.alarm_list):
            d2={}
            for person in self.get_person()[table]:
                base_alarm_count, app_alarm_count, lose_alarm_count=0,0,0
                l=[]
                person2="'"+person+"'"
                sql='select count(*) from (select * from '+table+' where submit_person='+person2+') as A where alarm_type='
                for i in base_alarm:
                        SQL=sql+i
                        self.cursor.execute(SQL)
                        base_alarm_count+=self.cursor.fetchall()[0][0]
                for i in app_alarm:
                    SQL = sql + i
                    self.cursor.execute(SQL)
                    app_alarm_count += self.cursor.fetchall()[0][0]
                for i in lose_alarm:
                    SQL = sql + i
                    self.cursor.execute(SQL)
                    lose_alarm_count += self.cursor.fetchall()[0][0]
                SQL=sql+"'down'"
                self.cursor.execute(SQL)
                restart_count=self.cursor.fetchall()[0][0]
                l=[base_alarm_count,app_alarm_count,lose_alarm_count,restart_count]
                d2[person]=l
            d1[table]=d2
        return d1



