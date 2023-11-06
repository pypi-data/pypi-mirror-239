from enum import Enum


class PROTOCOL(Enum):
    SSH = "ssh"
    TELNET = "telnet"
    SERIAL = "serial"

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return super().__eq__(other)
