from guerrilla.device.base import BaseDevice
from dataclasses import dataclass
from guerrilla.device.linux import Commands
from typing import List, override, Optional
import re

LINUX_PROMPT_PRI = "$"
LINUX_PROMPT_ALT = "#"
LINUX_PROMPT_ROOT = "#"


@dataclass
class Linux(BaseDevice):
    prompt_pattern: str = (
        rf"[{re.escape(LINUX_PROMPT_PRI)}{re.escape(LINUX_PROMPT_ALT)}]"
    )

    @override
    def session_preparation(self):
        """Prepare the session after the connection has been established."""
        self.session.ansi_escape_codes = True
        self.session._test_channel_read(pattern=self.prompt_pattern)
        self.session.set_base_prompt()

    @override
    def find_prompt(
        self, delay_factor: float = 1.0, pattern: Optional[str] = None
    ) -> str:
        if pattern is None:
            pattern = self.prompt_pattern
        return self.session.find_prompt(delay_factor=delay_factor, pattern=pattern)

    def flush_ip(self, dev: str) -> None:
        self.run(Commands.FLUSH_IP(dev))

    def set_networks(self, dev: str, ip: List[str], mask: List[str]) -> None:
        self.flush_ip(dev)
        self.run_timing(
            'echo "source-directory /etc/network/interfaces.d" > /etc/network/interfaces'
        )
        config = (
            f"auto {dev}\niface {dev} inet static\naddress {ip[0]}\nnetmask {mask[0]}"
        )
        self.run_timing(f'echo "{config}" > /etc/network/interfaces.d/{dev}')
        for i in range(1, len(ip)):
            self.run_timing(
                f'echo "up ip addr add {ip[i]}/{mask[i]} dev {dev}" >> /etc/network/interfaces.d/{dev}'
            )
