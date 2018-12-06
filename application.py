from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
import os

#封装app变量和db变量
class Application(Flask):
    def __init__(self,import_name,root_path=None):
        super(Application,self).__init__(import_name,root_path = root_path,static_folder = None)
        self.config.from_pyfile('config/base_setting.py')  # 加载配置文件
        db.init_app(self)

db =SQLAlchemy()
app =Application(__name__,root_path = os.getcwd())
manager =Manager(app)

