from netmiko import ConnectHandler

device = {
    "device_type": "huawei",
    "host": "172.29.1.18",
    "username": "root",
    "password": "admin123",
    "port": 22,

    # Password authentication only
    "use_keys": False,
    "allow_agent": False,
    "fast_cli": False,

    # Don't use system known_hosts
    "system_host_keys": False,
    "alt_host_keys": False,
}

try:
    print("Connecting...")

    conn = ConnectHandler(**device)

    print("Connected!")

    output = conn.send_command(
        "display version",
        expect_string=r"[>#\]",
        read_timeout=60
    )

    print(output)

    conn.disconnect()

except Exception as e:
    print("\n========== ERROR ==========")
    print(type(e).__name__)
    print(e)
