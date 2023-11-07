#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   LogUtil.py
@Describe :  封装日志输出相关的初始化和配置
        调用示例：
            from util import LogUtil
            default_logger = LogUtil.initLogConfig(__name__)
            default_logger.debug('This is a debug message.')
@Contact :   mrbingzhao@qq.com
@License :   (C)Copyright 2023/11/7, Liugroup-NLPR-CASIA

@Modify Time        @Author       @Version    @Desciption
----------------   -----------   ---------    -----------
2023/11/7 上午8:51   liubingzhao      1.0           ml
'''

import logging


def initLogConfig(logger_name='main', log_file='logs/service.log'):
    '''
    初始化日志配置
    :param logger_name:默认值为
    :param log_file: 默认值为logs/service.log
    :return:
    '''
    level = logging.DEBUG
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    log_formatter = logging.Formatter(
        '[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    log_file_handler = logging.FileHandler(log_file)
    log_file_handler.setLevel(logging.INFO)
    log_file_handler.setFormatter(log_formatter)

    log_console_handler = logging.StreamHandler()
    log_console_handler.setLevel(level)
    log_console_handler.setFormatter(log_formatter)

    logger.addHandler(log_file_handler)
    logger.addHandler(log_console_handler)

    return logger
