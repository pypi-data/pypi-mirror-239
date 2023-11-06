from guerrilla.device.base import BaseDevice
from guerrilla.device.router import Commands
from dataclasses import dataclass
import re
from guerrilla.logging import logger
from guerrilla.utils.decorator import log
from typing import override, Optional


class RouterShowMixin:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._add_show_methods()

    @classmethod
    def _add_show_methods(cls):
        def create_show_method(command):
            """Return a dynamically created method."""

            def method(self):
                return self.run(command)

            return method

        def process_enum(enum_obj, prefix=""):
            for cmd in enum_obj:
                method_suffix = cmd.name.lower()
                # If nested Enum, process it first
                if hasattr(cmd.value, "__members__"):
                    new_prefix = f"{method_suffix}_"
                    process_enum(cmd.value, new_prefix)
                elif isinstance(cmd.value, str):  # Direct command
                    method_name = f"show_{prefix}{method_suffix}"
                    setattr(cls, method_name, create_show_method(cmd.value))

        process_enum(Commands.SHOW)


@dataclass
class Router(BaseDevice, RouterShowMixin):
    @override
    def connect(self):
        super().connect()
        self.disable_paging()

    def disable_paging(
        self,
        command: str = "terminal length 0",
        cmd_verify: bool = False,
        pattern: Optional[str] = None,
    ) -> str:
        """Disable paging default to a CLI method.

        :param command: Device command to disable pagination of output

        :param delay_factor: Deprecated in Netmiko 4.x. Will be eliminated in Netmiko 5.

        :param cmd_verify: Verify command echo before proceeding (default: True).

        :param pattern: Pattern to terminate reading of channel
        """
        command = self.session.normalize_cmd(command)
        self.session.write_channel(command)
        # Make sure you read until you detect the command echo (avoid getting out of sync)
        if cmd_verify:
            output = self.session.read_until_pattern(
                pattern=re.escape(command.strip()), read_timeout=20
            )
        elif pattern:
            output = self.session.read_until_pattern(pattern=pattern, read_timeout=20)
        else:
            output = self.session.read_until_prompt()
        logger.info("Disable Paging Default")
        return output

    @log
    @override
    def run(
        self, command: str, expect_string: str = None, change_prompt: bool = False
    ) -> str:
        if change_prompt:
            result = self.session.run_timing(command)
            self.session.set_base_prompt()
        else:
            result = self.session.run(command, expect_string=expect_string)
        if "^Parse error" in result:
            logger.warning(f"Command '{command}' not accepted")
        return result
