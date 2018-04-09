# _*_ coding: utf-8 _*_
__author__ = 'Angela'
__date__ = '2018年3月15日15:42:03'



import os
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from flask_elasticsearch import FlaskElasticsearch
from flask_apscheduler import APScheduler


# 实例化对象
app = Flask(__name__)



# 数据库连接配置  （多个数据库连接）
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sub_view:sMeqqakk75gubuGccMBF@10.30.72.51:21406/sub_view'
app.config['SQLALCHEMY_BINDS'] = {
    'best':'mysql+pymysql://cdr:ZUi6vwX529BfGM6ffGkBOYNnMLBUmThX@47.90.124.253:21406/cdr_report',
    'charge':'mysql+pymysql://blueGuest:r9ue9dk#kmYT6Ni3QE&D@203.151.92.138:21406/charge'
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'zwS4zlWA5ZO0Zn0n'
app.config["SQLALCHEMY_ECHO"] = True
# 使用绝对路径  ()
app.config["BLUE_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/bluecoins/")

#Redis
app.config["REDIS_URL"] = "redis://127.0.0.1:6379/0"
app.config["ELASTICSEARCH_HOST"] = "47.52.0.90:9200"



# 开启调试模式
app.debug = False
app.use_reloader=False


# 实例化对象
db = SQLAlchemy(app)
redis = FlaskRedis(app)
es = FlaskElasticsearch(app)
scheduler = APScheduler()


# 导入蓝图模块 # 不要在生成db之前导入注册蓝图。
from app.home import home as home_blueprint

# 注册蓝图
app.register_blueprint(home_blueprint)



# 404 错误页面
@app.errorhandler(404)
def page_not_found(error):
    return render_template("home/404.html")  # 搜索页面

# 权限页面
@app.errorhandler(403)
def page_access_found(error):
    return render_template("home/403.html")  # 搜索页面
