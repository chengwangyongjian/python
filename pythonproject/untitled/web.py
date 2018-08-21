from flask import Flask,request,render_template
import time,check_user,get_config

web=Flask(__name__)

@web.route('/',methods=['GET'])
def login_form():
    return render_template('login.html')

@web.route('/login',methods=['POST'])
def login():
    username=request.form['username']
    password=request.form['password']
    if check_user.check(username,password):
        login_time = time.asctime()
        return render_template('ch_ng.html',d=get_config.get(),t=login_time)
    return render_template('login.html', message='bad username or password', username=username)

@web.route('/ch_conf',methods=['POST'])
def change():



if __name__ == "__main__":
    web.run()