#
# Copyright (C) 2015 Xiao-Fang Huang <huangxfbnu@163.com>
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#

import rsa
import socket
from threading import Lock
from lib.stream import Stream

class DPMClient():   
    def __init__(self, uid=None, key=None):
        self._lock = Lock()
        self._uid = uid
        self._key = None
        if key:
            self._key = rsa.PublicKey.load_pkcs1(key)
      
    def request(self, addr, port, buf):
        self._lock.acquire()
        try:
            return self._request(addr, port, buf)
        finally:
            self._lock.release()
    
    def _request(self, addr, port, buf):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((addr, port))
        try:
            if self._key:
                stream = Stream(sock, uid=self._uid, key=self._key)
            else:
                stream = Stream(sock)
            stream.write( buf)
            if self._key:
                stream = Stream(sock)
            _, _, res = stream.readall()
            return res
        finally:
            sock.close()
