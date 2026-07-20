class HuaweiSSHError(Exception):
    """Base Huawei SSH exception."""


class HuaweiAuthenticationError(HuaweiSSHError):
    """Authentication failed."""


class HuaweiConnectionError(HuaweiSSHError):
    """Cannot establish SSH connection."""


class HuaweiCommandError(HuaweiSSHError):
    """Command execution failed."""


class HuaweiTimeoutError(HuaweiSSHError):
    """SSH command timeout."""
