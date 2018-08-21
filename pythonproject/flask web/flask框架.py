from flask import Flask,request,render_template,make_response,url_for

web=Flask(__name__)

@web.route('/',methods=['GET'])
def home():
    return render_template('home.html')

@web.route('/login',methods=['GET'])
def login_form():
    return render_template('login_form.html')

@web.route('/login',methods=['POST'])
def login():
    username=request.form['username']
    password=request.form['password']
    if request.form['username']=='root' and request.form['password']=='cheng':
        resp=make_response(render_template('login.html',usernmae=username))
        resp.set_cookie('username','ccc')
        return resp
    return render_template('login_form.html',message='bad username or password',username=username)

@web.before_request
def get_coo():
    cookie=request.cookies.get('username')
    if cookie=='ccc':
        print 'b'
        return home()
    else:
        print 'a'

if __name__ == "__main__":
    web.run()