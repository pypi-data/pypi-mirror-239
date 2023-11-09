import logging.handlers
import asyncio
import datetime
import json
from collections import deque
from pg_environment import config
from pg_logging.define import *
from pg_common.func import start_coroutines, log_print
from pg_logging.log_client import LogClient
__FORMATTED_LOG_FLAG_NAME__ = "_formatted_log"


class TcpHandler(logging.handlers.TimedRotatingFileHandler):
    def __init__(self, filename, *args, **kwargs):
        self._formatted_log = kwargs.get(__FORMATTED_LOG_FLAG_NAME__, False)
        if __FORMATTED_LOG_FLAG_NAME__ in kwargs:
            del kwargs[__FORMATTED_LOG_FLAG_NAME__]
        logging.handlers.TimedRotatingFileHandler.__init__(self, filename, *args, **kwargs)
        _log_cfg = config.get_conf(KEY_LOG)
        self._target_host = _log_cfg[KEY_LOG_TCP_HOST]
        self._target_port = _log_cfg[KEY_LOG_FORMAT_LOG_PORT] if self._formatted_log \
            else _log_cfg[KEY_LOG_NON_FORMAT_LOG_PORT]
        self._client = LogClient(self._target_host, self._target_port, filename)
        self._queue = deque()
        self._is_finished = False
        self._filename = filename
        start_coroutines(self._get_all_coroutines())

    def send(self, record):
        self._queue.append(record)

    def _send(self, _msg):
        self._client.send(bytes(_msg.encode()))

    def _get_all_coroutines(self):
        return [self._coroutine_sending_logs]

    async def _coroutine_sending_logs(self):
        while not self._is_finished:
            if self._client.is_connected() and len(self._queue) > 0:
                _log = self._queue.popleft()
                try:
                    self._send(_log)
                except Exception as e:
                    self.send(_log)
                    log_print(f"{self._filename} sending error: {e}")
            else:
                # if Core.debug and not self._client.is_connected():
                #     print(f"{self._filename}'s socket client is not connected.")
                await asyncio.sleep(3)

    def emit(self, record):
        if self._client.is_connected():
            _log_time = datetime.datetime.utcfromtimestamp(
                        record.__dict__['created']).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            if self._formatted_log:
                if type(record.__dict__['msg']) == dict and '_log_dict_' in record.__dict__['msg']:
                    _tmp = record.__dict__['msg']['_log_dict_']
                    _tmp.update({'log_file': self._filename,
                                 'log_name': record.__dict__['name'],
                                 'log_level': record.__dict__['levelname'],
                                 'log_time': _log_time})
                    self.send("%s\n" % json.dumps(_tmp))

                    if config.get_conf(KEY_LOG)[KEY_LOG_FORMAT_LOG_OUTPUT_LOCAL]:
                        record.__dict__['msg'] = record.__dict__['msg']['_log_str_']
                        logging.handlers.TimedRotatingFileHandler.emit(self, record)
                else:
                    logging.handlers.TimedRotatingFileHandler.emit(self, record)

            else:
                _tmp = {
                    'log_time': _log_time,
                    "log_file": self._filename,
                    'log_level': record.__dict__['levelname'],
                    "message": self.format(record)
                }
                self.send("%s\n" % json.dumps(_tmp))
                if config.get_conf(KEY_LOG)[KEY_LOG_NON_FORMAT_LOG_OUTPUT_LOCAL]:
                    logging.handlers.TimedRotatingFileHandler.emit(self, record)
        else:
            if self._formatted_log:
                if type(record.__dict__['msg']) == dict and '_log_dict_' in record.__dict__['msg']:
                    record.__dict__['msg'] = record.__dict__['msg']['_log_str_']

            logging.handlers.TimedRotatingFileHandler.emit(self, record)

    def close(self):
        if self._client.is_connected():
            while len(self._queue) > 0:
                self._send(self._queue.popleft())
        self._is_finished = True
        logging.handlers.TimedRotatingFileHandler.close(self)
