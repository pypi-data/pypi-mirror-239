# -*- coding: utf-8 -*-

"""
@Project : hertz_packet 
@File    : __init__.py
@Date    : 2023/5/12 10:31:05
@Author  : zhchen
@Desc    : 发送一些消息
"""
import json
from json import JSONDecodeError

import requests

note_server_url = "https://note-tempnote-edzsrbkyef.cn-hangzhou.fcapp.run"


def send_note(_k, _v, _memo: dict = None):
    """发送键值对到数据库，用于分析情况"""
    try:
        data = {"key": _k, "value": _v, }
        if _memo:
            data['memo'] = json.dumps(_memo)
        requests.post(note_server_url, json=data)
    except Exception:
        pass


def get_kv(_k, default=None):
    """Since 2.2.0 增加自动转换memo"""
    headers = {'content-type': 'application/json'}
    params = {"key": _k}
    if default is not None:
        params['default'] = default
    response = requests.get(f"{note_server_url}/kv", headers=headers, params=params)
    _msg = response.json()['msg']
    if 'memo' in _msg and _msg['memo']:
        try:
            _msg['memo'] = json.loads(_msg['memo'])
        except JSONDecodeError:
            pass
    return _msg


def set_kv(_k, _v, _memo: dict = None):
    headers = {'content-type': 'application/json'}
    data = {"key": _k, "value": _v, }
    if _memo:
        data['memo'] = json.dumps(_memo)
    response = requests.post(f"{note_server_url}/kv", json=data, headers=headers)
    return response.json()
