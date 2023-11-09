import asyncio
from pg_common import log_info


async def handle(reader, writer):
    _peer_name = writer.get_extra_info('socket').getpeername()
    log_info(f"client connected: {_peer_name}.")
    while True:
        _req = await reader.readline()
        if not _req:
            log_info(f"client loss: {_peer_name}.")
            break
        log_info(_req.decode())


async def serve():
    _server = await asyncio.start_server(handle, "0.0.0.0", 5555)
    _address = _server.sockets[0].getsockname()
    log_info(f"Serving on: {_address}.")

    async with _server:
        await _server.serve_forever()


def run():
    try:
        asyncio.run(serve())
    except KeyboardInterrupt:
        log_info("stop server gracefully.")


if __name__ == "__main__":
    run()
