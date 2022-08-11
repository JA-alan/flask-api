import os
import logging
from logging import handlers
from setting import LOG_PATH
import time
from logging.handlers import RotatingFileHandler


def init_logging():
    # 1 初始化日志器
    logger = logging.getLogger()
    # 2 设置日志等级
    logger.setLevel(logging.INFO)
    # 3 创建控制处理器
    sh = logging.StreamHandler()
    # 4 创建文件处理器 - LOG_PATH为setting.py内的变量
    fh = logging.handlers.TimedRotatingFileHandler(filename=LOG_PATH, when='D', interval=1, backupCount=7,
                                                   encoding='utf-8')
    fmt = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s %(funcName)s:%(lineno)d] - [%(message)s]"
    formatter = logging.Formatter(fmt)
    # 6 将格式化器添加到处理器
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)
    # 7 将处理器添加到日志
    logger.addHandler(sh)
    logger.addHandler(fh)


# if __name__ == '__main__':
#     init_logging()
    # logging.info('——————————————测试一下—————————————————1')


# def make_dir(mark_dir_path):
#     path = mark_dir_path.strip()
#     if not os.path.exists(path):
#         os.makedirs(path)
#
#
# def getLogHandlers():
#     log_dir_name = "Logs"
#     log_file_name = "logger-" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())) + "log"
#
#     log_file_folder = os.path.abspath(
#         os.path.join(os.path.dirname(__file__), os.pardir)) + os.sep + log_dir_name
#     make_dir(log_file_folder)
#     log_file_str = log_file_folder + os.sep + log_file_name
#
#     logging.basicConfig(level=logging.WARNING)
#     file_log_handler = RotatingFileHandler(log_file_str, maxBytes=1024 * 1024, backupCount=10, encoding="utf-8")
#     formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] [%(filename)s %(funcName)s:%(lineno)d] - [%(message)s]")
#     file_log_handler.setFormatter(formatter)
#
#     return file_log_handler
