from drivers.huawei_driver import HuaweiDriver

driver = HuaweiDriver(
    host="172.29.1.59",
    username="defutz",
    password="Avchi-s@d1k123.",
)

driver.connect()

version = driver.get_version()
print(version)

driver.disconnect()
