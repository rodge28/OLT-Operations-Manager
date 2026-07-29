from drivers.huawei_driver import HuaweiDriver

driver = HuaweiDriver(
    host="YOUR_OLT_IP",
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
)

try:

    print("Connecting...")
    driver.connect()

    service_port = 201

    print("\nCurrent Profile")
    before = driver.get_service_port_details(service_port)
    print(before)

    print("\nChanging profile...")

    driver.change_traffic_profile(
        service_port,
        "PRIVATE_FTTH-999Mb"
    )

    print("\nReading again...")

    after = driver.get_service_port_details(service_port)
    print(after)

finally:

    print("Disconnecting...")
    driver.disconnect()
