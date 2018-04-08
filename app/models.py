# _*_ coding: utf-8 _*_
__author__ = 'Angela'
__date__ = '2018年3月15日15:42:03'

from datetime import datetime
from app import db


# 后台用户数据模型
class Admin(db.Model):
    __tablename__ = "admin"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 管理员账号
    pwd = db.Column(db.String(100))  # 管理员密码
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # 所属角色
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    adminlogs = db.relationship("Adminlog", backref='admin')  # 管理员登录日志外键关系关联
    actionlogs = db.relationship("Actionlog", backref='admin')  # 管理员操作日志外键关系关联

    def __repr__(self):
        return "<Admin %r>" % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 管理员登录日志
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 登录IP
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间
    update_time = db.Column(db.DateTime, index=True, default=datetime.now, onupdate=datetime.now)  # 修改时间

    def __repr__(self):
        return "<Adminlog %r>" % self.id


# 管理员操作日志
class Actionlog(db.Model):
    __tablename__ = "actionlog"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 操作IP
    reason = db.Column(db.String(600))  # 操作原因
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间
    update_time = db.Column(db.DateTime, index=True, default=datetime.now, onupdate=datetime.now)  # 修改时间

    def __repr__(self):
        return "<Oplog %r>" % self.id


# 权限
class Auth(db.Model):
    __tablename__ = "auth"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    url = db.Column(db.String(255), unique=True)  # 地址
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间
    update_time = db.Column(db.DateTime, index=True, default=datetime.now, onupdate=datetime.now)  # 修改时间
    name_url_idx = db.UniqueConstraint('name', 'url', name='name_url_idx')

    def __repr__(self):
        return "<Auth %r>" % self.name

    # 检测密码是否正确
    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 角色
class Role(db.Model):
    __tablename__ = "role"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    auths = db.Column(db.String(600))  # 角色权限列表
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间
    update_time = db.Column(db.DateTime, index=True, default=datetime.now, onupdate=datetime.now)  # 修改时间
    admins = db.relationship("Admin", backref='role')  # 管理员外键关系关联

    def __repr__(self):
        return "<Role %r>" % self.name




# 任务列表
class TaskList(db.Model):
    __tablename__ = "task_list"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(32), unique=True)  # 名称
    task = db.Column(db.String(16))  # 任务类型
    format = db.Column(db.String(180))  # 任务定时任务格式
    func = db.Column(db.String(32))  # 执行函数
    args = db.Column(db.String(18))  # 执行参数
    info = db.Column(db.String(255))  # 备注信息
    status = db.Column(db.Integer)   #状态
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间
    update_time = db.Column(db.DateTime, index=True, default=datetime.now, onupdate=datetime.now)  # 修改时间


    def __repr__(self):
        return "<task_list %r>" % self.name

# ===============BEST======数据库模型=======

# 查询月备表
class Tb_transaction_backup(db.Model):
    __bind_key__ = 'best'
    __tablename__ = "tb_transaction_backup"
    __abstract__ = True
    __table_args__ = {"useexisting": True}
    Id = db.Column(db.Integer, primary_key=True)  # 编号
    status = db.Column(db.String(8), nullable=True)
    price = db.Column(db.String(12), nullable=True)
    promotion_id = db.Column(db.String(8), nullable=True)
    product_id = db.Column(db.String(12), nullable=True)
    producer_id = db.Column(db.String(12),nullable=True,)
    operator_id = db.Column(db.String(4), nullable=True)
    actiontype = db.Column(db.String(5), nullable=True)
    shortcode = db.Column(db.String(50), nullable=True)
    numbers = db.Column(db.String(20), nullable=True)
    create_time = db.Column(db.String(10), nullable=True)
    operator_desc = db.Column(db.String(20), nullable=True)
    ccy = db.Column(db.String(20), nullable=True)
    telco_name = db.Column(db.String(50), nullable=True)
    idx_tel_act = db.UniqueConstraint('telco_name', 'actiontype', name='idx_telcoName_actiontype')



    def __repr__(self):
        return "<Tb_transaction_backup %r>" % self.Id


