#coding:utf-8

import os, sys
import time
import traceback
import json
import datetime as dt

from . import datacenter as __dc

### config

__curdir = os.path.dirname(os.path.abspath(__file__))

__dc.set_config_dir(os.path.join(__curdir, 'config'))

__data_home_dir = 'data'

__quote_token = ''


### function

def set_token(token = ''):
    '''
    设置用于登录行情服务的token，此接口应该先于init_quote调用
    token获取地址：https://xuntou.net/#/userInfo
    迅投投研服务平台 - 用户中心 - 个人设置 - 接口TOKEN
    '''
    global __quote_token
    __quote_token = token
    return


def set_data_home_dir(data_home_dir):
    '''
    设置数据存储目录，此接口应该先于init_quote调用
    datacenter启动后，会在data_home_dir目录下建立若干目录存储数据
    如果不设置存储目录，会使用默认路径
    在datacenter作为独立行情服务的场景下，data_home_dir可以任意设置
    如果想使用现有数据，data_home_dir对应QMT的f'{安装目录}'，或对应极简模式的f'{安装目录}/userdata_mini'
    '''
    global __data_home_dir
    __data_home_dir = data_home_dir
    return


def init(start_local_service = True):
    '''
    初始化行情模块
    start_local_service: bool
        如果start_local_service为True，会额外启动一个默认本地监听，以支持datacenter作为独立行情服务时的xtdata内置连接
    '''
    __dc.set_data_home_dir(__data_home_dir)
    __dc.set_token(__quote_token)
    __dc.start_init_quote()

    status = __dc.get_status()
    while not status.get('init_done', False):
        status = __dc.get_status()
        time.sleep(0.5)

    if start_local_service:
        listen('127.0.0.1', 58609)
    return


def shutdown():
    '''
    关闭行情模块，停止所有服务和监听端口
    '''
    __dc.shutdown()
    return


def listen(ip = '0.0.0.0', port = 58610):
    '''
    独立行情服务模式，启动监听端口，支持xtdata.connect接入
    ip:
        str, '0.0.0.0'
    port:
        int, 指定监听端口
        tuple, 指定监听端口范围，从port[0]至port[1]逐个尝试监听
    返回:
        (ip, port), 表示监听的结果
    示例:
        from xtquant import xtdatacenter as xtdc
        ip, port = xtdc.listen('0.0.0.0', 58610)
        ip, port = xtdc.listen('0.0.0.0', (58610, 58620))
    '''
    if isinstance(port, tuple):
        port_start, port_end = port
        return __dc.listen(ip, port_start, port_end)

    return __dc.listen(ip, port, port)
