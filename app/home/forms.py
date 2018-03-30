# _*_ coding: utf-8 _*_
__author__ = 'Angela'
__date__ = '2018年3月15日15:39:44'

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField,SelectField,SelectMultipleField,widgets
from wtforms.validators import DataRequired, Email, Regexp, EqualTo, ValidationError
from app.models import Role,Auth,Admin


# 登录后台界面
class LoginForm(FlaskForm):
    name = StringField(
        label="账号",
        validators=[
            DataRequired("账号不能为空")
        ],
        description="账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号",
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("密码不能为空")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码",
        }
    )
    submit = SubmitField(
        '登录',
        render_kw={
            "class": "btn btn-default submit btn-sm",
        }
    )



# 管理员管理
class AdminForm(FlaskForm):
    name = StringField(
        label="管理员名称",
        validators=[
            DataRequired("管理员名称不能为空")
        ],
        description="管理员名称",
        render_kw={
            "class": "form-control col-md-7 col-xs-12",
            "placeholder": "请输入管理员名称",
        }
    )
    pwd = PasswordField(
        label="管理员密码",
        validators=[
            DataRequired("管理员密码不能为空")
        ],
        description="管理员密码",
        render_kw={
            "class": "form-control col-md-7 col-xs-12",
            "placeholder": "请输入管理员密码",
        }
    )
    repwd = PasswordField(
        label="管理员确认密码",
        validators=[
            DataRequired("管理员重复密码不能为空"),
            EqualTo('pwd', message="两次密码不一致")
        ],
        description="管理员确认密码",
        render_kw={
            "class": "form-control col-md-7 col-xs-12",
            "placeholder": "请输入管理员确认密码",
        }
    )
    role_id = SelectField(
        label="所属角色",
        coerce=int,
        choices=[(v.id, v.name) for v in Role.query.all()],
        render_kw={
            "class": "form-control col-md-7 col-xs-12",
        }
    )
    submit = SubmitField(
        '确定',
        render_kw={
            "class": "btn btn-primary",
        }
    )



"""
权限表单
"""
class AuthForm(FlaskForm):
    name = StringField(
        label="权限名称",
        validators=[
            DataRequired("权限名称不能为空")
        ],
        description="权限名称",
        render_kw={
            "class": "form-control col-md-7 col-xs-12",
            "placeholder": "请输入权限名称"
        }
    )
    url = StringField(
        label="权限地址",
        validators=[
            DataRequired("权限地址不能为空")
        ],
        description="权限地址",
        render_kw={
            "class": "form-control col-md-7 col-xs-12",
            "placeholder": "请输入权限地址"
        }
    )
    submit = SubmitField(
        '确定',
        render_kw={
            "class": "btn btn-primary",
        }
    )



# 角色管理
class RoleForm(FlaskForm):
    name = StringField(
        label="角色名称",
        validators=[
            DataRequired("角色名称不能为空！")
        ],
        description="角色名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入角色名称！"
        }
    )
    # 多选框
    """
    auths = SelectMultipleField(
        label="权限列表",
        validators=[
            DataRequired("权限列表不能为空！")
        ],
        # 动态数据填充选择栏：列表生成器,
        # choices 参数来传入可选择项，每个项是一个(值, 显示名称)对，
        # 同时它们也有一个参数coerce 参数来强制转换选择项"值"的类型，比如 coerce=int。
        coerce=int,
        choices=[(v.id, v.name) for v in Auth.query.all()],
        description="权限列表",
        render_kw={
            "class": "form-control",
        }
        #传入一个字典（render_kw），把需要添加到字段的属性以键值对的形式
    )
    """
    auths =SelectMultipleField(
        label="权限列表",
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(html_tag='ol',prefix_label=True),
        #widget=widgets.TableWidget(),
        validators=[
            DataRequired("权限列表不能为空！")
        ],
        coerce=int,
        choices=[(v.id, v.name) for v in Auth.query.all()],
        description="权限列表",
        render_kw={
           #"class": "form-control",
        }
    )
    submit = SubmitField(
        '确定',
        render_kw={
            "class": "btn btn-primary",
        }
    )

# 修改密码
class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label="旧密码",
        validators=[
            DataRequired("旧密码不能为空")
        ],
        description="旧密码",
        render_kw={
            "class": "form-control col-md-7 col-xs-12",
            "placeholder": "请输入旧密码",
        }
    )
    new_pwd = PasswordField(
        label="新密码",
        validators=[
            DataRequired("新密码不能为空")
        ],
        description="新密码",
        render_kw={
            "class": "form-control col-md-7 col-xs-12",
            "placeholder": "请输入新密码",
        }
    )
    submit = SubmitField(
        '确定',
        render_kw={
            "class": "btn btn-primary",
        }
    )

    # 验证密码是否正确
    def validate_old_pwd(self, field):
        from flask import session
        pwd = field.data
        name = session["admin"]
        admin = Admin.query.filter_by(
            name=name
        ).first()
        if not admin.check_pwd(pwd):
            raise ValidationError("旧密码错误！")


class JobForm(FlaskForm):
    """
    执行操作
    """
    action = SelectField(
        label="操作记录",
        validators=[
            DataRequired("选择操作记录不能为空！")
        ],
        coerce=str,
        choices=[('', '选择操作类型'),('1', '删除'),('2', '补充')],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入角色名称！"
        }
    )
    field = SelectField(
        label="操作记录",
        validators=[
            DataRequired("选择操作字段不能为空！")
        ],
        coerce=str,
        choices=[('', '选择操作字段'), ('hour_time', '记录小时'), ('create_time', '记录时间')],
        render_kw={
            "class": "form-control",
            "placeholder": "选择操作字段！"
        }
    )
    where = StringField(
        label="条件",
        validators=[
            DataRequired("填写条件不能为空！")
        ],
        description="填写条件",
        render_kw={
            "class": "form-control",
            "placeholder": "请严格按照格式填写！"
        }
    )
    submit = SubmitField(
        '执行',
        render_kw={
            "class": "btn btn-round btn-danger",
        }
    )



class BlueCoinForm(FlaskForm):
        """
        BlueCoins
        """
        amount = StringField(
            label="BlueCoin",
            validators=[
                DataRequired("BlueCoin真实面值不能为空！")
            ],
            description="BlueCoin",
            render_kw={
                "class": "form-control",
                "placeholder": "请输入BlueCoin真实面值"
            }
        )
        numbers = StringField(
            label="BlueCoin 数量",
            validators=[
                DataRequired("BlueCoin数量不能为空！")
            ],
            description="BlueCoin",
            render_kw={
                "class": "form-control",
                "placeholder": "请输入BlueCoin数量"
            }
        )
        submit = SubmitField(
            '执行',
            render_kw={
                "class": "btn btn-round btn-danger",
            }
        )




