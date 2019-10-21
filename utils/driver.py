#
# Copyright (C) Xu Tian <tianxu@iscas.ac.cn>
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#

from hash_ring import HashRing
from conf.log import LOG_DRIVER
from lib.rpcclient import RPCClient
from lib.log import show_info, show_error
from conf.servers import SERVER_REPOSITORY, REPOSITORY_PORT

class Driver(object):
    def _print(self, text):
        if LOG_DRIVER:
            show_info(self, text)
    
    def _get_repo(self, package):
        ring = HashRing(SERVER_REPO)
        server = ring.get_node(package)
        return server
    
    def install(self, uid, package, version):
        addr = self._get_repo(package)
        rpcclient = RPCClient(addr, REPOSITORY_PORT)
        if not version:
            version = rpcclient.request('version', package=package)
            if not version:
                show_error(self, 'failed to install, invalid version, uid=%s, package=%s' % (uid, package))
                return
        ret = rpcclient.request('download', package=package, version=version)
        return ret
