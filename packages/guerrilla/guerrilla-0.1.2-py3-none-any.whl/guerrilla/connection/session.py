from guerrilla.connection.channel import SSHChannel
from guerrilla.utils.globals import PROTOCOL


from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Union, Any, Callable, TypeVar, cast, Optional, Tuple
import time
import re
from functools import wraps
from threading import Lock
from guerrilla.logging import logger
from guerrilla.utils.parser import structured_data_converter
from typing import List, Optional, Union, Dict, Any, Deque
from collections import deque


# For decorators
F = TypeVar("F", bound=Callable[..., Any])


def lock_channel(func: F) -> F:
    @wraps(func)
    def wrapper_decorator(self: "BaseSession", *args: Any, **kwargs: Any) -> Any:
        self._lock_session()
        try:
            return_val = func(self, *args, **kwargs)
        finally:
            # Always unlock the channel, even on exception.
            self._unlock_session()
        return return_val

    return cast(F, wrapper_decorator)


@dataclass
class BaseSession(ABC):
    """
    Base class for all session types.

    Attributes:
    -----------
    protocol : str
        The protocol used to connect to the device.
    """

    protocol: str = ""
    name: str = ""
    type: str = ""
    channel: Union[None, SSHChannel] = field(init=False)

    RETURN: str = "\n"
    fast_cli: bool = True
    global_delay_factor: float = 1.0
    _locker: Lock = Lock()
    session_timeout: int = 60
    disable_lf_normalization: bool = False
    response_return: str = "\n"
    ansi_escape_codes: bool = False
    _read_buffer: str = ""

    def __del__(self):
        """
        Closes the SSH connection when the object is deleted.
        """
        self.disconnect()

    @property
    def status(self):
        """
        Returns the status of the session.

        Returns:
        --------
        str
            'connected' if the session is alive, 'disconnected' otherwise.
        """
        return "connected" if self._is_alive() else "disconnected"

    @abstractmethod
    def _is_alive(self) -> bool:
        """
        Abstract method to check if the session is alive.

        Returns:
        --------
        bool
            True if the session is alive, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def _establish_connection(self):
        """
        Abstract method to establish a connection to the device.
        """
        raise NotImplementedError

    @abstractmethod
    def disconnect(self):
        """
        Abstract method to disconnect from the device.
        """
        raise NotImplementedError

    def connect(self):
        """
        Abstract method to connect to the device.
        """
        self._establish_connection()
        self._try_session_preparation()

    def clear_buffer(
        self,
        backoff: bool = True,
        backoff_max: float = 3.0,
        delay_factor: Optional[float] = None,
    ) -> str:
        """Read any data available in the channel."""

        if delay_factor is None:
            delay_factor = self.global_delay_factor
        sleep_time = 0.1 * delay_factor

        output = ""
        for _ in range(10):
            time.sleep(sleep_time)
            data = self.read_channel()
            data = self.strip_ansi_escape_codes(data)
            output += data
            if not data:
                break
            # Double sleep time each time we detect data
            logger.debug("Clear buffer detects data in the channel")
            if backoff:
                sleep_time *= 2
                sleep_time = backoff_max if sleep_time >= backoff_max else sleep_time
        return output

    def find_prompt(
        self, delay_factor: float = 1.0, pattern: Optional[str] = None
    ) -> str:
        """Finds the current network device prompt, last line only.

        :param delay_factor: See __init__: global_delay_factor
        :type delay_factor: int

        :param pattern: Regular expression pattern to determine whether prompt is valid
        """
        delay_factor = self.select_delay_factor(delay_factor)
        sleep_time = delay_factor * 0.25
        self.clear_buffer()
        self.write_channel(self.RETURN)

        if pattern is not None:
            prompt = self.read_until_pattern(pattern=pattern)
        else:
            # Initial read
            time.sleep(sleep_time)
            prompt = self.read_channel().strip()
            logger.info(prompt)
            count = 0
            while count <= 12 and not prompt:
                if not prompt:
                    self.write_channel(self.RETURN)
                    time.sleep(sleep_time)
                    prompt = self.read_channel().strip()
                    if sleep_time <= 3:
                        # Double the sleep_time when it is small
                        sleep_time *= 2
                    else:
                        sleep_time += 1
                count += 1

        # If multiple lines in the output take the last line
        prompt = prompt.split(self.response_return)[-1]
        prompt = prompt.strip()
        self.clear_buffer()
        if not prompt:
            raise ValueError(f"Unable to find prompt: {prompt}")
        logger.debug(f"[find_prompt()]: prompt is {prompt}")
        return prompt

    def _timeout_exceeded(self, start: float, msg: str = "Timeout exceeded!") -> bool:
        """Raise NetmikoTimeoutException if waiting too much in the serving queue.

        :param start: Initial start time to see if session lock timeout has been exceeded
        :type start: float (from time.time() call i.e. epoch time)

        :param msg: Exception message if timeout was exceeded
        :type msg: str
        """
        if not start:
            # Must provide a comparison time
            return False
        if time.time() - start > self.session_timeout:
            # session_timeout exceeded
            raise TimeoutError(msg)
        return False

    def _lock_session(self, start: Optional[float] = None) -> bool:
        """Try to acquire the Netmiko session lock. If not available, wait in the queue until
        the channel is available again.

        :param start: Initial start time to measure the session timeout
        :type start: float (from time.time() call i.e. epoch time)
        """
        if not start:
            start = time.time()
        # Wait here until the SSH channel lock is acquired or until session_timeout exceeded
        while not self._locker.acquire(False) and not self._timeout_exceeded(
            start, "The channel is not available!"
        ):
            time.sleep(0.1)
        return True

    def _unlock_session(self) -> None:
        """
        Release the channel at the end of the task.
        """
        # if self._locker.locked():
        #     self._locker.release()
        return self._locker.release() if self._locker.locked() else None

    @lock_channel
    def write_channel(self, out_data: str) -> None:
        """Generic method that will write data out the channel.

        :param out_data: data to be written to the channel
        :type out_data: str
        """
        self.channel.write_channel(out_data)

    def normalize_linefeeds(self, a_string: str) -> str:
        """Convert `\r\r\n`,`\r\n`, `\n\r` to `\n.`

        :param a_string: A string that may have non-normalized line feeds
            i.e. output returned from device, or a device prompt
        :type a_string: str
        """
        newline = re.compile("(\r\r\r\n|\r\r\n|\r\n|\n\r)")
        a_string = newline.sub(self.response_return, a_string)
        if self.response_return == "\n":
            # Convert any remaining \r to \n
            return re.sub("\r", self.response_return, a_string)
        else:
            return a_string

    def strip_ansi_escape_codes(self, string_buffer: str) -> str:
        """
        Remove any ANSI (VT100) ESC codes from the output

        http://en.wikipedia.org/wiki/ANSI_escape_code

        Note: this does not capture ALL possible ANSI Escape Codes only the ones
        I have encountered

        Current codes that are filtered:
        ESC = '\x1b' or chr(27)
        ESC = is the escape character [^ in hex ('\x1b')
        ESC[24;27H   Position cursor
        ESC[?25h     Show the cursor
        ESC[E        Next line (HP does ESC-E)
        ESC[K        Erase line from cursor to the end of line
        ESC[2K       Erase entire line
        ESC[1;24r    Enable scrolling from start to row end
        ESC[?6l      Reset mode screen with options 640 x 200 monochrome (graphics)
        ESC[?7l      Disable line wrapping
        ESC[2J       Code erase display
        ESC[00;32m   Color Green (30 to 37 are different colors)
        ESC[6n       Get cursor position
        ESC[1D       Move cursor position leftward by x characters (1 in this case)
        ESC[9999B    Move cursor down N-lines (very large value is attempt to move to the
                     very bottom of the screen).

        HP ProCurve and Cisco SG300 require this (possible others).

        :param string_buffer: The string to be processed to remove ANSI escape codes
        :type string_buffer: str
        """  # noqa

        code_position_cursor = chr(27) + r"\[\d+;\d+H"
        code_show_cursor = chr(27) + r"\[\?25h"
        code_next_line = chr(27) + r"E"
        code_erase_line_end = chr(27) + r"\[K"
        code_erase_line = chr(27) + r"\[2K"
        code_erase_start_line = chr(27) + r"\[K"
        code_enable_scroll = chr(27) + r"\[\d+;\d+r"
        code_insert_line = chr(27) + r"\[(\d+)L"
        code_carriage_return = chr(27) + r"\[1M"
        code_disable_line_wrapping = chr(27) + r"\[\?7l"
        code_reset_mode_screen_options = chr(27) + r"\[\?\d+l"
        code_reset_graphics_mode = chr(27) + r"\[00m"
        code_erase_display = chr(27) + r"\[2J"
        code_erase_display_0 = chr(27) + r"\[J"
        code_graphics_mode = chr(27) + r"\[\dm"
        code_graphics_mode1 = chr(27) + r"\[\d\d;\d\dm"
        code_graphics_mode2 = chr(27) + r"\[\d\d;\d\d;\d\dm"
        code_graphics_mode3 = chr(27) + r"\[(3|4)\dm"
        code_graphics_mode4 = chr(27) + r"\[(9|10)[0-7]m"
        code_get_cursor_position = chr(27) + r"\[6n"
        code_cursor_position = chr(27) + r"\[m"
        code_attrs_off = chr(27) + r"\[0m"
        code_reverse = chr(27) + r"\[7m"
        code_cursor_left = chr(27) + r"\[\d+D"
        code_cursor_forward = chr(27) + r"\[\d*C"
        code_cursor_up = chr(27) + r"\[\d*A"
        code_cursor_down = chr(27) + r"\[\d*B"
        code_wrap_around = chr(27) + r"\[\?7h"
        code_bracketed_paste_mode = chr(27) + r"\[\?2004h"

        code_set = [
            code_position_cursor,
            code_show_cursor,
            code_erase_line,
            code_enable_scroll,
            code_erase_start_line,
            code_carriage_return,
            code_disable_line_wrapping,
            code_erase_line_end,
            code_reset_mode_screen_options,
            code_reset_graphics_mode,
            code_erase_display,
            code_graphics_mode,
            code_graphics_mode1,
            code_graphics_mode2,
            code_graphics_mode3,
            code_graphics_mode4,
            code_get_cursor_position,
            code_cursor_position,
            code_erase_display,
            code_erase_display_0,
            code_attrs_off,
            code_reverse,
            code_cursor_left,
            code_cursor_up,
            code_cursor_down,
            code_cursor_forward,
            code_wrap_around,
            code_bracketed_paste_mode,
        ]

        output = string_buffer
        for ansi_esc_code in code_set:
            output = re.sub(ansi_esc_code, "", output)

        # CODE_NEXT_LINE must substitute with return
        output = re.sub(code_next_line, self.RETURN, output)

        # Aruba and ProCurve switches can use code_insert_line for <enter>
        insert_line_match = re.search(code_insert_line, output)
        if insert_line_match:
            # Substitute each insert_line with a new <enter>
            count = int(insert_line_match.group(1))
            output = re.sub(code_insert_line, count * self.RETURN, output)

        return output

    @lock_channel
    def read_channel(self) -> str:
        """Generic handler that will read all the data from given channel."""
        new_data = self.channel.read_channel()

        if self.disable_lf_normalization is False:
            start = time.time()
            # Data blocks shouldn't end in '\r' (can cause problems with normalize_linefeeds)
            # Only do the extra read if '\n' exists in the output
            # this avoids devices that only use \r.
            while ("\n" in new_data) and (time.time() - start < 1.0):
                if new_data[-1] == "\r":
                    time.sleep(0.01)
                    new_data += self.channel.read_channel()
                else:
                    break
            new_data = self.normalize_linefeeds(new_data)

        if self.ansi_escape_codes:
            new_data = self.strip_ansi_escape_codes(new_data)
        logger.debug(f"read_channel: {new_data}")
        # if self.session_log:
        #     self.session_log.write(new_data)

        # If data had been previously saved to the buffer, the prepend it to output
        # do post read_channel so session_log/log doesn't record buffered data twice
        if self._read_buffer:
            output = self._read_buffer + new_data
            self._read_buffer = ""
        else:
            output = new_data
        return output

    def select_delay_factor(self, delay_factor: float) -> float:
        """
        Choose the greater of delay_factor or self.global_delay_factor (default).
        In fast_cli choose the lesser of delay_factor of self.global_delay_factor.

        :param delay_factor: See __init__: global_delay_factor
        :type delay_factor: int
        """
        if self.fast_cli:
            return (
                min(delay_factor, self.global_delay_factor)
                if delay_factor
                else self.global_delay_factor
            )
        else:
            return max(delay_factor, self.global_delay_factor)

    def read_until_pattern(
        self,
        pattern: str = "",
        read_timeout: float = 10.0,
        re_flags: int = 0,
    ) -> str:
        """Read channel until pattern is detected.

        Will return string up to and including pattern.

        Returns ReadTimeout if pattern not detected in read_timeout seconds.

        :param pattern: Regular expression pattern used to identify that reading is done.

        :param read_timeout: maximum time to wait looking for pattern. Will raise ReadTimeout.
            A read_timeout value of 0 will cause the loop to never timeout (i.e. it will keep
            reading indefinitely until pattern is detected.

        :param re_flags: regex flags used in conjunction with pattern (defaults to no flags).

        :param max_loops: Deprecated in Netmiko 4.x. Will be eliminated in Netmiko 5.
        """
        output = ""
        loop_delay = 0.01
        start_time = time.time()
        # if read_timeout == 0 or 0.0 keep reading indefinitely
        while (time.time() - start_time < read_timeout) or (not read_timeout):
            output += self.read_channel()
            if re.search(pattern, output, flags=re_flags):
                if "(" in pattern and "(?:" not in pattern:
                    msg = f"""
Parenthesis found in pattern.

pattern: {pattern}\n

This can be problemtic when used in read_until_pattern().

You should ensure that you use either non-capture groups i.e. '(?:' or that the
parenthesis completely wrap the pattern '(pattern)'"""
                    logger.debug(msg)
                results = re.split(pattern, output, maxsplit=1, flags=re_flags)

                # The string matched by pattern must be retained in the output string.
                # re.split will do this if capturing parenthesis are used.
                if len(results) == 2:
                    # no capturing parenthesis, convert and try again.
                    pattern = f"({pattern})"
                    results = re.split(pattern, output, maxsplit=1, flags=re_flags)

                if len(results) != 3:
                    # well, we tried
                    msg = f"""Unable to successfully split output based on pattern:
pattern={pattern}
output={repr(output)}
results={results}
"""
                    raise Exception(msg)

                # Process such that everything before and including pattern is return.
                # Everything else is retained in the _read_buffer
                output, match_str, buffer = results
                output = output + match_str
                if buffer:
                    self._read_buffer += buffer
                logger.debug(f"Pattern found: {pattern} {output}")
                return output
            time.sleep(loop_delay)

        msg = f"""\n\nPattern not detected: {repr(pattern)} in output.

Things you might try to fix this:
1. Adjust the regex pattern to better identify the terminating string. Note, in
many situations the pattern is automatically based on the network device's prompt.
2. Increase the read_timeout to a larger value.

You can also look at the Netmiko session_log or debug log for more information.\n\n"""
        raise TimeoutError(msg)

    def read_until_prompt(
        self,
        read_timeout: float = 10.0,
        read_entire_line: bool = False,
        re_flags: int = 0,
    ) -> str:
        """Read channel up to and including self.base_prompt."""
        pattern = re.escape(self.base_prompt)
        if read_entire_line:
            pattern = f"{pattern}.*"
        return self.read_until_pattern(
            pattern=pattern,
            re_flags=re_flags,
            read_timeout=read_timeout,
        )

    def read_channel_timing(
        self,
        last_read: float = 2.0,
        read_timeout: float = 30.0,
    ) -> str:
        """Read data on the channel based on timing delays.

        General pattern is keep reading until no new data is read.

        Once no new data is read wait `last_read` amount of time (one last read).
        As long as no new data, then return data.

        Setting `read_timeout` to zero will cause read_channel_timing to never expire based
        on an absolute timeout. It will only complete based on timeout based on there being
        no new data.

        :param last_read: Amount of time to wait before performing one last read (under the
            idea that we should be done reading at this point and there should be no new
            data).

        :param read_timeout: Absolute timer for how long Netmiko should keep reading data on
            the channel (waiting for there to be no new data). Will raise ReadTimeout if this
            timeout expires. A read_timeout value of 0 will cause the read-loop to never timeout
            (i.e. Netmiko will keep reading indefinitely until there is no new data and last_read
            passes).

        :param delay_factor: Deprecated in Netmiko 4.x. Will be eliminated in Netmiko 5.

        :param max_loops: Deprecated in Netmiko 4.x. Will be eliminated in Netmiko 5.
        """

        # Time to delay in each read loop
        loop_delay = 0.1
        channel_data = ""
        start_time = time.time()

        # Set read_timeout to 0 to never timeout
        while (time.time() - start_time < read_timeout) or (not read_timeout):
            time.sleep(loop_delay)
            new_data = self.read_channel()
            # gather new output
            if new_data:
                channel_data += new_data
            # if we have some output, but nothing new, then do the last read
            elif channel_data != "":
                # Make sure really done (i.e. no new data)
                time.sleep(last_read)
                new_data = self.read_channel()
                if not new_data:
                    break
                else:
                    channel_data += new_data
        else:
            msg = f"""\n
read_channel_timing's absolute timer expired.

The network device was continually outputting data for longer than {read_timeout}
seconds.

If this is expected i.e. the command you are executing is continually emitting
data for a long period of time, then you can set 'read_timeout=x' seconds. If
you want Netmiko to keep reading indefinitely (i.e. to only stop when there is
no new data), then you can set 'read_timeout=0'.

You can look at the Netmiko session_log or debug log for more information.

"""
            raise TimeoutError(msg)
        return channel_data

    def _test_channel_read(self, count: int = 40, pattern: str = "") -> str:
        """Try to read the channel (generally post login) verify you receive data back.

        :param count: the number of times to check the channel for data

        :param pattern: Regular expression pattern used to determine end of channel read
        """

        def _increment_delay(
            main_delay: float, increment: float = 1.1, maximum: int = 8
        ) -> float:
            """Increment sleep time to a maximum value."""
            return min(main_delay * increment, maximum)

        i = 0
        delay_factor = self.select_delay_factor(delay_factor=0)

        if pattern:
            return self.read_until_pattern(pattern=pattern, read_timeout=20)

        main_delay = delay_factor * 0.1
        time.sleep(main_delay * 10)
        new_data = ""
        while i <= count:
            new_data += self.read_channel_timing(read_timeout=20)
            if new_data:
                return new_data

            self.write_channel(self.RETURN)
            main_delay = _increment_delay(main_delay)
            time.sleep(main_delay)
            i += 1

        raise TimeoutError("Timed out waiting for data")

    def set_base_prompt(
        self,
        pri_prompt_terminator: str = "#",
        alt_prompt_terminator: str = ">",
        delay_factor: float = 1.0,
        pattern: Optional[str] = None,
    ) -> str:
        """Sets self.base_prompt

        Used as delimiter for stripping of trailing prompt in output.

        Should be set to something that is general and applies in multiple contexts. For Cisco
        devices this will be set to router hostname (i.e. prompt without > or #).

        This will be set on entering user exec or privileged exec on Cisco, but not when
        entering/exiting config mode.

        :param pri_prompt_terminator: Primary trailing delimiter for identifying a device prompt

        :param alt_prompt_terminator: Alternate trailing delimiter for identifying a device prompt

        :param delay_factor: See __init__: global_delay_factor

        :param pattern: Regular expression pattern to search for in find_prompt() call
        """
        if pattern is None:
            if pri_prompt_terminator and alt_prompt_terminator:
                pri_term = re.escape(pri_prompt_terminator)
                alt_term = re.escape(alt_prompt_terminator)
                pattern = rf"({pri_term}|{alt_term})"
            elif pri_prompt_terminator:
                pattern = re.escape(pri_prompt_terminator)
            elif alt_prompt_terminator:
                pattern = re.escape(alt_prompt_terminator)

        if pattern:
            prompt = self.find_prompt(delay_factor=delay_factor, pattern=pattern)
        else:
            prompt = self.find_prompt(delay_factor=delay_factor)

        if prompt[-1] not in (pri_prompt_terminator, alt_prompt_terminator):
            raise ValueError(f"Router prompt not found: {repr(prompt)}")

        # If all we have is the 'terminator' just use that :-(
        if len(prompt) == 1:
            self.base_prompt = prompt
        else:
            # Strip off trailing terminator
            self.base_prompt = prompt[:-1]
        logger.info(f"Default Prompt:{self.base_prompt}")

        return self.base_prompt

    def normalize_cmd(self, command: str) -> str:
        """Normalize CLI commands to have a single trailing newline.

        :param command: Command that may require line feed to be normalized
        :type command: str
        """
        command = command.rstrip()
        command += self.RETURN
        return command

    def set_terminal_width(
        self,
        command: str = "",
        cmd_verify: bool = False,
        pattern: Optional[str] = None,
    ) -> str:
        """CLI terminals try to automatically adjust the line based on the width of the terminal.
        This causes the output to get distorted when accessed programmatically.

        Set terminal width to 511 which works on a broad set of devices.

        :param command: Command string to send to the device

        :param delay_factor: Deprecated in Netmiko 4.x. Will be eliminated in Netmiko 5.
        """
        if not command:
            return ""
        command = self.normalize_cmd(command)
        self.write_channel(command)

        # Avoid cmd_verify here as terminal width must be set before doing cmd_verify
        if cmd_verify and self.global_cmd_verify is not False:
            output = self.read_until_pattern(pattern=re.escape(command.strip()))
        elif pattern:
            output = self.read_until_pattern(pattern=pattern)
        else:
            output = self.read_until_prompt()
        return output

    def session_preparation(self) -> None:
        """
        Prepare the session after the connection has been established

        This method handles some differences that occur between various devices
        early on in the session.

        In general, it should include:
        self._test_channel_read(pattern=r"some_pattern")
        self.set_base_prompt()
        self.set_terminal_width()
        self.disable_paging()
        """
        self._test_channel_read()
        self.set_base_prompt()
        self.set_terminal_width()
        # self.disable_paging()

    def _try_session_preparation(self, is_send_return: bool = True):
        try:
            if is_send_return:
                self.write_channel(self.RETURN)
                time.sleep(0.1)
            self.session_preparation()
        except Exception:
            self.disconnect()

    def _prompt_handler(self, auto_find_prompt: bool) -> str:
        if auto_find_prompt:
            try:
                prompt = self.find_prompt()
            except ValueError:
                prompt = self.base_prompt
        else:
            prompt = self.base_prompt
        return re.escape(prompt.strip())

    def command_echo_read(self, cmd: str, read_timeout: float) -> str:
        # Make sure you read until you detect the command echo (avoid getting out of sync)
        new_data = self.read_until_pattern(
            pattern=re.escape(cmd), read_timeout=read_timeout
        )

        # There can be echoed prompts that haven't been cleared before the cmd echo
        # this can later mess up the trailing prompt pattern detection. Clear this out.
        lines = new_data.split(cmd)
        if len(lines) == 2:
            # lines[-1] should realistically just be the null string
            new_data = f"{cmd}{lines[-1]}"
        else:
            # cmd exists in the output multiple times? Just retain the original output
            pass
        return new_data

    def _first_line_handler(self, data: str, search_pattern: str) -> Tuple[str, bool]:
        """
        In certain situations the first line will get repainted which causes a false
        match on the terminating pattern.

        Filter this out.

        returns a tuple of (data, first_line_processed)

        Where data is the original data potentially with the first line modified
        and the first_line_processed is a flag indicating that we have handled the
        first line.
        """
        try:
            # First line is the echo line containing the command. In certain situations
            # it gets repainted and needs filtered
            lines = data.split(self.RETURN)
            first_line = lines[0]
            BACKSPACE_CHAR = "\x08"
            if BACKSPACE_CHAR in first_line:
                pattern = search_pattern + r".*$"
                first_line = re.sub(pattern, repl="", string=first_line)
                lines[0] = first_line
                data = self.RETURN.join(lines)
            return (data, True)
        except IndexError:
            return (data, False)

    def strip_command(self, command_string: str, output: str) -> str:
        """
        Strip command_string from output string

        Cisco IOS adds backspaces into output for long commands (i.e. for commands that line wrap)

        :param command_string: The command string sent to the device
        :type command_string: str

        :param output: The returned output as a result of the command string sent to the device
        :type output: str
        """
        backspace_char = "\x08"

        # Check for line wrap (remove backspaces)
        if backspace_char in output:
            output = output.replace(backspace_char, "")

        # Juniper has a weird case where the echoed command will be " \n"
        # i.e. there is an extra space there.
        cmd = command_string.strip()
        if output.startswith(cmd):
            output_lines = output.split(self.response_return)
            new_output = output_lines[1:]
            return self.response_return.join(new_output)
        else:
            # command_string isn't there; do nothing
            return output

    def strip_prompt(self, a_string: str) -> str:
        """Strip the trailing router prompt from the output.

        :param a_string: Returned string from device
        :type a_string: str
        """
        response_list = a_string.split(self.response_return)
        last_line = response_list[-1]

        if self.base_prompt in last_line:
            return self.response_return.join(response_list[:-1])
        else:
            return a_string

    def _sanitize_output(
        self,
        output: str,
        strip_command: bool = False,
        command_string: Optional[str] = None,
        strip_prompt: bool = False,
    ) -> str:
        """Strip out command echo and trailing router prompt."""
        if strip_command and command_string:
            output = self.strip_command(command_string, output)
        if strip_prompt:
            output = self.strip_prompt(output)
        return output

    def run(
        self,
        command_string: str,
        expect_string: Optional[str] = None,
        read_timeout: float = 10.0,
        auto_find_prompt: bool = True,
        strip_prompt: bool = True,
        strip_command: bool = True,
        normalize: bool = True,
        use_textfsm: bool = False,
        textfsm_template: Optional[str] = None,
        cmd_verify: bool = True,
    ) -> Union[str, List[Any], Dict[str, Any]]:
        # Time to delay in each read loop
        loop_delay = 0.025

        if expect_string is not None:
            search_pattern = expect_string
        else:
            search_pattern = self._prompt_handler(auto_find_prompt)

        if normalize:
            command_string = self.normalize_cmd(command_string)

        # Start the clock
        start_time = time.time()
        self.write_channel(command_string)
        new_data = ""

        cmd = command_string.strip()
        if cmd and cmd_verify:
            new_data = self.command_echo_read(cmd=cmd, read_timeout=10)

        MAX_CHARS = 2_000_000
        DEQUE_SIZE = 20
        output = ""
        # Check only the past N-reads. This is for the case where the output is
        # very large (i.e. searching a very large string for a pattern a whole bunch of times)
        past_n_reads: Deque[str] = deque(maxlen=DEQUE_SIZE)
        first_line_processed = False

        # Keep reading data until search_pattern is found or until read_timeout
        while time.time() - start_time < read_timeout:
            if new_data:
                output += new_data
                past_n_reads.append(new_data)

                # Case where we haven't processed the first_line yet (there is a potential issue
                # in the first line (in cases where the line is repainted).
                if not first_line_processed:
                    output, first_line_processed = self._first_line_handler(
                        output, search_pattern
                    )
                    # Check if we have already found our pattern
                    if re.search(search_pattern, output):
                        break

                else:
                    if len(output) <= MAX_CHARS:
                        if re.search(search_pattern, output):
                            break
                    else:
                        # Switch to deque mode if output is greater than MAX_CHARS
                        # Check if pattern is in the past n reads
                        if re.search(search_pattern, "".join(past_n_reads)):
                            break

            time.sleep(loop_delay)
            new_data = self.read_channel()

        else:  # nobreak
            msg = f"""
Pattern not detected: {repr(search_pattern)} in output.

Things you might try to fix this:
1. Explicitly set your pattern using the expect_string argument.
2. Increase the read_timeout to a larger value.

"""
            raise TimeoutError(msg)

        output = self._sanitize_output(
            output,
            strip_command=strip_command,
            command_string=command_string,
            strip_prompt=strip_prompt,
        )
        return_val = structured_data_converter(
            command=command_string,
            raw_data=output,
            platform=self.protocol,
            use_textfsm=use_textfsm,
            textfsm_template=textfsm_template,
        )
        return return_val

    def run_timing(
        self,
        command_string: str,
        last_read: float = 2.0,
        read_timeout: float = 30.0,
        strip_prompt: bool = True,
        strip_command: bool = True,
        normalize: bool = True,
        use_textfsm: bool = False,
        textfsm_template: Optional[str] = None,
        cmd_verify: bool = False,
    ) -> Union[str, List[Any], Dict[str, Any]]:
        """
        Execute command_string on the SSH channel using a delay-based mechanism. Generally
        used for show commands.
        """
        output = ""
        new_data = ""
        if normalize:
            command_string = self.normalize_cmd(command_string)
        self.write_channel(command_string)

        cmd = command_string.strip()
        if cmd and cmd_verify:
            new_data = self.command_echo_read(cmd=cmd, read_timeout=10)
            output += new_data
        output += self.read_channel_timing(
            last_read=last_read, read_timeout=read_timeout
        )

        output = self._sanitize_output(
            output,
            strip_command=strip_command,
            command_string=command_string,
            strip_prompt=strip_prompt,
        )
        return_data = structured_data_converter(
            command=command_string,
            raw_data=output,
            platform=self.type,
            use_textfsm=use_textfsm,
            textfsm_template=textfsm_template,
        )
        return return_data


@dataclass
class Session:
    """
    Session class for managing sessions.
    """

    config: dict

    def __new__(cls, config: dict):
        """
        Create a new session based on the protocol.
        """
        protocol = config.get("protocol", None)
        match protocol:
            case PROTOCOL.SSH:
                from guerrilla.connection.ssh import SSHSession

                return SSHSession(**config)
            case _:
                raise ValueError(f"Invalid protocol: {protocol}")
