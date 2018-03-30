# _*_ coding: utf-8 _*_
__author__ = 'Angela'
__date__ = '2018年3月15日15:42:03'

from flask_apscheduler import APScheduler
from datetime import datetime,timedelta
from app import db,es
from app.models import Cdr_file,Cdr_file_hour,Backup_log
from sqlalchemy import func


class Config(object):  # 创建配置，用类
    JOBS = [  # 任务列表
        {
            'id': 'job_es_hour',
            'func': 'app.home.jobs:job_es_hour',
            'args': (3, 4),
            'trigger': 'cron',
            'second':'1',
            'minute':'30',   # */5   每5分钟
            'hour':'0-23'
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
    ]
    SCHEDULER_API_ENABLED = True


def jobs(app):
    app.config.from_object(Config())  # 为实例化的flask引入配置
    scheduler = APScheduler()  # 实例化APScheduler
    scheduler.init_app(app)  # 把任务列表放进flask
    scheduler.start()  # 启动任务列表






# 每个小时缓存数据到数据，直接从备份数据临时表获取一个小时数据
def job_es_hour(a, b):
    dt = datetime.now()
    end_time =dt.strftime('%Y-%m-%d %H:%M:%S')

    print('start:'+end_time)


    # 程序执行时间  （前2小时时间）
    hour_time_before = datetime.now() + timedelta(hours=-2)
    hour_time_str = hour_time_before.strftime("%Y-%m-%d %H")  # 获取当前小时


    start_time_hour = hour_time_str+':00:00'
    end_time_hour = hour_time_str + ':59:59'


    filters = {
        Cdr_file.status == 200,
        Cdr_file.operator_id != 9,
        Cdr_file.price > 0,
        Cdr_file.create_time >= start_time_hour,
        Cdr_file.create_time <= end_time_hour
    }

    try:

        # 先删除数据
        hour_time_str_del = hour_time_before.strftime("%Y-%m-%d-%H")  # 获取当前小时
        print(hour_time_str_del)
        Cdr_file_hour.query.filter(Cdr_file_hour.hour_time == hour_time_str_del).delete()
        db.session.commit()

        #查询数据
        data = Cdr_file.query.with_entities(
            Cdr_file.producer_id,
            Cdr_file.actiontype,
            Cdr_file.currency,
            func.DATE_FORMAT(Cdr_file.create_time, '%Y-%m-%d-%H').label('hour_time'),
            func.sum(Cdr_file.price).label('amount'),
            func.count(1).label('numbers')
        ).filter(*filters).group_by(
            func.DATE_FORMAT(Cdr_file.create_time, '%Y-%m-%d-%H'),
            Cdr_file.producer_id,
            Cdr_file.actiontype,
            Cdr_file.currency
        ).order_by(
            Cdr_file.create_time.desc()
        ).all()

        # 添加数据
        list_hour_data = []
        for v in data:
            hour_data = Cdr_file_hour(
                producer_id=v.producer_id,
                actiontype=v.actiontype,
                currency=v.currency,
                hour_time=v.hour_time,
                amount=v.amount,
                numbers=v.numbers
            )
            list_hour_data.append(hour_data)

        # 批量添加数据
        db.session.add_all(list_hour_data)
        db.session.commit()

        dtt = datetime.now()
        end_time_d = dtt.strftime('%Y-%m-%d %H:%M:%S')


        # 添加备份日志
        backup_log =Backup_log(
            backup_time=end_time,
            func_name='app.home.jobs:job_es_hour',
            used_time=end_time +' ~ '+end_time_d,
            cdr_file_max_time=start_time_hour + ' ~ '+ end_time_hour
        )

        db.session.add(backup_log)
        db.session.commit()

    except:
        db.session.rollback()

    print('end:' + end_time_d)




# 删除昨天数据

def job_del_hour(a,b):

    dt = datetime.now()
    start_time = dt.strftime('%Y-%m-%d %H:%M:%S')
    print('start:' + start_time)
    try:
        # 先删除数据
        days_time_before = dt + timedelta(days=-2)
        del_time_str = days_time_before.strftime("%Y-%m-%d")  # 获取当前小时

        filters={
            Cdr_file_hour.create_time <= del_time_str+' 23:59:59',
            Cdr_file_hour.create_time >= del_time_str + ' 00:00:00',
        }
        Cdr_file_hour.query.filter(*filters).delete()
        db.session.commit()

        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 添加备份日志
        backup_log = Backup_log(
            backup_time=end_time,
            func_name='app.home.jobs:job_del_hour',
            used_time=start_time + ' ~ ' + end_time,
            cdr_file_max_time=days_time_before + ' ~ ' + days_time_before
        )
        db.session.add(backup_log)
        db.session.commit()

    except:
        db.session.rollback()

    print('end:' + end_time)