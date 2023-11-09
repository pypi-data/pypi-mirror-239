VERSION = "1.0.2"


# -*- encoding: utf-8 -*-
"""
    @Contact: baozilaji@gmail.com
    @Modify Time: 2022/7/5 11:42
    @Author: Eric
    @Version: 1.0
    @Description: None
"""
import os
import getpass
import logging
from logging.handlers import TimedRotatingFileHandler
from pg_logging.define import *
from pg_common import log_info
from pg_environment import config as penv


class Logger:
    _log_level = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warn': logging.WARN,
        'error': logging.ERROR,
        'fatal': logging.FATAL
    }

    @classmethod
    def init(cls):
        _log_cfg = penv.get_conf(KEY_LOG)
        _uname = os.uname().sysname
        _log_dir = _log_cfg[KEY_LOG_DIR][_uname]
        if _uname == "Darwin":
            _log_dir = _log_dir % (getpass.getuser(), )
        _log_dir = "%s/%s" % (_log_dir,
                                    penv.get_env())
        log_info(f"non formatted log dir: {_log_dir}")
        if not os.path.exists(_log_dir):
            os.makedirs(_log_dir)

        _fmt = "%(asctime)s %(levelname)s %(message)s"
        _fmt2 = "%(message)s"
        _format = logging.Formatter(fmt=_fmt2)
        logging.basicConfig(level=cls._log_level[_log_cfg[KEY_LOG_LEVEL]], format=_fmt)

        for _key in cls._log_level.keys():
            _logger = logging.getLogger(_key)
            if not _log_cfg[KEY_LOG_OUTPUT_CONSOLE]:
                _logger.propagate = False
            cls.add_handler(_logger, _format, f"{_log_dir}/{_key}.log", _using_tcp_log=True)

    @classmethod
    def add_handler(cls, _logger, _format, _path, _using_tcp_log=False, _formatted_log=False):
        if _using_tcp_log:
            from pg_logging.tcp_handler import TcpHandler
            _file_handler = TcpHandler(_path,
                                                            when="midnight",
                                                            backupCount=5,
                                                            _formatted_log=_formatted_log)
        else:
            _file_handler = TimedRotatingFileHandler(_path, when="midnight", backupCount=5)
        _file_handler.setFormatter(_format)
        _logger.addHandler(_file_handler)

    @classmethod
    def debug(cls, msg):
        logging.getLogger("debug").debug(msg)

    @classmethod
    def info(cls, msg):
        logging.getLogger("info").info(msg)

    @classmethod
    def warn(cls, msg):
        logging.getLogger("warning").warning(msg)

    @classmethod
    def error(cls, msg):
        logging.getLogger("error").error(msg)

    @classmethod
    def fatal(cls, msg):
        logging.getLogger("fatal").fatal(msg)
