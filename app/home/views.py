# -*- coding: UTF-8 -*-
__author__ = 'Angela'
__date__ = '2018年3月15日15:39:44'


from . import home
from app.home.forms import LoginForm, AdminForm, AuthForm, RoleForm, PwdForm,JobForm,BlueCoinForm,TaskForm
from flask import render_template, url_for, redirect, flash, session, request, Response, abort,jsonify
from app.models import Admin, Auth, Role, Adminlog, Ref_producer, Tb_transaction_backup, NewTbModel, Subs_subscription,Product_info, Cdr_file_hour,Backup_log,Cdr_file,Bluecoins_log,TaskList
from sqlalchemy import func
from werkzeug.security import generate_password_hash
from app import db, app, redis, es,scheduler
from datetime import timedelta, datetime
from functools import wraps
import json
import time
from urllib.parse import urlencode
import urllib.request
from hashlib import md5
from random import Random
import os
from sqlalchemy.ext.serializer import loads, dumps
# ================公共函数================


def is_login_req(f):
    """
    登录装饰器
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("home.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function



def random_str(randomlength=8):
    """
    随机生成字符
    :param randomlength:
    :return:
    """
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str


def PHPmd5(s, raw_output=False):
    """
    PHP MD5
    :param s:
    :param raw_output:
    :return:
    """
    res = md5(s.encode("utf-8"))
    if raw_output:
        return res.digest()
    return res.hexdigest()


def home_auth(f):
    """
    权限控制装饰器
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):


        admin = Admin.query.join(
            Role
        ).filter(
            Role.id == Admin.role_id,
            Admin.id == session["admin_id"]
        ).first()


        auths = admin.role.auths  # 字符串
        auths = list(map(lambda v: int(v), auths.split(",")))  # 转化为列表

        # 缓存
        if 'auth' in session:
            auth_list = loads(session['auth'])
        else:
            auth_list = Auth.query.all()
            session['auth'] = dumps(auth_list)

        # urls = [v.url for v in auth_list for val in auths if val == v.id]
        urls = []
        for v in auth_list:
            if v.id in auths:
                urls.append(v.url)
        rule = request.url_rule
        # print(urls)
        # print(rule)
        """"""
        if str(rule) not in urls:
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


# 当前用户币种

def current_currency():
    USER_CCY = 'USD'
    return USER_CCY


# 定义场景类型
def action_type(key):
    action_all = dict(
        locan=[15],
        receive=[21],
        game=[1, 2, 4, 8, 11, 13, 14, 20],
        sub=[5]
    )
    if key in action_all:
        action = action_all[key]
    else:
        action = action_all
    return action


"""
功能：币种转化
@:param int original 原始金额
@:param str ccy 原始币种
@:return int amount
"""


def rate_currency(original, ccy):
    rate = dict(
        THB=32,
        VND=22700,
        IDR=13400,
        CNY=7,
        USD=1,
        MYR=4
    )
    if ccy == 'MYR' or ccy == 'THB':
        original = original / 100
    cy = current_currency()  # 目标币种
    amount = original / (rate[ccy]) * (rate[cy])  # 先转为美金再转化为目标币种
    return amount


# ==============公共函数==========end=====


def income_data(data):
    locan_income = dict()  # 放款
    receive_income = dict()  # 收款
    game_income = dict()  # 游戏
    sub_income = dict()  # 订阅
    locan_income_action = action_type('locan')
    receive_income_action = action_type('receive')
    game_income_action = action_type('game')
    sub_income_action = action_type('sub')

    for v in data:
        action = int(v.actiontype)
        rate_amount = round(rate_currency(v.total, v.ccy), 2)
        if action in locan_income_action:
            if v.create_time in locan_income:
                locan_income[v.create_time]['t'] += rate_amount
                locan_income[v.create_time]['n'] += int(v.num)
            else:
                locan_income[v.create_time] = dict(
                    t=rate_amount,
                    n=int(v.num)
                )
        elif action in receive_income_action:
            if v.create_time in receive_income:
                receive_income[v.create_time]['t'] += rate_amount
                receive_income[v.create_time]['n'] += int(v.num)
            else:
                receive_income[v.create_time] = dict(
                    t=rate_amount,
                    n=int(v.num)
                )
        elif action in game_income_action:
            if v.create_time in game_income:
                game_income[v.create_time]['t'] += rate_amount
                game_income[v.create_time]['n'] += int(v.num)
            else:
                game_income[v.create_time] = dict(
                    t=rate_amount,
                    n=int(v.num)
                )
        elif action in sub_income_action:
            if v.create_time in sub_income:
                sub_income[v.create_time]['t'] += rate_amount
                sub_income[v.create_time]['n'] += int(v.num)
            else:
                sub_income[v.create_time] = dict(
                    t=rate_amount,
                    n=int(v.num)
                )

    income = dict(
        locan=locan_income,
        receive=receive_income,
        game=game_income,
        sub=sub_income
    )

    return income


