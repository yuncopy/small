# _*_ coding: utf-8 _*_
__author__ = 'Angela'
__date__ = '2018年3月15日15:39:44'


from app import app,scheduler
from flask_script import Manager

class Config(object):
    JOBS = []
    SCHEDULER_API_ENABLED = True

manage = Manager(app)
app.config.from_object(Config())  # 为实例化的flask引入配置
if __name__ == "__main__":
    scheduler.init_app(app=app)
    scheduler.start()
    manage.run()
