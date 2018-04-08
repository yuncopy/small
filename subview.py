# _*_ coding: utf-8 _*_
__author__ = 'Angela'
__date__ = '2018年3月15日15:39:44'


from app import app,scheduler

class Config(object):
    JOBS = []
    SCHEDULER_API_ENABLED = True


# 启动定时任务
app.config.from_object(Config())  # 为实例化的flask引入配置
scheduler.init_app(app=app)
scheduler.start()

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=9008)
    #app.run(debug=True, host='127.0.0.1', port=9008,use_reloader=False)