@home.route("/", methods=["GET", "POST"])
@is_login_req
def index():
    """
    后台汇总
    :return:
    """
    if request.method == 'POST':

        dt = datetime.now()
        mt = dt.strftime("%Y%m")
        # 处理每个月1 号问题
        st = dt.strftime("%d")
        if st == '01':
            yesterday = datetime.today() + timedelta(-1)
            yesterday_format = yesterday.strftime('%Y%m')
            mt = yesterday_format

        TbModel = NewTbModel(Tb_transaction_backup, 'tb_transaction_backup_' + mt)

        # 获取数据
        data = TbModel.query.with_entities(
            TbModel.create_time,
            TbModel.actiontype,
            TbModel.ccy,
            func.sum(TbModel.numbers).label('num'),
            func.sum(TbModel.price * TbModel.numbers).label('total')
        ).filter(
            TbModel.status == 200,
            TbModel.operator_id != 9,
            TbModel.price > 0
        ).group_by(
            TbModel.create_time,
            TbModel.actiontype,
            TbModel.ccy
        ).all()

        # 查询今日流水，实时查询 前两个小时
        day_time_day = dt.strftime("%Y-%m-%d")  # 获取
        filters_hour = {
            Cdr_file_hour.hour_time >= day_time_day + '-00'
        }
        data_hour = Cdr_file_hour.query.with_entities(
            Cdr_file_hour.actiontype,
            Cdr_file_hour.currency.label('ccy'),
            Cdr_file_hour.hour_time.label('create_time'),
            func.sum(Cdr_file_hour.amount).label('total'),
            func.sum(Cdr_file_hour.numbers).label('num')
        ).filter(*filters_hour).group_by(
            Cdr_file_hour.hour_time,
            Cdr_file_hour.actiontype,
            Cdr_file_hour.currency
        ).order_by(
            Cdr_file_hour.hour_time.asc()
        ).all()

        es_total =0
        """
        qry = Cdr_file_hour.query.order_by(
            Cdr_file_hour.create_time.desc(),
            Cdr_file_hour.id.desc()
        ).limit(1).all()
        es_total = 0
        if qry :
            hour_time_str = qry[0].hour_time
            hour_time_es = hour_time_str.replace('-', '')

            es_data = real_time(hour_time_es+'0000')

            records = es_data['aggregations']['currency']['buckets']
            es_total = 0
            if records:
                for v in records:
                    es_total += round(rate_currency(v['doc_count'], v['key']), 2)
        """

        print(es_total)


        income_hour = income_data(data_hour)

        income = income_data(data)

        return json.dumps([income, income_hour,es_total])

    return render_template("home/index.html")



def real_time(time):
    """
    实时数据
    :param time:
    :return:
    """
    return  es.search(
        index='transaction',
        request_timeout=300,
        body={
            "query": {
                "bool": {
                    "filter": [
                        {
                            "bool": {
                                "must": [
                                    {
                                        "bool": {
                                            "must": [
                                                {
                                                    "range": {
                                                        "create_time": {
                                                            "from": time,
                                                            "to": None,
                                                            "include_lower": False,
                                                            "include_upper": True,
                                                            "boost": 1.0
                                                        }
                                                    }
                                                },
                                                {
                                                    "match_phrase": {
                                                        "status": {
                                                            "query": 200,
                                                            "slop": 0,
                                                            "boost": 1.0
                                                        }
                                                    }
                                                },
                                                {
                                                    "range": {
                                                        "price": {
                                                            "from": 0,
                                                            "to": None,
                                                            "include_lower": False,
                                                            "include_upper": True,
                                                            "boost": 1.0
                                                        }
                                                    }
                                                },
                                                {
                                                    "bool": {
                                                        "must_not": [
                                                            {
                                                                "match_phrase": {
                                                                    "operator_id": {
                                                                        "query": 9,
                                                                        "slop": 0,
                                                                        "boost": 1.0
                                                                    }
                                                                }
                                                            }
                                                        ],
                                                        "disable_coord": False,
                                                        "adjust_pure_negative": True,
                                                        "boost": 1.0
                                                    }
                                                }
                                            ],
                                            "disable_coord": False,
                                            "adjust_pure_negative": True,
                                            "boost": 1.0
                                        }
                                    }
                                ],
                                "disable_coord": False,
                                "adjust_pure_negative": True,
                                "boost": 1.0
                            }
                        }
                    ],
                    "disable_coord": False,
                    "adjust_pure_negative": True,
                    "boost": 1.0
                }
            },
            "aggregations": {
                "currency": {
                    "terms": {
                        "field": "currency",
                        "size": 200,
                        "min_doc_count": 1,
                        "shard_min_doc_count": 0,
                        "show_term_doc_count_error": False,
                        "order": [
                            {
                                "_count": "desc"
                            },
                            {
                                "_term": "asc"
                            }
                        ]
                    }
                }
            }
        }
    )



