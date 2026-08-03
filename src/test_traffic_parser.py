from utils.traffic_table_parser import TrafficTableParser

with open("traffic_summary.txt", encoding="utf-8") as f:
    output = f.read()

print("========== FILE ==========")
print(output[:500])
print("==========================")

tables = TrafficTableParser.parse_summary(output)

print(f"Tables found: {len(tables)}")

for table in tables:
    print(table)
