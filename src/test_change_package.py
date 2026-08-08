from drivers.huawei_driver import HuaweiDriver


OLT_IP = "172.29.1.35"
USERNAME = "root"
PASSWORD = "admin123"

SERVICE_PORT = 12
NEW_PROFILE = "PRIVATE_FTTH-50Mb"


driver = HuaweiDriver(
    host=OLT_IP,
    username=USERNAME,
    password=PASSWORD,
)


print("Connecting...")
driver.connect()

try:

    print("\nChanging package...")
    result = driver.change_traffic_profile(
        service_port=SERVICE_PORT,
        profile_name=NEW_PROFILE,
    )

    print("Change result:", result)

    print("\nVerifying service-port...")
    output = driver.run(
        f"display service-port {SERVICE_PORT}"
    )

    print(output)

finally:

    print("\nDisconnecting...")
    driver.disconnect()
