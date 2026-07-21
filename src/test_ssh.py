from drivers.huawei_driver import HuaweiDriver

driver = HuaweiDriver(
    host="172.29.1.59",
    username="defutz",
    password="Avchi-s@d1k123.",
)

driver.connect()

ont = driver.find_ont_by_serial("48575443DA250FB1")
print(ont)

driver.disconnect()
