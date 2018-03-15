# _*_ coding: utf-8 _*_
__author__ = 'Angela'
__date__ = '2018年3月15日15:39:44'


from app import app
from flask_script import Manager
manage = Manager(app)

if __name__ == "__main__":
    manage.run()
