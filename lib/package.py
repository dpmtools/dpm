#
# Copyright (C) 2015 Xiao-Fang Huang <huangxfbnu@163.com>
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#

from lib.log import log_err
from lib.bson import dumps, loads

def pack(op, args, kwargs):
    if type(op) != str or type(args) != tuple or type(kwargs) != dict:
        log_err('package', 'failed to pack, invalid type')
        return
    buf = {'op': op, 'args': args, 'kwargs': kwargs}
    return dumps(buf)

def unpack(buf):
    tmp = loads(buf)
    if type(tmp) != dict or not tmp.has_key('op') or not tmp.has_key('args') or not tmp.has_key('kwargs'):
        log_err('package', 'failed to unpack, invalid type')
        return
    op = tmp['op']
    args = tmp['args']
    kwargs = tmp['kwargs']
    if type(op) != str or type(args) != list or type(kwargs) != dict:
        log_err('package', 'failed to unpack, invalid arguments')
        return
    return (op, args, kwargs)
