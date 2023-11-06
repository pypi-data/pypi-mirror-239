from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Union, AnyStr
import paramiko


@dataclass
class Channel(ABC):
    remote_conn: Union[None, paramiko.Channel]
    encoding: str = "utf-8"

    @abstractmethod
    def read_buffer(self) -> str:
        """Single read of available data."""
        raise NotImplementedError

    @abstractmethod
    def read_channel(self) -> str:
        """Read all of the available data from the channel."""
        raise NotImplementedError

    @abstractmethod
    def write_channel(self, out_data: str) -> None:
        """Write data down the channel."""
        raise NotImplementedError

    @staticmethod
    def write_bytes(out_data: AnyStr, encoding: str = "utf-8") -> bytes:
        """Ensure output is properly encoded bytes."""
        if isinstance(out_data, str):
            return out_data.encode(encoding)
        elif isinstance(out_data, bytes):
            return out_data
        msg = f"Invalid value for out_data neither unicode nor byte string: {str(out_data)}"
        raise ValueError(msg)


class SSHChannel(Channel):
    def write_channel(self, out_data: str) -> None:
        if self.remote_conn is None:
            raise Exception("Attempt to write data, but there is no active channel.")
        self.remote_conn.sendall(self.write_bytes(out_data))

    def read_buffer(self) -> str:
        """Single read of available data."""
        if self.remote_conn is None:
            raise Exception("Attempt to read, but there is no active channel.")
        output = ""
        MAX_BUFFER = 32768
        if self.remote_conn.recv_ready():
            outbuf = self.remote_conn.recv(MAX_BUFFER)
            if len(outbuf) == 0:
                raise Exception("Channel stream closed by remote device.")
            output += outbuf.decode(self.encoding)
        return output

    def read_channel(self) -> str:
        """Read all of the available data from the channel."""
        if self.remote_conn is None:
            raise Exception("Attempt to read, but there is no active channel.")
        output = ""
        while True:
            new_output = self.read_buffer()
            output += new_output
            if new_output == "":
                break
        return output
