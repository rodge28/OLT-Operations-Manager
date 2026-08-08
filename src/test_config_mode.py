from drivers.huawei_driver import HuaweiDriver


driver = HuaweiDriver(
    host="172.29.1.35",
    username="root",
    password="admin123",
)

print("Connecting...")

driver.connect()

try:

    print("\nEntering configuration mode...")
    output = driver.shell.enter_config_mode()
    print(output)

    print("\nExiting configuration mode...")
    output = driver.shell.exit_config_mode()
    print(output)

finally:

    print("\nDisconnecting...")
    driver.disconnect()
