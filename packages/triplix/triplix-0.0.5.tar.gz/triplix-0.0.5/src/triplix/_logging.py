
# inspired from pairtools: https://github.com/open2c/pairtools/blob/master/pairtools/_logging.py

import logging

from triplix.core import configurations

_loggers = {}


def get_logger(name="triplix", level=None):
    global _loggers

    if name not in _loggers:
        _loggers[name] = logging.getLogger(name)
        _loggers[name].propagate = False

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s %(name)s [%(levelname)s]: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
        )
        handler.setFormatter(formatter)
        _loggers[name].addHandler(handler)
        
        if level is None:
            level=logging.DEBUG if configurations.configs['debug'] else logging.INFO
        _loggers[name].setLevel(level)
    
    return _loggers[name]
