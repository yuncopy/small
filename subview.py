# _*_ coding: utf-8 _*_
__author__ = 'Angela'
__date__ = '2018年3月15日15:39:44'


from app import app,scheduler


class Config(object):
    """
    定时任务配置
    """
    JOBS = [
        {
            'id': 'job_es_hour',
            'func': 'app.home.jobs:job_es_hour',
            'args': (3, 4),
            'trigger': 'cron',
            'second': '1',
            'minute': '30',  # */5   每5分钟
            'hour': '0-23'
        },
        {
            'id': 'job_del_hour',
            'func': 'app.home.jobs:job_del_hour',
            'args': (1, 2),
            'trigger': 'cron',
            'second': '1',
            'minute': '1',
            'hour': '2'
        }
        #{'id': 'job_task1','func': 'app.home.jobs:task1','args': (1, 2),'trigger': 'interval','seconds': 10}
    ]
    SCHEDULER_API_ENABLED = True


# 启动定时任务
app.config.from_object(Config())  # 为实例化的flask引入配置
scheduler.init_app(app=app)
scheduler.start()

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=9008)
    #app.run(debug=True, host='127.0.0.1', port=9008,use_reloader=False)
