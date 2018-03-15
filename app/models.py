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
    update_time = db.Column(db.DateTime, index=True, default=datetime.now,onupdate = datetime.now)  # 修改时间

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
    def check_pwd(self,pwd):
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



#===============BEST======数据库模型=======

# 查询月备表
class Tb_transaction_backup(db.Model):
    __bind_key__ = 'best'
    __tablename__ = "tb_transaction_backup"
    __table_args__ = {"useexisting": True}
    Id = db.Column(db.Integer, primary_key=True)  # 编号
    status = db.Column(db.String(8), nullable=True)
    price = db.Column(db.String(12), nullable=True)
    promotion_id = db.Column(db.String(8), nullable=True)
    product_id = db.Column(db.String(12), nullable=True)
    producer_id = db.Column(db.String(12), nullable=True)
    operator_id = db.Column(db.String(4), nullable=True)
    actiontype = db.Column(db.String(5), nullable=True)
    shortcode = db.Column(db.String(50), nullable=True)
    numbers = db.Column(db.String(20), nullable=True)
    create_time = db.Column(db.String(10), nullable=True)
    operator_desc = db.Column(db.String(20), nullable=True)
    ccy = db.Column(db.String(20), nullable=True)
    telco_name = db.Column(db.String(50), nullable=True)
    idx_tel_act= db.UniqueConstraint('telco_name', 'actiontype', name='idx_telcoName_actiontype')

    def __repr__(self):
        return "<Tb_transaction_backup %r>" % self.name


# CP 信息表
class Ref_producer(db.Model):
    __bind_key__ = 'best'
    __tablename__ = "ref_producer_backup"
    __table_args__ = {"useexisting": True}
    producer_id = db.Column(db.Integer, primary_key=True,autoincrement = True)  # 编号
    producer_name = db.Column(db.String(50), nullable=True)
    callback = db.Column(db.String(150), nullable=True)
    md5Suf = db.Column(db.String(16), nullable=True)
    grade = db.Column(db.String(2), nullable=True)
    def __repr__(self):
        return "<ref_roducer %r>" % self.producer_id



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