import MySQLdb

db=MySQLdb.connect('192.168.37.129','root','cheng','notice')
cursor=db.cursor()
sql='select * from notice_table where alarm_type='
def get_down():
    cursor.execute(sql+'"down"')
    return cursor.fetchall()
def get_disk():
    cursor.execute(sql + '"disk"')
    return cursor.fetchall()