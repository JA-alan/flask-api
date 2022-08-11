import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))  # 项目根目录
LOG_PATH = os.path.join(PROJECT_ROOT, 'test-one/log', 'api_test.log')  # 日志路径

BASE_URL_test = "127.0.0.1"  # 本地url
BASE_URL_dev = '43.138.182.131'  # 线上


def host():
    return "localhost"


def user():
    return "root"


def dbname():
    return "test-root"


def psd():
    return "asd123456"
# def host():
#     # return "localhost"
#     return "43.138.182.131"
#
#
# def user():
#     # return "root"
#     return "flask-test"
#
#
# def dbname():
#     # return "test-root"
#     return "flask-test"
