#
# Copyright (C) 2015 Xu Tian <tianxu@iscas.ac.cn>
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#

import zlib
import json
from log import show_error
from conf.config import SCAN_TOOL

if SCAN_TOOL == 'pyblade':
    from pyblade import scan

class Scanner(object):
    def _do_scan(self, files):
        result = scan(files)
        if result:
            return True
    
    def _extract(self, content):
        if content.get('app'):
            files = content.get('app')
        elif content.get('driver'):
            files = content.get('driver')
        else:
            show_error(self, 'cannot extract')
            return
        filenames = filter(lambda f: f.endswith('.py'), files)
        info = {}
        for name in filenames:
            file = files.get(name)
            info.update({name: file})
        return info
    
    def _scan(self, buf):
        text = zlib.decompress(buf)
        content = json.loads(text)
        if not content or type(content) != dict:
            show_error(self, 'invalid content')
            return
        files = self._extract(content)
        if files:
            if not self._do_scan(files):
                raise Exception('this package contains invalid files')
        return content.get('description')
    
    def scan(self, buf):
        return self._scan(buf)
