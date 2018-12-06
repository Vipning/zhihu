from application import app,manager
from flask_script import Server
import www
#自定义命令
manager.add_command('runserver',Server(host='127.0.0.1',port=app.config['SERVER_PORT'],use_debugger = True ,use_reloader = True))

def main():
    manager.run()
if __name__ =='__main__':
    try:
        import sys
        sys.exit(main())
    except Exception as e:
        import traceback
        traceback.print_exc()

#flask-sqlacodegen mysql://root:ltn5090791@127.0.0.1/zhihu --tables member --outfile "common/models/member/Member.py"  --flask