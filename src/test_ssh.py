from drivers.huawei_driver import HuaweiDriver
from utils.version_parser import VersionParser

driver = HuaweiDriver(
    host="172.29.1.35",
    username="root",
    password="admin123"
)

driver.connect()

output = driver.find_ont_by_serial("485754438CC852AB")

print(output)

driver.disconnect()