@home.route("/bluecons/list/<int:page>/", methods=["GET","POST"])
@is_login_req
@home_auth
def blue_coins(page=None):
    """
    BlueCoins列表
    """

    form = BlueCoinForm()
    if request.method =='POST':
        if form.validate_on_submit():
            data = form.data

            # 检测路径，否则创建
            blue_dir = app.config["BLUE_DIR"]
            if not os.path.exists(blue_dir):
                # 创建一个多级目录
                os.makedirs(blue_dir)
                os.chmod(blue_dir, "rw")  # 授权读写

            dt = datetime.now()
            mt = dt.strftime("%Y%m%d%H")

            # 组合数据
            amount = data['amount']
            numbers = int(data['numbers'])
            url='http://203.154.114.7:21813/voucher/generateVoucher'
            voucherKey='BEST'

            try:
                for i in range(0, numbers):
                    transactionId = 'best'+random_str(12)
                    customerId='66'+random_str(6)
                    cardNote = transactionId+customerId
                    data_encrypt = dict(
                        cardType=1,
                        channel=0,
                        transactionId=transactionId,
                        customerId=customerId,
                        producerId=1,
                        currency='THB',
                        amount=amount,
                        cardNote=cardNote,
                        validity=360
                    )
                    voucherParams = urlencode(data_encrypt)
                    str_md5='%s%s'%(voucherParams,voucherKey)
                    encrypt_text = PHPmd5(str_md5)
                    data_encrypt['encrypt'] = encrypt_text
                    open_url = url+'?'+urlencode(data_encrypt)
                    response = urllib.request.urlopen(open_url)

                    print(response.info())
                    res = response.read().decode()

                    #res ='{"result":{"activityId":0,"amount":50,"batchId":"batch20180330160141185EkU","cardNo":"6437937526832855","cardNote":"best7bqCdJl3H9Mk66uaA36Y","cardType":1,"channel":0,"createTime":"2018-03-30 16:01:41","currency":"THB","customerId":"66uaA36Y","expiredTime":"2019-03-25 16:01:41","innerId":"THB20180330160141187XpS","producerId":1,"status":0,"transactionId":"best7bqCdJl3H9Mk"},"status":200}'

                    blue_coin_log = open(blue_dir+mt+'.log', 'a')
                    blue_coin_log.write(dt.strftime("%Y-%m-%d %H:%M:%S")+'||'+res+'|| '+session['admin']+"\n")
                    blue_coin_log.close()

                    dict_res = json.loads(s=res)
                    result = dict_res['result']
                    cardNo = str(result['cardNo'])
                    amount = str(result['amount'])
                    cardNo_info = cardNo + ' | ' + amount

                    # 写入文件
                    file_name = mt+'_'+amount+'_'+str(numbers)+'.txt'
                    file_path = blue_dir+file_name
                    blue_coin_file = open(file_path, 'a')
                    blue_coin_file.write(cardNo_info+"\n")
                    blue_coin_file.close()

                    coins_dir = blue_dir.split('/')[-2]

                    print(coins_dir+'/'+file_name)
                    # 添加操作日志
                    bluecons_log = Bluecoins_log(
                        data=voucherParams,
                        url=encrypt_text,
                        name=session['admin'],
                        result='cardNo:'+ cardNo_info,
                        filename=coins_dir+'/'+file_name
                    )

                    db.session.add(bluecons_log)
                    db.session.commit()
                    time.sleep(0.2)

                flash("[{0}] [{1}]导出成功".format(amount, numbers), "ok")
            except:
                db.session.rollback()
                flash("[{0}] [{1}]导出失败".format(amount, numbers), "err")
            return redirect(url_for('home.blue_coins', page=1))
    else:
        if page is None:
            page = 1
        page_data = Bluecoins_log.query.order_by(
            Bluecoins_log.create_time.desc()
        ).paginate(page=page, per_page=10)
    return render_template("home/bluecons_list.html", page_data=page_data,form=form)



@home.route("/day/", methods=["GET"])
@is_login_req
@home_auth
def day():
    """
    按天流水
    :return:
    """
    # 获取产生流水CP/SP ，近似值
    dt = datetime.now()
    mt = dt.strftime("%Y%m")
    st = dt.strftime("%d")
    if st == '01':  # 处理每个月1 号问题
        yesterday = datetime.today() + timedelta(-1)
        yesterday_format = yesterday.strftime('%Y%m')
        mt = yesterday_format

    TbModel = NewTbModel(Tb_transaction_backup, 'tb_transaction_backup_' + mt)
    data = TbModel.query.filter(
        TbModel.status == 200,
        TbModel.operator_id != 9,
        TbModel.price > 0
    ).group_by(
        TbModel.producer_id,
        TbModel.product_id
    ).order_by(
        TbModel.producer_id
    ).all()

    producers = dict()
    for v in Ref_producer.query.all():
        producers[str(v.producer_id)] = v.producer_name

    products = dict()
    for v in Product_info.query.all():
        products[str(v.product_id)] = v.product_name

    sub_cp = []
    game_cp = []
    temp = []  # 临时使用
    tempa = []  # 临时使用

    sub_pro = []
    game_pro = []

    sub = action_type('sub')
    game = action_type('game')
    for v in data:
        if int(v.producer_id) > 0:
            if int(v.actiontype) in sub:
                # CP
                if v.producer_id not in temp:
                    sub_cp.append(
                        dict(
                            producer_id=v.producer_id,
                            producer_name=producers[str(v.producer_id)]
                        )
                    )
                    temp.append(v.producer_id)

                # 产品
                sub_pro.append(
                    dict(
                        producer_id=v.producer_id,
                        producer_name=producers[str(v.producer_id)],
                        product_id=v.product_id,
                        product_name=v.product_id
                    )
                )

            elif int(v.actiontype) in game:
                if v.producer_id not in tempa:
                    game_cp.append(
                        dict(
                            producer_id=v.producer_id,
                            producer_name=producers[str(v.producer_id)]
                        )
                    )
                    tempa.append(v.producer_id)

                # 产品
                game_pro.append(
                    dict(
                        producer_id=v.producer_id,
                        producer_name=producers[str(v.producer_id)],
                        product_id=v.product_id,
                        product_name=products[str(v.product_id)]
                    )
                )

    search_data = dict(
        cp=game_cp,
        sp=sub_cp,
        cpp=game_pro,
        spp=sub_pro,
    )
    # print(search_data)
    return render_template("home/day.html", search_data=search_data)


