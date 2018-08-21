import MySQLdb

def sql(username,password):
    username2="'"+username+"'"
    db=MySQLdb.connect('192.168.37.129','root','cheng','users')
    cursor=db.cursor()
    SQL='select * from user_list where username='+username2
    cursor.execute(SQL)
    if (username,password) in cursor.fetchall():
        return True
    else:
        return False
