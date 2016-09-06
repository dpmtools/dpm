#
# Copyright (C) 2015 Xiao-Fang Huang <huangxfbnu@163.com>,  Xu Tian <tianxu@iscas.ac.cn>
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#

from utils.app import App
from utils.driver import Driver
from threading import Thread
from lib.log import show_error
from lib.rpcserver import RPCServer
from lib.util import APP, DRIVER, localhost
from conf.servers import INSTALLER_PORT

class Installer(RPCServer):
    def __init__(self, addr, port):
        RPCServer.__init__(self, addr, port)
        self._app = App()
        self._driver = Driver()
    
    def install(self, uid, package, version, typ, content):
        if typ == APP:
            return self._app.install(uid, package, version, content)
        elif typ == DRIVER:
            return self._driver.install(uid, package, version)
        else:
            show_error(self, 'failed to install, invalid type, typ=%s' % str(typ))
    
    def uninstall(self, uid, package, typ):
        if typ == APP:
            return self._app.uninstall(uid, package)
        else:
            show_error(self, 'failed to uninstall, invalid type, typ=%s' % str(typ))
    
    def get_packages(self, uid, typ):
        if typ == APP:
            return self._app.get_packages(uid)
    
    def has_package(self, uid, package, typ):
        if typ == APP:
            return self._app.has_package(uid, package)
    
    def start(self):
        t = Thread(target=self.run)
        t.start()
        t.join()

def main():
    inst = Installer(localhost(), INSTALLER_PORT)
    inst.start()
