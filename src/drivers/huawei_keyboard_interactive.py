from typing import Any, List, Tuple

from numpy.strings import title
from paramiko import SSHClient, Transport
from netmiko.huawei.huawei import HuaweiSSH


class HuaweiInteractiveSSHClient(SSHClient):
    """
    SSHClient using keyboard-interactive authentication
    for Huawei MA5800.
    """

    def huawei_banner_handler(
        self,
        title: str,
        instructions: str,
        prompt_list: List[Tuple[str, bool]],
    ) -> List[str]:

        responses = []

        print(f"TITLE : {repr(title)}")
        print(f"INSTR : {repr(instructions)}")

        for i, (prompt, echo) in enumerate(prompt_list):

            print(f"Prompt {i}: {repr(prompt)}")
            print(f"Echo     : {echo}")

            if "password" in prompt.lower():
                responses.append(self.password)
            else:
                responses.append("")

        print(f"Password length: {len(self.password)}")
        print(f"Response lengths: {[len(r) for r in responses]}")

        return responses

    def _auth(self, username: str, password: str, *args: Any) -> None:

        print(">>> Keyboard-interactive authentication <<<")

        self.password = password

        transport = self.get_transport()
        assert isinstance(transport, Transport)

        transport.auth_interactive(
            username,
            handler=self.huawei_banner_handler,
        )

# ==========================================
# Step 4 starts here
# ==========================================

class HuaweiOLTSSH(HuaweiSSH):

    def _get_ssh_client_instance(self):
        print(">>> Using HuaweiInteractiveSSHClient <<<")
        return HuaweiInteractiveSSHClient()
