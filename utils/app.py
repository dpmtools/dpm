#
# Copyright (C) 2015 Xiao-Fang Huang <huangxfbnu@163.com>,  Xu Tian <tianxu@iscas.ac.cn>
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#

from threading import Lock
from lib.db import Database
from conf.log import LOG_APP
from hash_ring import HashRing
from lib.util import APP, localhost
from lib.rpcclient import RPCClient
from conf.config import INSTALL_TOOL
from lib.log import show_info, show_error
from conf.servers import SERVER_REPOSITORY, SERVER_APPDB, REPOSITORY_PORT

if INSTALL_TOOL == 'vdtools':
    from vdtools import installer

class App():
    def __init__(self):
        self._lock = Lock()
        if SERVER_APPDB:
            self._db = Database(addr=SERVER_APPDB[0], domain=APP)
        else:
            self._db = Database(addr=localhost(), domain=APP)
    
    def _print(self, text):
        if LOG_APP:
            show_info(self, text)
    
    def _get_repo(self, package):
        ring = HashRing(SERVER_REPO)
        server = ring.get_node(package)
        return server
    
    def _install(self, uid, content):
        if  content:
            return True
#         output = installer.install(uid, content)
#         if output:
#             return output
        else:
            return str(None)
    
    def install(self, uid, package, version, content):
        self._lock.acquire()
        try:
            if self._db.has_package(uid, package, None):
                show_error(self, 'failed to install, cannot install %s again' % package)
                return
            else:
                result = self._install(uid, content)
                if result:
                    self._db.set_package(uid, package, version, result)
                    self._print('finished installing %s, version=%s' % (package, version))
                    return True
        finally:
            self._lock.release()
    
    def _uninstall(self, uid, package, info):
        pass
        
    def uninstall(self, uid, package):
        self._lock.acquire()
        try:
            if not self._db.has_package(uid, package, None):
                show_error(self, 'failed to uninstall %s' % package)
                return
            version, info = self._db.get_package(uid, package, None)
            if info:
                self._uninstall(uid, package, info)
            self._db.rm_package(uid, package, version)
            return True
        finally:
            self._lock.release()
    
    def get_packages(self, uid):
        return self._db.get_packages(uid)
    
    def has_package(self, uid, package):
        return self._db.has_package(uid, package)

    