from db.database import DatabaseManager
from services.olt_service import OLTService
from drivers.huawei_driver import HuaweiDriver
from utils.traffic_table_parser import TrafficTableParser

db = DatabaseManager()
session = db.get_session()

olt_service = OLTService(session)

# Change this if your master OLT is different
olt = olt_service.get_by_id(1)

driver = HuaweiDriver(
    host=olt.ip_address,
    username=olt.username,
    password=olt.password,
)

print("Connecting...")

driver.connect()

print("Downloading traffic table summary...")

output = driver.get_traffic_table_summary(500)

driver.disconnect()

tables = TrafficTableParser.parse_summary(output)

print(f"Found {len(tables)} traffic tables")

for table in tables:
    print(table)
