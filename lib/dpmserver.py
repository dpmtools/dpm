#
# Copyright (C) 2015 Xiao-Fang Huang <huangxfbnu@163.com>
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#

import rsa
import struct
import socket
import threading
from lib.stream import Stream
from conf.config import SHOW_TIME
from lib.log import show_info, show_error
from conf.log import LOG_DPMSERVER
from lib.stream import UID_LEN, FLG_LEN, FLG_SEC
from SocketServer import BaseRequestHandler, TCPServer, ThreadingMixIn

if SHOW_TIME:
    from datetime import datetime

CACHE_MAX = 4096

class DPMRequestHandler(BaseRequestHandler):
    def _print(self, text):
        if LOG_DPMSERVER:
            show_info(self, text)
    
    def handle(self):
        if SHOW_TIME:
            start_time = datetime.utcnow()
        uid = self.request.recv(UID_LEN)
        if len(uid) != UID_LEN:
            show_error(self, 'failed to handle, invalid head')
            return
        buf = self.request.recv(FLG_LEN)
        if len(buf) != FLG_LEN:
            show_error(self, 'failed to handle, invalid head')
            return
        flg, = struct.unpack('I', buf)
        if flg == FLG_SEC:
            if not self.server.rpcserver.user:
                show_error(self, 'user is not initialized')
                raise Exception('user is not initialized')
            key = self.server.cache_get(uid)
            if not key:
                key = self.server.rpcserver.user.get_private_key(uid)
                if not key:
                    show_error(self, 'failed to handle, invalid private key')
                    return
                key = rsa.PrivateKey.load_pkcs1(key)
                self.server.cache_update(uid, key)
            stream = Stream(self.request, uid=uid, key=key)
        else:
            stream = Stream(self.request)
        buf = stream.read()
        if buf:
            res = self.server.rpcserver.proc(buf)
            if flg == FLG_SEC:
                stream = Stream(self.request)
            stream.write(res)
        if SHOW_TIME:
            self._print('handle, time=%d sec' % (datetime.utcnow() - start_time).seconds)

class DPMTCPServer(ThreadingMixIn, TCPServer):
    def set_server(self, rpcserver):
        self._cache = {}
        self.rpcserver = rpcserver
    
    def cache_get(self, uid):
        return self._cache.get(uid)
    
    def cache_update(self, uid, key):
        if len(self._cache) >= CACHE_MAX:
            self._cache.popitem()
        self._cache.update({uid:key})
    
class DPMServer(object):
    def run(self, rpcserver):
        self.server = DPMTCPServer((rpcserver.addr, rpcserver.port), DPMRequestHandler)
        self.server.set_server(rpcserver) 
        self.server.serve_forever()
