# _*_ coding: utf-8 _*_
__author__ = 'Angela'
__date__ = '2018年3月15日15:42:03'



import os
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis

# 实例化对象
app = Flask(__name__)

# 数据库连接配置  （多个数据库连接）
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@192.168.4.9:3306/subview'
app.config['SQLALCHEMY_BINDS'] = {
    'best':'mysql+pymysql://huian:As4a1LlRSqQFR23ZIXqYrie06Qsn1871@192.168.4.210:21409/cdr_report'
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'zwS4zlWA5ZO0Zn0n'
app.config["SQLALCHEMY_ECHO"] = True


#Redis
app.config["REDIS_URL"] = "redis://127.0.0.1:6379/0"

# 开启调试模式
app.debug = True

# 实例化对象
db = SQLAlchemy(app)
redis = FlaskRedis(app)

# 导入蓝图模块 # 不要在生成db之前导入注册蓝图。
from app.home import home as home_blueprint

# 注册蓝图
app.register_blueprint(home_blueprint)



# 404 错误页面
@app.errorhandler(404)
def page_not_found(error):
    return render_template("home/404.html")  # 搜索页面
