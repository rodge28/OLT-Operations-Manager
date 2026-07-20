from drivers.huawei_driver import HuaweiDriver

driver = HuaweiDriver(
    "172.29.1.59",
    "root",
    "admin123"
)

try:
    print("Connecting...")
    driver.connect()
    print("SUCCESS")
finally:
    driver.disconnect()
