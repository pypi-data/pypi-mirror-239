class SSHAuthenticationError(Exception):
    def __init__(self, error_msg, host, port):
        self.error_msg = error_msg
        self.host = host
        self.port = port

    def __str__(self):
        return f"""TCP connection to device failed.

Common causes of this problem are:
1. Incorrect hostname or IP address.
2. Wrong TCP port.
3. Intermediate firewall blocking access.

Device settings:  {self.host}:{self.port}

{str(self.error_msg)}
"""
