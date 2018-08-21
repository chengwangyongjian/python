import db,time

def next_id(table):
    sql='select max(id) from %s'%table
    r=db.select(sql)
    return r[0]['max(id)']+1 if r[0]['max(id)']!=None else 0

class pk_Error(Exception):
    pass

class Field(object):
    count=0
    def __init__(self,**args):
        self.primary_key = args.get('primary_key', False)
        self.nullable=args.get('nullable',False)
        Field.count+=1
        self.count=Field.count

class StringField(Field):
    def __init__(self,**args):
        super(StringField, self).__init__(**args)
        self.default = args.get('default', '')
        self.ty=args.get('ty','varchar(255)')

class IntegerField(Field):
    def __init__(self,**args):
        super(IntegerField, self).__init__(**args)
        self.default = args.get('default', 0)
        self.ty = args.get('ty', 'bigint')

class FloatField(Field):
    def __init__(self,**args):
        super(FloatField, self).__init__(**args)
        self.default = args.get('default', 0.0)
        self.ty = args.get('ty', 'real')

class BooleanField(Field):
    def __init__(self, **args):
        super(BooleanField, self).__init__(**args)
        self.default = args.get('default', False)
        self.ty = args.get('ty', 'bool')

class TextField(Field):
    def __init__(self, **args):
        super(TextField, self).__init__(**args)
        self.default = args.get('default', '')
        self.ty = args.get('ty', 'text')

def create_sql(table,mapping):
    l = sorted([(k, v) for k, v in mapping.iteritems() if k != 'primary key'],key=lambda x: x[1].count)
    l=[v.nullable and '%s %s' % (k, v.ty) or '%s %s not null' % (k, v.ty) for k,v in l]
    l.append('primary key(%s)'%mapping['primary key'])
    sql = 'create table %s (%s)' % (table, ',\n'.join(l))
    return sql

class make_class(type):
    def __new__(cls, class_name,parent_class,attrs):
        if class_name=='Model':
            return type.__new__(cls, class_name,parent_class,attrs)
        attrs['__table__']=class_name
        __mapping__={}
        primary_key=''
        for k,v in attrs.iteritems():
            if isinstance(v,Field):
                __mapping__[k]=v
                if v.primary_key:
                    if primary_key:
                        raise pk_Error('primary key has defined!')
                    primary_key=k
        if not primary_key:
            raise pk_Error('primary key not define!')
        for key in __mapping__.iterkeys():
            attrs.pop(key)
        __mapping__['primary key']=primary_key
        attrs['primary_key']=primary_key
        attrs['__mapping__']=__mapping__
        attrs['__sql__']=create_sql(attrs['__table__'],attrs['__mapping__'])
        return type.__new__(cls, class_name,parent_class,attrs)

class Model(dict):
    __metaclass__ = make_class
    def __init__(self,**kwargs):
        super(Model, self).__init__(**kwargs)
    def __getattr__(self, item):
        return self[item]
    def __setattr__(self, key, value):
        self[key]=value
    def insert(self):
        for k, v in self.__mapping__.iteritems():
            if not hasattr(self,k) and k!= 'primary key':
                if k=='id':
                    setattr(self,k,next_id(self.__table__))
                else:
                    setattr(self,k,v.default)
        db.insert('%s' % self.__table__, **self)
    def update(self):
        L=[k+'='+`getattr(self,k)` for k in self.__mapping__.keys() if k != 'primary key']
        sql='update %s set %s where %s=?'%(self.__table__,','.join(L),self.primary_key)
        db.update(sql,getattr(self,self.primary_key))
    def delete(self):
        sql='delete from %s where %s=?'%(self.__table__,self.primary_key)
        db.update(sql,getattr(self,self.primary_key))
    @classmethod
    def get(cls,pk):
        sql='select * from %s where %s=?'%(cls.__table__,cls.primary_key)
        d=db.select(sql,pk)[0]
        return cls(**d) if d else None
    @classmethod
    def find_all(cls):
        sql='select * from %s'%cls.__table__
        return [cls(**i) if i else None for i in db.select(sql)]
    @classmethod
    def find_where(cls,gen_sql,*args):
        sql='select * from %s %s'%(cls.__table__,gen_sql)
        return [cls(**i) if i else None for i in db.select(sql,*args)]

if __name__=='__main__':
    class User(Model):
        id = IntegerField(primary_key=True)
        name = StringField(nullable=True)
        email = StringField()
        passwd = StringField(default='cheng')
        last_modified = FloatField(default=time.time())
    u1 = User(id=10190, name='Michael', email='794277368@qq.com',passwd='CHENG')
    u2=User(id=10191,name='cwang',email='cwyj@xunlei.com')
    db.create_engine('root', 'cheng', 'awesome')
    with db.conn():
        '''db.update('drop table if exists User')
        db.update(u1.__sql__)
        u1.insert()
        u2.insert()
        u=User.get(10190)
        u1.name='cwyj'
        u1.update()
        u2.delete()'''




