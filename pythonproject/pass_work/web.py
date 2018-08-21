from flask import Flask,request,render_template
import time,check_user,updatedb,get_notice

web=Flask(__name__)
d={}
login_time=0
username=''

@web.route('/',methods=['GET'])
def login_form():
    return render_template('login.html')

@web.route('/login',methods=['POST'])
def login():
    global username
    username=request.form['username']
    password=request.form['password']
    if check_user.sql(username,password):
        global login_time,d
        d={}
        login_time=time.asctime()
        return render_template('pass_work.html',username=username,d=d,t=login_time)
    return render_template('login.html',message='bad username or password',username=username)

@web.route('/pass_work',methods=['POST'])
def passwork():
    host=request.form['host']
    type=request.form['alarm_type']
    status=request.form['deal']
    submit_time=time.strftime('%H:%M',time.localtime(time.time()))
    #today=time.strftime('%Y%m%d',time.localtime(time.time()))
    today='20171203'
    d[host]=type
    updatedb.update_db(today,username,submit_time,host,type,status)
    return render_template('pass_work.html',username=username,d=d,t=login_time)

if __name__ == "__main__":
    web.run()