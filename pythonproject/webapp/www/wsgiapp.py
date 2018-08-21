from urls import web
import ConfigParser
from transwarp import db

config_file='E:\pythonproject\webapp\www\config.ini'
cfg=ConfigParser.ConfigParser()
cfg.read(config_file)

db.create_engine(**dict(cfg.items('db')))

if __name__=='__main__':
    with db.conn():
        web.run()