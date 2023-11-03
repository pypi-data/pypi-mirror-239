# -*- coding: utf-8 -*-

"""
@Project : hertz_packet 
@File    : log.py
@Date    : 2023/5/19 17:56:47
@Author  : zhchen
@Desc    : 
"""
import logging
import os
import random
import sys
from datetime import datetime


class Logger:
    def __init__(self, log_path=None, file_name=None):
        logger_name = file_name or f"{__name__}{random.randint(0, 15)}"
        self.logger = logging.getLogger(logger_name)  # 创建日志记录器
        self.logger.setLevel(logging.INFO)  # 日志记录器的等级

        _format = logging.Formatter('%(asctime)s [%(filename)s] %(levelname)s: %(message)s',
                                    datefmt='%Y-%m-%d %H:%M:%S')

        today = datetime.now().strftime("%Y_%m_%d")
        log_path = log_path or f'./log/{today}'
        now = datetime.now().strftime("%H_%M_%S")
        filename = file_name or f"{os.path.basename(sys.argv[0]).split('.')[0]}_{now}.log"
        os.path.exists(log_path) or os.makedirs(log_path)
        file_handler = logging.FileHandler(f"{log_path}/{filename}", encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(_format)

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(_format)

        if self.logger.handlers:
            self.logger.handlers.clear()
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console)

    def get_logger(self):
        return self.logger