# 按天流水Ajax
@home.route("/get_day_data/", methods=["POST"])
@is_login_req
@home_auth
def get_day_data():
    """
    获取当天数据
    :return:
    """
    if request.method == 'POST':

        data = request.form
        time_month = data['time_month']  # 获取时间
        producer_id = data['producer_id']
        product_id = data['product_id']
        business = data['business']
        start_end_time = list(map(lambda v: str(v), time_month.split(" ~ ")))
        start_time = start_end_time[0]
        end_time = start_end_time[1]

        start_time_str = start_time.replace("-", "")
        end_time_str = end_time.replace("-", "")
        start_time_m = start_time_str[0: 6]
        end_time_m = end_time_str[0: 6]

        start_end_time = [start_time_m, end_time_m]
        data = []
        for mt in start_end_time:
            TbModel = NewTbModel(Tb_transaction_backup, 'tb_transaction_backup_' + mt)
            filters = {
                TbModel.status == 200,
                TbModel.operator_id != 9,
                TbModel.price > 0,
                TbModel.create_time <= end_time,
                TbModel.create_time >= start_time
            }

            if len(producer_id) > 0:
                filters.add(TbModel.producer_id == producer_id)

            if len(product_id) > 0:
                filters.add(TbModel.product_id == product_id)

            if len(business) > 0:
                action = action_type(business)
                filters.add(TbModel.actiontype.in_(action))

            data += TbModel.query.with_entities(
                TbModel.create_time,
                TbModel.producer_id,
                TbModel.product_id,
                TbModel.numbers,
                TbModel.ccy,
                func.sum(TbModel.price * TbModel.numbers).label('total')
            ).filter(*filters).group_by(
                TbModel.create_time,
                TbModel.ccy
            ).order_by(
                TbModel.create_time.asc()
            ).all()

        print(data)
        data_out = dict()
        for v in data:
            rate_amount = round(rate_currency(v.total, v.ccy), 2)
            if v.create_time in data_out:
                data_out[v.create_time]['n'] += v.numbers
                data_out[v.create_time]['t'] += rate_amount
            else:
                data_out[v.create_time] = dict(
                    t=rate_amount,
                    n=v.numbers
                )
        return json.dumps(data_out)


@home.route("/charge/", methods=["GET", "POST"])
@is_login_req
@home_auth
def charge():
    """
    重点关注
    :return:
    """

    # 查询当月数据
    dt = datetime.now()
    mt = dt.strftime("%Y%m")
    st = dt.strftime("%d")
    if st == '01':  # 处理每个月1 号问题
        yesterday = datetime.today() + timedelta(-1)
        yesterday_format = yesterday.strftime('%Y%m')
        mt = yesterday_format

    selected = 0
    spp = 0
    TbModel = NewTbModel(Tb_transaction_backup, 'tb_transaction_backup_' + mt)
    filters = {
        TbModel.status == '200',
        TbModel.operator_id != '9',
        TbModel.price > '0'
    }

    # 拼接过滤条件
    cp = request.args.get("cp", 0)
    if cp != 0:
        filters.add(TbModel.producer_id == cp)
        selected = int(cp)

    ccy = request.args.get("ccy", 0)
    if ccy != 0:
        filters.add(TbModel.ccy == ccy)
        action = action_type('sub')
        filters.add(TbModel.actiontype.in_(action))
        selected = str(ccy)

    sp = request.args.get("sp", 0)
    if sp != 0:
        filters.add(TbModel.producer_id == sp)
        action = action_type('sub')
        filters.add(TbModel.actiontype.in_(action))
        selected = int(sp)
        spp = 1

    # 执行查询
    data = TbModel.query.with_entities(
        TbModel.create_time,
        TbModel.ccy,
        func.sum(TbModel.price * TbModel.numbers).label('total')
    ).filter(*filters).group_by(
        TbModel.create_time,
        TbModel.ccy
    ).order_by(
        TbModel.create_time.desc()
    ).all()

    # 查询上个月数据
    num = 30 - len(data)  # 补上数据
    if num > 0:
        day_time_before = datetime.now() + timedelta(days=-30)
        day_time_format = day_time_before.strftime("%Y%m")  # 获取

        TbModel_LAST = NewTbModel(Tb_transaction_backup, 'tb_transaction_backup_' + day_time_format)

        filters_last = {
            TbModel_LAST.status == '200',
            TbModel_LAST.operator_id != '9',
            TbModel_LAST.price > '0'
        }

        # 拼接过滤条件
        if cp != 0:
            filters_last.add(TbModel_LAST.producer_id == cp)

        if ccy != 0:
            filters_last.add(TbModel_LAST.ccy == ccy)
            action = action_type('sub')
            filters_last.add(TbModel_LAST.actiontype.in_(action))

        if sp != 0:
            filters_last.add(TbModel_LAST.producer_id == sp)
            action = action_type('sub')
            filters_last.add(TbModel_LAST.actiontype.in_(action))

        day_time_day = day_time_before.strftime("%Y-%m-%d")  # 获取
        filters_last.add(TbModel_LAST.create_time >= day_time_day)

        data_last = TbModel_LAST.query.with_entities(
            TbModel_LAST.create_time,
            TbModel_LAST.ccy,
            func.sum(TbModel_LAST.price * TbModel_LAST.numbers).label('total')
        ).filter(*filters_last).group_by(
            TbModel_LAST.create_time,
            TbModel_LAST.ccy
        ).order_by(
            TbModel_LAST.create_time.desc()
        ).all()

        if data_last:
            data += data_last

    data_out = dict()
    for v in data:
        rate_amount = round(rate_currency(v.total, v.ccy), 2)
        if v.create_time in data_out:
            data_out[v.create_time] += rate_amount
        else:
            data_out[v.create_time] = rate_amount

    return render_template("home/charge.html", data_out=data_out, selected=selected, spp=spp)


