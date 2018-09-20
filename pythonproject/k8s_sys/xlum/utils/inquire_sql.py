#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/8/20

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, INTEGER, String
from sqlalchemy.orm import sessionmaker

sql_user = 'root'
sql_pwd = 'k8s394032his'
server_ip = 'twin13a029.sandai.net'
sql_database = 'ccuser'
engine = create_engine("mysql+pymysql://%s:%s@%s/%s?charset=utf8" % (sql_user, sql_pwd, server_ip, sql_database))
Base = declarative_base()   # 生成orm基类


class User(Base):
    __tablename__ = 't_number_info'   # 表名
    id = Column(INTEGER, primary_key=True)
    f_account = Column(String(255))
    f_password = Column(String(255))
    f_name = Column(String(255))


#Base.metadata.create_all(engine)   # 创建表结构
Session_class = sessionmaker(bind=engine)   # 创建与数据库的会话session class，即这里返回的是一个class，不是实例
Session = Session_class()   # 生成session实例

#user_obj = User(f_account='test', f_password='62ea587a4302161a205c3a20e04c888b', f_name='大水牛')
#Session.add(user_obj)
#Session.commit()


def query_user(username):
    '''查找op用户并返回'''
    user_obj = Session.query(User).filter(User.f_account == username).first()
    return user_obj
