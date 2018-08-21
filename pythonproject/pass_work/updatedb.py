import MySQLdb

def update_db(today,username,submit_time,host,type,status):
    host2 = "'" + host + "'"
    type2="'"+type+"'"
    status2="'"+status+"'"
    submit_time2="'"+submit_time+"'"
    username2="'"+username+"'"
    db = MySQLdb.connect('192.168.37.129', 'root', 'cheng', 'users')
    cursor = db.cursor()
    SQL='insert into '+'d'+today+'(submit_time,host,alarm_type,status,submit_person) values('+','.join([submit_time2,host2,type2,status2,username2])+')'
    try:
        cursor.execute(SQL)
    except Exception:
        SQL='create table '+'d'+today+'(submit_time char(10),host char(10),alarm_type char(10),status char(30),submit_person char(30))'
        cursor.execute(SQL)
        print 'create '+username+' finished'
        update_db(today,username,submit_time,host,type,status)