# 定时任务处理cdr_file 文件
@home.route('/jobs/list/<int:page>/', methods=["GET"])
@is_login_req
@home_auth
def job_list(page):
    """
    任务日志列表
    """
    # 获取数据表数据

    form = JobForm()
    task = TaskForm()

    # 任务日志
    if page is None:
        page = 1
    page_data = Backup_log.query.order_by(
        Backup_log.create_time.desc()  # 倒序
    ).paginate(page=page, per_page=6)  # page当前页 per_page 分页显示多少条

    # 任务列表
    if page is None:
        page = 1
    task_data = TaskList.query.order_by(
        TaskList.create_time.desc()  # 倒序
    ).paginate(page=page, per_page=10)  # page当前页 per_page 分页显示多少条

    return render_template('home/job_list.html', page_data=page_data,form=form,task=task,task_data=task_data)  # 权限管理


@home.route('/jobs/', methods=["GET", "POST"])
@is_login_req
@home_auth
def jobs():
    form = JobForm()
    if form.validate_on_submit():
        dt = datetime.now()
        start_time = dt.strftime('%Y-%m-%d %H:%M:%S')
        try:
            data = form.data
            action = data['action']
            field = data['field']
            where = data['where']
            if action == '1':
                text = '删除'
                if field == 'hour_time':
                    Cdr_file_hour.query.filter(Cdr_file_hour.hour_time == where).delete()
                elif field == 'create_time':
                    Cdr_file_hour.query.filter(Cdr_file_hour.create_time == where).delete()
                db.session.commit()
            if action == '2':
                text = '补充'
                filters = {
                    Cdr_file.status == 200,
                    Cdr_file.operator_id != 9,
                    Cdr_file.price > 0
                }

                if field == 'hour_time':
                    star_hour_time = where[0:10] + ' ' + where[11:13] + ':00:00'
                    end_hour_time = where[0:10] + ' ' + where[11:13] + ':59:59'
                    filters.add(Cdr_file.create_time >= star_hour_time)
                    filters.add(Cdr_file.create_time <= end_hour_time)

                elif field == 'create_time':
                    star_hour_time = where  #
                    end_hour_time = where.replace('00', '59')
                    filters.add(Cdr_file.create_time >= star_hour_time)
                    filters.add(Cdr_file.create_time <= end_hour_time)

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

                print(data)
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

            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 添加备份日志
            backup_log = Backup_log(
                backup_time=end_time,
                func_name=session['admin']+'手动执行:'+text,
                used_time=start_time + ' ~ ' + end_time,
                cdr_file_max_time=action + ' ~ ' + where
            )
            db.session.add(backup_log)
            db.session.commit()

            flash("[{0}] [{1}]操作成功".format(text, where), "ok")
        except:
            db.session.rollback()
            flash("[{0}] [{1}]操作失败".format(text, where), "err")

    return redirect(url_for('home.job_list', page=1))




@home.route('/addtask/', methods=["GET", "POST"])
@is_login_req
def addtask():
    """
    添加
    :param id:
    :return:
    """
    form = TaskForm()
    if form.validate_on_submit():
        data = form.data
        # 组合数据
        task = TaskList(
            name=data['name'],
            task=data['task'],
            format=data['format'],
            func=data['func'],
            args=data['args'],
            info=data['info'],
            status=1
        )

        try:
            json.loads(data['format']) # 检测是否为JSON格式
            # 执行添加
            db.session.add(task)
            db.session.commit()
            flash("添加任务成功！", "ok")
        except:
            db.session.rollback()
            flash('添加任务失败，请严格按照格式输入！', 'err')

    return redirect(url_for('home.job_list', page=1))
    """
    #scheduler.add_job(func='app.home.jobs:task1', id='1', args=(1, 2), trigger='interval', seconds=5, replace_existing=True)
    data = dict(status=200,message='success')
    return json.dumps(data)
    """


@home.route('/task/', methods=["POST"])
@is_login_req
def task():
    if request.method=='POST':
        form = request.form
        input_id = form['id']
        task = form['task']
        task_data = TaskList.query.filter_by(id=input_id).first_or_404()
        id = str(task_data.id)
        out_data = dict(status=200, message='suceess')

        if task =='start':
            func=task_data.func
            args = task_data.args
            args_ditc = list(map(lambda v: int(v), args.split(",")))
            trigger = task_data.task
            format = task_data.format

            format_dict = eval(format)
            # 关键字可变参数
            task_args={
                'func': func,
                'id': id,
                'args':args_ditc,
                'trigger':trigger,
                'replace_existing':True
            }
            # 遍历字典列表
            for key, values in format_dict.items():
                task_args[key] = values
            try:
                scheduler.add_job(**task_args)
                #scheduler.add_job(func=func, id=id, args=args_ditc, trigger=trigger, seconds=5, replace_existing=True)
                status = 2
            except:
                out_data = dict(status=400, message='error')

        elif  task =='stop':
            scheduler.pause_job(id)
            status = 3
        elif task == 'move':
            scheduler.delete_job(id)
            status = 4
        elif task == 'restart':
            scheduler.resume_job(id)
            status = 5
        else:
            db.session.delete(task_data)
            db.session.commit()

        # 更状态，排除删除数据
        if task != 'del':
            task_data.status = status
            db.session.commit()
    return json.dumps(out_data)


