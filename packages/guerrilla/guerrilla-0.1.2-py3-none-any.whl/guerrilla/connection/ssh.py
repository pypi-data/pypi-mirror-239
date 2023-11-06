from dataclasses import dataclass, field
import paramiko
from guerrilla.connection.session import BaseSession
from guerrilla.logging import logger
from guerrilla.connection.channel import SSHChannel
from guerrilla.utils.exception import SSHAuthenticationError


@dataclass
class SSHSession(BaseSession):
    host: str = ""
    username: str = ""
    password: str = ""
    port: int = 22
    client: paramiko.SSHClient = field(default_factory=paramiko.SSHClient, init=False)
    channel: SSHChannel = field(init=False)

    def _is_alive(self) -> bool:
        """
        Checks if the SSH channel is still active.

        Returns:
        --------
        bool
            True if the channel is active, False otherwise.
        """
        transport = self.client.get_transport()
        return transport and transport.is_active()

    def _establish_connection(self):
        """
        Tries to connect to the remote server using SSH.
        """
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        logger.info(f"Created {self.name}'s SSH session to {self.host}:{self.port}")
        try:
            self.client.connect(
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
            )
        except paramiko.AuthenticationException as e:
            raise SSHAuthenticationError(e, self.host, self.port)
        except Exception:
            logger.error(f"Could not connect to {self.host}:{self.port}")
            raise ConnectionError("Could not connect to remote server")
        logger.success(f"Connected to {self.username} {self.host}:{self.port}")

        remote_conn = self.client.invoke_shell(width=511, height=1000)
        self.channel = SSHChannel(remote_conn)

    # def connect(self):
    #     """
    #     Connects to the remote server using SSH.
    #     """
    #     self._establish_connection()
    #     self._try_session_preparation()

    def disconnect(self):
        """
        Closes the SSH connection.
        """
        try:
            self.client.close()
            logger.info(f"Closed connection to {self.host}:{self.port}")
        except Exception:
            logger.error(f"Error when closing connection to {self.host}:{self.port}")
            raise ConnectionError("Could not close connection")
