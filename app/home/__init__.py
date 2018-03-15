# _*_ coding: utf-8 _*_
__author__ = 'Angela'
__date__ = '2018年3月15日15:39:23'

# 从flask中导入蓝图对象
from flask import Blueprint

#定义蓝图
home = Blueprint('home',__name__)

#导入视图模块
import app.home.views
