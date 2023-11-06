"""Modbus connection management"""
import time
from pymodbus.client import ModbusTcpClient
from ..common import getLogger


__copyright__ = "Copyright 2023 binchoo"
__license__ = "GPLv3"
__author__ = "Jaebin Joo"
__email__ = "jaebin.joo@megazone.com"


_logger_ = getLogger(__name__)

def safeget(getter, default):
    if getter is not None:
        v = getter()
        return v if v is not None else default
    return default


class SingleModbusConnection:
    '''Singleton modbus connection manager'''

    def get_connection(self, *args, **kwargs):
        raise NotImplementedError


class ModbusTCPConnection(SingleModbusConnection):

    def __init__(self):
        self.client = None # singleton connection

    def get_connection(self, get_host, get_port, get_max_retry=None, get_wait_sec=None, **kwargs):
        max_retry = max(0, safeget(get_max_retry, 2147483647))
        while max_retry >= 0:
            host = safeget(get_host, '127.0.0.1')
            port = safeget(get_port, 502)
            wait_sec = safeget(get_wait_sec, 10)

            _logger_.info(f"Connecting to {host}:{port} (max_retry={max_retry}, wait_sec={wait_sec})")

            if self._connect(host, port):
                return self.client

            max_retry -= 1
            time.sleep(wait_sec)

        raise RuntimeError("Connection ultimately failed")

    def _connect(self, host, port):
        if self.client is not None:
            self.client.close()

        self.client = ModbusTcpClient(host=host, port=port)
        self.client.connect()

        if self.client.connected:
            _logger_.info(f"Connected to {host}:{port}")
            return True
        else:
            _logger_.warning(f"Connection failed")
            return False

class ModbusRTUConnection(SingleModbusConnection):
    pass
