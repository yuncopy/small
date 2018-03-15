# _*_ coding: utf-8 _*_
__author__ = 'Angela'
__date__ = '2018年3月15日15:39:44'



from . import home
from app.home.forms import LoginForm
from flask import render_template, url_for, redirect, flash, session, request, Response
from app.models import Admin,Adminlog
from werkzeug.security import generate_password_hash
from app import db, app,redis
from functools import wraps


#================公共函数================

# 检测是否登录服务
def is_login_req(f):
    """
    登录装饰器
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("home.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function
#==============公共函数==========end=====



# 后台汇总
@home.route("/", methods=["GET"])
@is_login_req
def index():


    return render_template("home/index.html")


#按天流水
@home.route("/day/", methods=["GET"])
@is_login_req
def day():

    return render_template("home/day.html")





#按天流水
@home.route("/charge/", methods=["GET"])
@is_login_req
def charge():

    return render_template("home/charge.html")



#按天流水
@home.route("/sub/", methods=["GET"])
@is_login_req
def sub():

    return render_template("home/sub.html")





# 后台管理员登录界面
@home.route("/login/", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=data["name"]).first()
        if admin:
            if not admin.check_pwd(data["pwd"]):
                flash("密码错误！", "err")
                return redirect(url_for("home.login"))
        else:
            flash("账户不存在！", "err")
            return redirect(url_for("home.login"))

        # 异常处理
        try:
            adminlog = Adminlog(
                admin_id=admin.id,
                ip=request.remote_addr
            )
            db.session.add(adminlog)
            db.session.commit()

            # 保存会话
            session["admin"] = admin.name
            session["admin_id"] = admin.id
            return redirect(url_for("home.index"))  # 跳转
        except:
            db.session.rollback()

    return render_template("home/login.html", form=form)  # 登录页面


# 退出
@home.route('/logout/')
def logout():
    """
    退出登录
    """
    # 重定向到home模块下的登录。
    session.pop("admin", None)
    session.pop("admin_id", None)
    flash('已安全退出。','ok')
    return redirect(url_for('home.login'))  # 退出跳转到登录界面