# 动态创建表名
class NewTbModel(object):
    """
    动态产生模型和表的对应关系模型
    eg:
    '''
    class TemplateModel(db.Model):
        __abstract__ = True
        id = db.Column(db.Integer(), autoincrement=True, primary_key=True)

    Test_2018 = NewDynamicModel(TemplateModel, 'tb_test_2017')
    print Test_2018.query.all()
    '''
    """
    _instance = dict()
    def __new__(cls, base_cls, tb_name):
        new_cls_name = "%s_To_%s" % (
            base_cls.__name__, '_'.join(map(lambda x:x.capitalize(),tb_name.split('_'))))

        if new_cls_name not in cls._instance:
            model_cls = type(new_cls_name, (base_cls,),
                             {'__tablename__': tb_name})
            cls._instance[new_cls_name] = model_cls

        return cls._instance[new_cls_name]


# CP 信息表
class Ref_producer(db.Model):
    __bind_key__ = 'best'
    __tablename__ = "ref_producer"
    __table_args__ = {"useexisting": True}
    producer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 编号
    producer_name = db.Column(db.String(50), nullable=True)
    callback = db.Column(db.String(150), nullable=True)
    md5Suf = db.Column(db.String(16), nullable=True)
    grade = db.Column(db.String(2), nullable=True)

    def __repr__(self):
        return "<Ref_producer %r>" % self.producer_id


# 产品 信息表
class Product_info(db.Model):
    __bind_key__ = 'best'
    __tablename__ = "product_info"
    __table_args__ = {"useexisting": True}
    product_id = db.Column(db.Integer, primary_key=True)  # 编号
    producer_id = db.Column(db.Integer)
    product_alias = db.Column(db.String(120), nullable=True)
    product_name = db.Column(db.String(32), nullable=True)
    product_lastupdatetime = db.Column(db.DateTime, nullable=False,default=datetime.now,onupdate=datetime.now)
    product_shortname = db.Column(db.String(12), nullable=True)
    daily_limit = db.Column(db.Integer, nullable=False,default=1500)
    monthly_limit = db.Column(db.Integer, nullable=False, default=9000)
    limitType = db.Column(db.SmallInteger, nullable=False,default=1)
    amountLimitType = db.Column(db.SmallInteger, nullable=False,default=2)
    product_desc = db.Column(db.String(12), nullable=True)
    product_category = db.Column(db.String(10), nullable=True)
    product_icon = db.Column(db.String(50), nullable=True)
    product_screenshot1 = db.Column(db.String(50), nullable=False,default='')
    product_screenshot2 = db.Column(db.String(50), nullable=False,default='')
    product_screenshot3 = db.Column(db.String(50), nullable=False,default='')
    product_screenshot4 = db.Column(db.String(50), nullable=False,default='')
    product_screenshot5 = db.Column(db.String(50), nullable=False,default='')
    product_downloadUrl = db.Column(db.String(120), nullable=False,default='')
    product_type = db.Column(db.Integer, nullable=True)
    product_pkgSize = db.Column(db.Integer, nullable=True)
    product_rating = db.Column(db.Float, nullable=True)
    product_downloadType = db.Column(db.Integer, nullable=True)
    product_status = db.Column(db.Integer, nullable=True)
    product_subscribeable = db.Column(db.Integer, nullable=True)
    product_rss = db.Column(db.Integer, nullable=True)
    product_createTime = db.Column(db.DateTime, nullable=True)
    notify_url = db.Column(db.String(150), nullable=True)
    sender = db.Column(db.String(50), nullable=True)
    product_applyTime = db.Column(db.DateTime, nullable=True)
    counts_limit = db.Column(db.Integer, nullable=True)
    money_limit = db.Column(db.Integer, nullable=True)
    chanel_type = db.Column(db.Integer, nullable=True)
    one_key_pay = db.Column(db.Integer, nullable=True)
    is_game = db.Column(db.Integer, nullable=True)
    th_daily_limit = db.Column(db.Integer, nullable=True)
    th_monthly_limit = db.Column(db.Integer, nullable=True)
    vn_daily_limit = db.Column(db.Integer, nullable=True)
    vn_monthly_limit = db.Column(db.Integer, nullable=True)
    id_daily_limit = db.Column(db.Integer, nullable=True)
    id_monthly_limit = db.Column(db.Integer, nullable=True)


    def __repr__(self):
        return "<Product_info %r>" % self.product_id