@home.route("/elastics/", methods=["GET", "POST"])
@is_login_req
@home_auth
def elastics():
    """
    查询ES
    """
    if request.method == 'POST':
        data = request.form
        filed = data['filed']
        value = data['value']
        draw = int(data['draw'])
        query = int(data['query'])
        length = data['length']
        start = data['start']
        time_month = request.form['time']  # 获取时间
        start_end_time = list(map(lambda v: str(v), time_month.split(" ~ ")))
        star_time_dt = start_end_time[0] + ' 00:00:00'
        end_time_dt = start_end_time[1] + ' 23:59:59'
        # 转换成时间数组
        star_time_timeArray = time.strptime(star_time_dt, "%Y-%m-%d %H:%M:%S")
        end_time_timeArray = time.strptime(end_time_dt, "%Y-%m-%d %H:%M:%S")
        # 转换成新的时间格式(20160505202854)
        star_time_dt_new = time.strftime("%Y%m%d%H%M%S", star_time_timeArray)
        end_time_dt_new = time.strftime("%Y%m%d%H%M%S", end_time_timeArray)
        try:
            out_data = []
            if query == 1:
                _source = es.search(
                    index='transaction',
                    q=filed + ':' + value,  # 使用精准匹配
                    size=length,
                    from_=start,
                    sort='create_time:desc',
                    request_timeout=300
                )
            elif query == 2:
                _source = es.search(
                    index='transaction',
                    size=length,
                    from_=start,
                    sort='create_time:desc',
                    request_timeout=300,
                    body={
                        "query": {
                            "bool": {
                                "filter": [
                                    {
                                        "bool": {
                                            "must": [
                                                {
                                                    "bool": {
                                                        "must": [
                                                            {
                                                                "range": {
                                                                    "create_time": {
                                                                        "from": star_time_dt_new,
                                                                        "to": None,
                                                                        "include_lower": False,
                                                                        "include_upper": True,
                                                                        "boost": 1
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "range": {
                                                                    "create_time": {
                                                                        "from": None,
                                                                        "to": end_time_dt_new,
                                                                        "include_lower": True,
                                                                        "include_upper": False,
                                                                        "boost": 1
                                                                    }
                                                                }
                                                            },
                                                            {
                                                                "match_phrase": {
                                                                    filed: {
                                                                        "query": value,
                                                                        "slop": 0,
                                                                        "boost": 1
                                                                    }
                                                                }
                                                            }
                                                        ],
                                                        "disable_coord": False,
                                                        "adjust_pure_negative": True,
                                                        "boost": 1
                                                    }
                                                }
                                            ],
                                            "disable_coord": False,
                                            "adjust_pure_negative": True,
                                            "boost": 1
                                        }
                                    }
                                ],
                                "disable_coord": False,
                                "adjust_pure_negative": True,
                                "boost": 1
                            }
                        }
                    }
                )

            records = _source['hits']['total']
            if _source['hits']:
                for v in _source['hits']['hits']:
                    out_data.append(v['_source'])
            es_data = dict(
                data=out_data,
                draw=draw,
                recordsFiltered=records,
                recordsTotal=records
            )
        except:
            es_data = dict(data=[], draw=0, recordsFiltered=0, recordsTotal=0)
        return json.dumps(es_data)

    return render_template("home/elastics.html")


@home.route("/adjust/", methods=["GET", "POST"])
@is_login_req
@home_auth
def adjust():
    """
    调整收入
    :return:
    """
    if request.method == 'POST':
        data = request.form
        time_month = data['time_month']  # 获取时间
        length = data['length']
        start = data['start']
        draw = int(data['draw'])

        start_end_time = list(map(lambda v: str(v), time_month.split(" ~ ")))
        income = request.form['income']
        star_time = start_end_time[0]
        end_time = start_end_time[1]
        if income in ['sub', 'pay', 'trs', 'everworks', 'idr']:

            if income in ['sub', 'everworks', 'idr']:
                table_name = 'tb_transaction_backup_sub'
            elif income == 'pay':
                table_name = 'tb_transaction_backup_pay'
            elif income == 'trs':
                table_name = 'tb_transaction_backup_trs'

            TbModel = NewTbModel(Tb_transaction_backup, table_name)  # 创建新模型
            if income in ['sub', 'pay', 'trs']:
                filters = {
                    TbModel.create_time <= end_time,
                    TbModel.create_time >= star_time
                }
            elif income in ['everworks']:
                filters = {
                    TbModel.create_time <= end_time,
                    TbModel.create_time >= star_time,
                    TbModel.operator_id == '17'
                }
            elif income in ['idr']:
                filters = {
                    TbModel.create_time <= end_time,
                    TbModel.create_time >= star_time,
                    TbModel.ccy == 'IDR'
                }

            producers = dict()
            for v in Ref_producer.query.all():
                producers[str(v.producer_id)] = v.producer_name

            tbcount = TbModel.query.filter(*filters).count()
            # print(tbcount)

            data = TbModel.query.with_entities(
                TbModel.create_time,
                TbModel.telco_name,
                TbModel.shortcode,
                TbModel.producer_id,
                TbModel.ccy,
                func.sum(TbModel.price * TbModel.numbers).label('total')
            ).filter(*filters).group_by(
                TbModel.create_time,
                TbModel.telco_name,
                TbModel.shortcode,
                TbModel.producer_id,
                TbModel.ccy
            ).order_by(
                TbModel.create_time.desc()
            ).offset(start).limit(length).all()
            list_data = []
            for v in data:
                rate_amount = round(rate_currency(v.total, v.ccy), 2)
                producer_name = producers[v.producer_id]
                list_data.append(
                    dict(
                        create_time=v.create_time,
                        telco_name=v.telco_name,
                        shortcode=v.shortcode,
                        producer_id=v.producer_id,
                        producer_name=producer_name,
                        ccy=v.ccy,
                        total=rate_amount
                    )
                )

        elif income in ['shelve']:
            tbcount = 0
            list_data = dict(
                create_time=0,
                telco_name=0,
                shortcode=0,
                producer_id=0,
                ccy=0,
                total=0
            )

        table_data = dict(
            data=list_data,
            draw=draw,
            recordsFiltered=tbcount,
            recordsTotal=tbcount
        )
        return json.dumps(table_data)

    return render_template("home/adjust.html")


@home.route("/get_adjust_data/", methods=["POST"])
@is_login_req
@home_auth
def get_adjust_data():
    """
    获取优化数据
    :return:
    """
    if request.method == 'POST':
        time_month = request.form['time_month']  # 获取时间
        start_end_time = list(map(lambda v: str(v), time_month.split(" ~ ")))
        income = request.form['income']
        star_time = start_end_time[0]
        end_time = start_end_time[1]
        data_out = dict()
        if income in ['sub', 'pay', 'trs', 'everworks', 'idr']:
            if income in ['sub', 'everworks', 'idr']:
                table_name = 'tb_transaction_backup_sub'
            elif income == 'pay':
                table_name = 'tb_transaction_backup_pay'
            elif income == 'trs':
                table_name = 'tb_transaction_backup_trs'

            TbModel = NewTbModel(Tb_transaction_backup, table_name)  # 创建新模型

            if income in ['sub', 'pay', 'trs']:
                filters = {
                    TbModel.create_time <= end_time,
                    TbModel.create_time >= star_time
                }
            elif income in ['everworks']:
                filters = {
                    TbModel.create_time <= end_time,
                    TbModel.create_time >= star_time,
                    TbModel.operator_id == '17'
                }
            elif income == 'idr':
                filters = {
                    TbModel.create_time <= end_time,
                    TbModel.create_time >= star_time,
                    TbModel.ccy == 'IDR'
                }

            data = TbModel.query.with_entities(
                TbModel.create_time,
                TbModel.price,
                TbModel.ccy,
                func.sum(TbModel.price * TbModel.numbers).label('total')
            ).filter(*filters).group_by(
                TbModel.create_time,
                TbModel.ccy
            ).order_by(
                TbModel.create_time.asc()
            ).all()

            # 输出数据
            data_out = dict()
            for v in data:
                rate_amount = round(rate_currency(v.total, v.ccy), 2)  # 转化后金额
                if v.create_time in data_out:
                    data_out[v.create_time] += rate_amount
                else:
                    data_out[v.create_time] = rate_amount

        elif income in ['shelve']:

            end_time_str = end_time + ' 23:59:59'
            data = Subs_subscription.query.with_entities(
                Subs_subscription.subscriped_time,
                func.DATE_FORMAT(Subs_subscription.lastupdate_time, '%Y%m%d').label('day'),
                func.count(1).label('num')
            ).filter(
                Subs_subscription.state == 'T',
                Subs_subscription.lastupdate_time <= end_time_str
            ).group_by(
                func.DATE_FORMAT(Subs_subscription.lastupdate_time, '%Y%m%d')
            ).order_by(
                Subs_subscription.lastupdate_time.desc()
            ).limit(30).all()

            for v in data:
                if v.day in data_out:
                    data_out[v.day] += v.num
                else:
                    data_out[v.day] = v.num

        return json.dumps(data_out)


@home.route("/admin/list/<int:page>/", methods=["GET"])
@is_login_req
@home_auth
def admin_list(page=None):
    """
    管理员列表
    """
    if page is None:
        page = 1
    page_data = Admin.query.join(
        Role
    ).filter(
        Role.id == Admin.role_id
    ).order_by(
        Admin.create_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template("home/admin_list.html", page_data=page_data)


@home.route("/admin/add/", methods=["GET", "POST"])
@is_login_req
@home_auth
def admin_add():
    """
    添加管理员
    """
    form = AdminForm()
    if form.validate_on_submit():
        try:
            data = form.data
            admin = Admin(
                name=data["name"],
                pwd=generate_password_hash(data["pwd"]),
                role_id=data["role_id"]
            )
            db.session.add(admin)
            db.session.commit()
            flash("添加管理员成功", "ok")
        except:
            db.session.rollback()
            flash("添加管理员失败", "err")
    return render_template("home/admin_add.html", form=form)


@home.route('/admin/edit/<int:id>/', methods=["GET", "POST"])
@is_login_req
@home_auth
def admin_edit(id):
    """
    管理员编辑
    """
    form = AdminForm()
    admin = Admin.query.get_or_404(int(id))
    # 编辑时赋初值，文本域，下拉框
    if request.method == "GET":
        form.role_id.data = admin.role_id

    if form.validate_on_submit():
        data = form.data
        try:
            admin.name = data['name']
            admin.role_id = data['role_id']
            admin.pwd = generate_password_hash(data['pwd'])
            db.session.add(admin)
            db.session.commit()
            flash("管理员[{0}]修改成功".format(admin.id), "ok")
        except:
            db.session.rollback()
            flash("管理员[{0}]修改失败".format(admin.id), "err")
    return render_template('home/admin_edit.html', form=form, admin=admin)  # 权限添加


@home.route('/auth/add/', methods=["GET", "POST"])
@is_login_req
@home_auth
def auth_add():
    """
    权限添加
    """
    form = AuthForm()
    if form.validate_on_submit():
        data = form.data
        # 组合数据
        auth = Auth(
            name=data['name'],
            url=data['url']
        )
        try:
            # 执行添加
            db.session.add(auth)
            db.session.commit()
            flash("添加权限成功！", "ok")
        except:
            db.session.rollback()
            flash('添加权限失败，请重新输入！', 'err')
    return render_template('home/auth_add.html', form=form)  # 权限添加


@home.route('/auth/list/<int:page>/')
@is_login_req
@home_auth
def auth_list(page):
    """
    标签列表
    """
    # 获取数据表数据
    if page is None:
        page = 1
    page_data = Auth.query.order_by(
        Auth.create_time.desc()  # 倒序
    ).paginate(page=page, per_page=10)  # page当前页 per_page 分页显示多少条
    return render_template('home/auth_list.html', page_data=page_data)  # 权限管理


@home.route('/auth/del/<int:id>', methods=["GET"])
@is_login_req
@home_auth
def auth_del(id):
    """
    权限删除
    """
    auth = Auth.query.filter_by(id=id).first_or_404()  # 查询记录是否存在
    db.session.delete(auth)
    db.session.commit()

    flash("权限[{0}]删除成功".format(auth.id), "ok")
    return redirect(url_for("home.auth_list", page=1))


@home.route('/auth/edit/<int:id>/', methods=["GET", "POST"])
@is_login_req
@home_auth
def auth_edit(id):
    """
    权限编辑
    """
    form = AuthForm()
    auth = Auth.query.get_or_404(int(id))
    if form.validate_on_submit():
        data = form.data
        try:
            auth.name = data['name']
            auth.url = data['url']
            db.session.add(auth)
            db.session.commit()
            flash("权限[{0}]修改成功".format(auth.id), "ok")
        except:
            db.session.rollback()
            flash("权限[{0}]修改失败".format(auth.id), "err")
    return render_template('home/auth_edit.html', form=form, auth=auth)  # 权限添加


@home.route('/role/list/<int:page>/')
@is_login_req
@home_auth
def role_list(page):
    """
    角色列表
    """
    # 获取数据表数据
    if page is None:
        page = 1
    page_data = Role.query.order_by(
        Role.create_time.desc()  # 倒序
    ).paginate(page=page, per_page=10)  # page当前页 per_page 分页显示多少条
    return render_template('home/role_list.html', page_data=page_data)  # 权限管理


@home.route('/role/add/', methods=["GET", "POST"])
@is_login_req
@home_auth
def role_add():
    form = RoleForm()
    if form.validate_on_submit():
        data = form.data
        auths = request.form.getlist('auths')
        #print(data['auths'])
        try:
            role = Role(
                name=data['name'],
                auths=",".join(map(lambda v: str(v), auths))
            )
            db.session.add(role)
            db.session.commit()
            flash("添加[{0}]权限成功".format(data['name']), "ok")
        except:
            db.session.rollback()
            flash("添加[{0}]权限失败".format(data['name']), "err")

    return render_template('home/role_add.html', form=form)  # 角色添加


@home.route('/role/del/<int:id>/', methods=["GET"])
@is_login_req
@home_auth
def role_del(id):
    """
    角色删除
    """
    role = Role.query.filter_by(id=id).first_or_404()  # 查询记录是否存在
    db.session.delete(role)
    db.session.commit()

    flash("角色[{0}]删除成功".format(role.id), "ok")
    return redirect(url_for("home.role_list", page=1))


@home.route('/role/edit/<int:id>/', methods=["GET", "POST"])
@is_login_req
@home_auth
def role_edit(id):
    """
    角色编辑
    """
    form = RoleForm()
    role = Role.query.get_or_404(int(id))
    if request.method == "GET":
        auths = role.auths
        if auths:
            # get时进行赋值。应对无法模板中赋初值
            form.auths.data = list(map(lambda v: int(v), auths.split(",")))
    if form.validate_on_submit():
        data = form.data
        try:
            role.name = data['name']
            auths = request.form.getlist('auths')
            role.auths = ",".join(map(lambda v: str(v), auths))
            db.session.add(role)
            db.session.commit()
            flash("权限[{0}]修改成功".format(role.id), "ok")
        except:
            db.session.rollback()
            flash("权限[{0}]修改失败".format(role.id), "err")
    return render_template('home/role_edit.html', form=form, role=role)


@home.route('/pwd/', methods=["POST", "GET"])
@is_login_req
def pwd():
    """
    后台密码修改
    """
    form = PwdForm()
    if form.validate_on_submit():  # 验证密码
        data = form.data
        admin = Admin.query.filter_by(name=session["admin"]).first()
        admin.pwd = generate_password_hash(data["new_pwd"])  # 修改密码
        db.session.add(admin)
        db.session.commit()
        flash("修改密码成功，请重新登录！", "ok")
        return redirect(url_for('home.logout'))
    return render_template('home/pwd.html', form=form)  # 修改密码











@home.route("/login/", methods=["GET", "POST"])
def login():
    """
    登录界面
    :return:
    """
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


@home.route('/logout/')
def logout():
    """
    退出登录
    """
    # 重定向到home模块下的登录。
    session.pop("admin", None)
    session.pop("admin_id", None)
    session.pop("auth", None)
    flash('已安全退出。', 'ok')
    return redirect(url_for('home.login'))  # 退出跳转到登录界面
