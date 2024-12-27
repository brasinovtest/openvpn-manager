from telnetlib import Telnet
from typing import Callable, Optional, Any

from openvpn_manager.decorators import parser


class ManagerObject:

    def __init__(self, name: str, parent: Callable) -> None:
        self.object = name
        self.parent = parent

    def __getattr__(self, name: str) -> Callable:
        def func(*args: Any, **kwargs: Any) -> Any:
            if name != 'execute':
                raise AttributeError(f"{self.parent} object has no attribute '{name}'")
            method = self.object.replace('_', '-')
            return self.parent._perform_execute(method, *args, **kwargs)
        return func


class OpenVPNManager:
    __session: Telnet
    __connected: bool = False

    def __init__(self, ip_address: Optional[str] = None, port_number: Optional[int] = None, timeout: int = 30) -> None:
        if ip_address and port_number:
            self.connect(ip_address, port_number, timeout)

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def __getattr__(self, name: str) -> Callable:
        return ManagerObject(name, self)

    @property
    def ip_address(self):
        return self.__ip_address

    @property
    def port_number(self):
        return self.__port_number

    @property
    def timeout(self):
        return self.__timeout

    @property
    def session(self):
        return self.__session

    @property
    def connected(self):
        return self.__connected

    def __enter__(self) -> "OpenVPNManager":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def connect(self, ip_address: str, port_number: int, timeout: int = 30) -> None:
        if not self.connected:
            self.__session = Telnet(ip_address, port_number, timeout)
            self.__connected = True

    def close(self) -> None:
        if self.connected:
            self.session.close()
            self.__connected = False

    def raise_exception_if_not_connected(self):
        if not self.connected:
            raise ConnectionError("Connection to OpenVPN server has not been established")


    @parser
    def _perform_execute(self, method: str, *args, **kwargs):
        self.raise_exception_if_not_connected()
        value = bytes(f"{method}\n", 'ascii')
        self.session.write(value)
        output = self.session.read_until(b"END\n", 1)
        return output.decode('ascii')
