import re
import time
import paramiko

from drivers.huawei_keyboard_interactive import HuaweiInteractiveSSHClient


class HuaweiShell:
    """
    Huawei MA5800 interactive shell using Paramiko keyboard-interactive
    authentication.
    """

    #PROMPT_REGEX = re.compile(r".+[>#]\s*$", re.MULTILINE)

    def __init__(self, host, username, password, port=22):
        self.host = host
        self.username = username
        self.password = password
        self.port = port

        self.client = None
        self.channel = None

    # -------------------------------------------------
    # Connection
    # -------------------------------------------------

    def connect(self):
        self.client = HuaweiInteractiveSSHClient()
        self.client.set_missing_host_key_policy(
            paramiko.AutoAddPolicy()
        )

        self.client.connect(
            hostname=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            look_for_keys=False,
            allow_agent=False,
            timeout=20,
        )

        self.channel = self.client.invoke_shell()

        # Wait for CLI prompt
        self._read_until_prompt()

        # Disable Smart interaction
        self.send_command("undo smart")

    def disconnect(self):
        try:
            self.send_command("smart")
        except Exception:
            pass

        try:
            if self.channel:
                self.channel.close()
        except Exception:
            pass

        try:
            if self.client:
                self.client.close()
        except Exception:
            pass

    # -------------------------------------------------
    # Commands
    # -------------------------------------------------

    def send_command(self, command):
        self._clear_buffer()

        self.channel.send(command + "\n")

        output = self._read_until_prompt()

        return self._clean_output(command, output)

    # -------------------------------------------------
    # Helpers
    # -------------------------------------------------

    def _clear_buffer(self):
        while self.channel.recv_ready():
            self.channel.recv(65535)

    def _read_until_prompt(self, timeout=60):

        output = ""
        start = time.time()

        while True:

            if self.channel.recv_ready():

                data = self.channel.recv(65535).decode(
                    "utf-8",
                    errors="ignore",
                )

                print(repr(data))

                output += data

                # Huawei pager
                if "---- More" in data:
                    self.channel.send(" ")
                    continue

                # Huawei prompt
                if output.rstrip().endswith(">"):
                    return output

            if time.time() - start > timeout:
                raise TimeoutError(output)

            time.sleep(0.05)

    def _clean_output(self, command, output):
        """
        Remove command echo and prompt.
        """

        lines = output.splitlines()

        cleaned = []

        for line in lines:

            if line.strip() == command.strip():
                continue

           # if self.PROMPT_REGEX.match(line):
           #     continue

            cleaned.append(line)

        return "\n".join(cleaned).strip()
