#
# Copyright (C) 2015 Xiao-Fang Huang <huangxfbnu@163.com>
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#

from lib.user import User
from lib.bson import dumps
from lib.package import unpack
from dpmserver import DPMServer
from lib.log import show_error

class RPCServer(object):   
    def __init__(self, addr, port, user=None):
        self.dpmserver = DPMServer()
        self.addr = addr
        self.port = port
        self.user = user
    
    def run(self):
        self.dpmserver.run(self)
    
    def __proc(self, op, args, kwargs):
        res = ''
        func = getattr(self, op)
        if func:
            ret = func(*args, **kwargs)
            if ret:
                res = ret
        return dumps({'res':res})
    
    def proc(self, buf):
        try:
            op, args, kwargs = unpack(buf)
            return self.__proc(op, args, kwargs)
        except:
           show_error(self, 'failed to process')
    
