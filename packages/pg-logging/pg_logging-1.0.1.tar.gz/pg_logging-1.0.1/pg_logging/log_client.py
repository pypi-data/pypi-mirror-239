import asyncio
from pg_common.func import log_print


class LogProtocol(asyncio.Protocol):
    def __init__(self, _host, _port, _log_name):
        self._host = _host
        self._port = _port
        self._log_name = _log_name

    def connection_made(self, transport):
        log_print(f"{self._log_name} connect to ({self._host}:{self._port}) made.")

    def connection_lost(self, exc):
        log_print(f"{self._log_name} connect to ({self._host}:{self._port}) lost.")


class LogClient(object):
    def __init__(self, _host, _port, _log_name):
        self._t_host = _host
        self._t_port = _port
        self._log_name = _log_name
        self._transport = None
        self._start()

    def _start(self):
        asyncio.create_task(self._run())

    def is_connected(self):
        if self._transport and not self._transport.is_closing():
            return True
        return False

    async def _connect(self):
        loop = asyncio.get_running_loop()
        self._transport, _ = await loop.create_connection(lambda:
                                                          LogProtocol(self._t_host, self._t_port, self._log_name),
                                                          self._t_host, self._t_port)
        log_print(f"{self._log_name} connection created.")

    async def _run(self):
        while True:
            try:
                if not self.is_connected():
                    log_print(f"{self._log_name} starting to connect.")
                    await self._connect()
                await asyncio.sleep(5)
            except Exception as e:
                log_print(f"{self._log_name} starting connect error: {e}")
                await asyncio.sleep(3)

    def send(self, _data):
        if self.is_connected():
            self._transport.write(_data)
        else:
            log_print(f"{self._log_name} sending data {_data} dropped....")
