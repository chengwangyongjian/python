from flask import Flask,request,render_template,make_response
import models,json,time,hashlib
from models import User,Blog,Comment

web=Flask(__name__)
user=None

@web.before_request
def auth_cookie():
    global user
    try:
        cookie = request.cookies.get(user.name)
        l=cookie.split('-')
        if len(l)!=3:
            user=None
        id,expire,md5=l
        if int(expire)<time.time():
            user=None
        u=User.get(id)
        if u is None:
            user=None
        if md5!=hashlib.md5('%s-%s-%s'%(user.id,user.password,expire)).hexdigest():
            user=None
    except:
        user=None

@web.route('/',methods=['GET'])
def index():
    global user
    blogs=Blog.find_all()
    return render_template('blogs.html',blogs=blogs,user=user)

@web.route('/api/<table>')
def api_get(table):
    try:
        data=models.__dict__[table].find_all()
    except Exception:
        return 'sth wrong'
    return json.dumps(data)

@web.route('/register',methods=['GET','POST'])
def register_user():
    if request.method=='GET':
        return render_template('register.html')
    else:
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        print password
        u=User.find_where('where email=?',email)
        if u:
            raise Exception("this email has been binding!!")
        user=User(name=name,password=password,email=email)
        user.insert()
        return signin()

def make_cookie(user):
    max_age=10
    expire=str(int(time.time())+max_age)
    return '-'.join([str(user.id),expire,hashlib.md5('%s-%s-%s'%(user.id,user.password,expire)).hexdigest()])

@web.route('/signin',methods=['GET','POST'])
def signin():
    if request.method=='GET':
        return render_template('signin.html')
    else:
        email=request.form['email']
        password=request.form['password']
        u=User.find_where('where email=?',email)
        print password,u[0].password
        if not u or password!=u[0].password:
            raise Exception("signin failed!!")
        global user
        user = u[0]
        blogs = Blog.find_all()
        resp=make_response(render_template('blogs.html'))
        #resp=make_response('<h1>hello world! </h1>')
        resp.set_cookie(user.name,make_cookie(user))
        return resp

@web.route('/signout')
def signout():
    global user
    user=None
    return index()

if __name__=='__main__':
    web.run(host='0.0.0.0', port=5000)