# CDR表
class Cdr_file(db.Model):
    __bind_key__ = 'best'
    __tablename__ = "cdr_file"
    __table_args__ = {"useexisting": True}
    Id = db.Column(db.String(25), primary_key=True, autoincrement=True)  # 编号
    status = db.Column(db.String(8), nullable=True)
    price = db.Column(db.String(12), nullable=True)
    promotion_id = db.Column(db.String(8), nullable=True)
    product_id = db.Column(db.String(12), nullable=True)
    producer_id = db.Column(db.String(12), nullable=True)
    operator_id = db.Column(db.String(4), nullable=True)
    actiontype = db.Column(db.String(5), nullable=True)
    shortcode = db.Column(db.String(40), nullable=True)
    msisdn = db.Column(db.String(20), nullable=True)
    create_time = db.Column(db.DateTime, nullable=True)
    innerid = db.Column(db.String(2), nullable=True)
    transactionid = db.Column(db.String(255), nullable=True)
    currency = db.Column(db.String(20), nullable=True)
    telco_name = db.Column(db.String(100), nullable=True)
    insert_time = db.Column(db.DateTime, nullable=True)
    serverid = db.Column(db.String(10), nullable=True)
    is_zip = db.Column(db.String(1), nullable=True)
    complain_flag = db.Column(db.SmallInteger, nullable=True)

    def __repr__(self):
        return "<Cdr_file %r>" % self.producer_id

# 角色
class Cdr_file_hour(db.Model):
    __tablename__ = "cdr_file_hour"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)  # 编号
    hour_time = db.Column(db.String(16), nullable=False)  # 名称
    amount = db.Column(db.String(32), nullable=False)  # 角色权限列表
    actiontype = db.Column(db.String(5), nullable=False)
    producer_id = db.Column(db.String(12), nullable=False)
    numbers = db.Column(db.String(12), nullable=False)
    currency = db.Column(db.String(5), nullable=False)
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间
    update_time = db.Column(db.DateTime, index=True, default=datetime.now, onupdate=datetime.now)  # 修改时间

    def __repr__(self):
        return "<Cdr_file_hour %r>" % self.id

# 备份日志表
class Backup_log(db.Model):
    __tablename__ = "backup_log"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)  # 编号
    backup_time = db.Column(db.String(18), nullable=False)  # 名称
    func_name = db.Column(db.String(32), nullable=False)  # 角色权限列表
    used_time = db.Column(db.String(200), nullable=False)
    cdr_file_max_time = db.Column(db.String(200), nullable=False)
    create_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 创建时间
    update_time = db.Column(db.DateTime, index=True, default=datetime.now, onupdate=datetime.now)  # 修改时间

    def __repr__(self):
        return "<Backup_log %r>" % self.id



# 备份日志表
class Bluecoins_log(db.Model):
    __tablename__ = "bluecoins_log"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)  # 编号
    data = db.Column(db.String(200), nullable=False)  # 名称
    url = db.Column(db.String(200), nullable=False)  # 角色权限列表
    name = db.Column(db.String(200), nullable=False)
    result = db.Column(db.String(200), nullable=False)
    filename = db.Column(db.String(180), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 修改时间

    def __repr__(self):
        return "<Bluecoins_log %r>" % self.id


# 订阅记录
class Subs_subscription(db.Model):
    __bind_key__ = 'charge'
    __tablename__ = "subs_subscription"
    __table_args__ = {"useexisting": True}
    subs_id = db.Column(db.String(32), primary_key=True)  # 编号
    svid = db.Column(db.String(7), nullable=True)
    msisdn = db.Column(db.String(12), nullable=True)
    state = db.Column(db.String(4), nullable=True)
    subscriped_time = db.Column(db.DateTime, nullable=True)
    lastupdate_time = db.Column(db.DateTime, nullable=True)
    next_recurring_time = db.Column(db.DateTime, nullable=True)
    Product_id = db.Column(db.String(20), nullable=True)
    operatorId = db.Column(db.Integer, nullable=True)
    True_mesasgeid = db.Column(db.String(64), nullable=True)
    telco_name = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return "<Subs_subscription %r>" % self.subs_id

''' 
#创建数据表
if __name__ == "__main__":
    db.create_all()


# 插入管理员角色
role = Role(
     name="超级管理员",
     auths=""
)
db.session.add(role)
db.session.commit()

# 插入管理员
from werkzeug.security import generate_password_hash
admin = Admin(
     name="admin",
     pwd=generate_password_hash("qwer@123"),
     role_id=1
 )
db.session.add(admin)
db.session.commit()
'''
