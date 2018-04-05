# _*_ coding: utf-8 _*_
__author__ = 'Angela'
__date__ = '2018年3月15日15:39:44'


from app import app
from app.home.jobs import jobs

if __name__ == "__main__":
    jobs(app)
    app.run(host='0.0.0.0', port=9008)
