# -*- coding: utf-8 -*-
import time
from transwarp import db
from transwarp.db_orm import Model, StringField, BooleanField, FloatField, TextField,IntegerField,next_id

class User(Model):
    __table__ = 'User'
    id = IntegerField(primary_key=True)
    name = StringField(ddl='varchar(50)')
    email = StringField(ddl='varchar(50)')
    password = StringField(ddl='varchar(50)')
    admin = BooleanField(default=False)
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(default=time.time())

class Blog(Model):
    __table__ = 'Blog'
    id = IntegerField(primary_key=True)
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    name = StringField(ddl='varchar(50)')
    summary = StringField(ddl='varchar(200)')
    content = TextField()
    created_at = FloatField(default=time.time())

class Comment(Model):
    __table__ = 'Comment'
    id = IntegerField(primary_key=True)
    blog_id = StringField(ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    user_name = StringField(ddl='varchar(50)')
    user_image = StringField(ddl='varchar(500)')
    content = TextField()

if __name__ == '__main__':
    db.create_engine('root', 'cheng', 'awesome')
    with db.conn():
        db.update('drop table if exists User')
        db.update('drop table if exists Blog')
        db.update('drop table if exists Comment')
        db.update(User.__sql__)
        db.update(Blog.__sql__)
        db.update(Comment.__sql__)
        u = User(id=0,name='cwyj', email='794277368@qq.com', password='CHENG',admin=True)
        u2=User(name='cheng',email='18992868907@163.com',password='CHENG')
        b = Blog(user_id=0, user_name='cwyj', name='hello', summary='hello world!',content='i love python!!!')
        c=Comment()
        u.insert()
        #u2.insert()
        #b.insert()
