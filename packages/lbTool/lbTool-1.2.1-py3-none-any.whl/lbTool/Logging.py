from datetime import datetime
import logging
from logging import config
import os


class Logger:
    def __init__(self, cover_existing_logger=False):
        """
        初始化
        :param cover_existing_logger: 是否覆盖已存在的日志记录器，默认False
        """
        # 配置日志记录 日志级别从低到高 DEBUG->INFO->WARNING->ERROR->CRITICAL
        if not os.path.exists(f"{os.getcwd()}/Log"):
            os.mkdir(f"{os.getcwd()}/Log")
        # 1.基本配置
        # logging.basicConfig(level=logging.DEBUG,  # 设置日志级别为 DEBUG（最低级别）
        #                     filename=f'Log/Logs_{datetime.now().strftime("%Y%m%d")}.log',  # 指定日志文件名
        #                     filemode='a',  # 设置文件模式为追加写入
        #                     format='%(asctime)s - %(levelname)s - %(message)s')
        # 2.加载配置文件
        logging.config.fileConfig('config/log.conf',
                                  defaults={
                                      'Ymd': datetime.now().strftime("%Y%m%d"),
                                      'dir_name': 'Log'
                                  },
                                  disable_existing_loggers=cover_existing_logger)
        # 获取文件输出
        self.logger = logging.getLogger("fileLogger")

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)
