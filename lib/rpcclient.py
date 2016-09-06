#
# Copyright (C) 2015 Xiao-Fang Huang <huangxfbnu@163.com>
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#

from lib.bson import loads
from lib.package import pack
from dpmclient import DPMClient

class RPCClient():
    def __init__(self, addr, port, uid=None, key=None):
        self.dpmclient = DPMClient(uid, key)
        self.addr = addr
        self.port = port
        
    def request(self, op, *args, **kwargs):
        buf = pack(op, args, kwargs)
        res = self.dpmclient.request(self.addr, self.port, buf)
        if res:
            ret = loads(res)
            return ret['res']