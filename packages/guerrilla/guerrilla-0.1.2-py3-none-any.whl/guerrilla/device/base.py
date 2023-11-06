from dataclasses import dataclass, field
from guerrilla.connection import Session
from guerrilla.connection.session import BaseSession
from guerrilla.utils.decorator import log


@dataclass
class BaseDevice:
    # name: str
    # type: str
    # connections: dict
    config: dict
    session: BaseSession = field(init=False)

    def __post_init__(self):
        self.name = self.config.get("name", None)
        self.session = Session(config=self.config)

    def connect(self) -> None:
        self.session.connect()

    def disconnect(self) -> None:
        self.session.disconnect()

    @log
    def run(self, command: str, expect_string: str = None) -> str:
        return self.session.run(command, expect_string=expect_string)

    @log
    def run_timing(self, command: str, last_read: int = 2) -> str:
        return self.session.run_timing(command, last_read)

    def find_prompt(self) -> str:
        return self.session.find_prompt()

    @property
    def status(self) -> str:
        return self.session.status


@dataclass
class Device:
    config: dict

    def __new__(cls, config: dict):
        device_model = config.get("type", None)
        match device_model:
            case "router":
                from .router import Router

                return Router(config)
            case "linux":
                from .linux import Linux

                return Linux(config)
            case _:
                raise NotImplementedError(f"Device type {device_model} not implemented")
