#
# Copyright (C) 2015 Xiao-Fang Huang <huangxfbnu@163.com>
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#

from conf.config import LOG_ERROR, LOG_DEBUG

def log_err(location, text):
    if LOG_ERROR:
        print('%s: %s' % (location, text))
        
def log_debug(location, text):
    if LOG_DEBUG:
        print('%s: %s' % (location, text))

def show_info(cls, text):
    log_debug(cls.__class__.__name__, text)
    
def show_error(cls, text):
    log_err(cls.__class__.__name__, text)