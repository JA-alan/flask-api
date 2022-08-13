import hashlib
import threading
import time
import datetime
import json
from random import random
import random
from threading import Timer
from apscheduler.schedulers.blocking import BlockingScheduler
from update_db import Update_Sql


def inset_md5(psd):
    """生成md5"""
    m = hashlib.md5()
    b = psd.encode(encoding='utf-8')
    m.update(b)
    md5_token = m.hexdigest()
    return md5_token


def inset_user():
    """造数据"""
    import random
    user = ''
    user1 = ['周', '赵', '钱', '孙', '李', '朱', '吴', '郑', '王', '张', '谢', '麦', '冯', '刘', '汤', '熊']
    user2 = ['春', '兰', '怀', '雅', '琪', '安', '子', '发', '若', '正', '耀', '让', '俊', '要', '梓', '浩']
    user3 = ['玉', '建', '嚄', '宇', '玲', '满', '曼', '末', '旺', '卫', '才', '伟', '从', '峰', '费', '坤']
    user1 = random.choice(user1)[0]
    user += user1
    user2 = random.choice(user2)[0]
    user += user2
    user3 = random.choice(user3)[0]
    user += user3
    sex = [1, 0]
    age = random.randint(18, 40)
    c = random.choice(sex)


def t_stamp():
    """转换时间格式"""
    t = time.time()
    t_tamp = int(t)
    return t_tamp


def inset_token():
    """生成token"""
    API_SECRET = 'JIANGAN'
    project_code = "test"
    account = "jiangan"
    time_stamp = str(t_stamp())
    h1 = hashlib.md5()
    strs = project_code + account + time_stamp + API_SECRET
    h1.update(strs.encode("utf-8"))
    user_token = h1.hexdigest()
    return user_token


class DateEncoder(json.JSONEncoder):
    """解决json不能序列化时间日期问题"""

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)


def inst_token():
    scheduler = BlockingScheduler()
    scheduler.add_job("清除token")


def func():
    now = datetime.datetime.now()
    ts = now.strftime('%Y-%m-%d %H:%M:%S')
    return ts,


def dojob():
    # 创建调度器：BlockingScheduler
    scheduler = BlockingScheduler()
    # 添加任务,时间间隔2S
    scheduler.add_job(func, 'interval', seconds=10, id='test_job1')
    # 添加任务,时间间隔5S
    scheduler.start()


class token_del:
    """
    定时器
    run:100秒执行一次定时器
    """
    def __init__(self):
        t1 = threading.Timer(1, function=self.run)  # 创建定时器
        t1.start()  # 开始执行线程

    def run(self):  # 定义方法
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  # 输出当前时间
        timer = threading.Timer(100, self.run)  # 每秒运行
        timer.start()  # 执行方法
        Update_Sql().time_del_token()


def random_phone():
    """随机获取手机号"""
    reu = ""
    reu1 = "1"
    cat_phone = ["32", "58", "31", "71", "55", "33", "47"]
    reu = reu + reu1
    cat_phone = random.choices(cat_phone)[0]
    reu = reu + cat_phone
    for i in range(8):
        num = str(random.randint(1, 9))
        reu += num
    return reu

