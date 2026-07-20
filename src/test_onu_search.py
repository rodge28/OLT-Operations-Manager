from services.onu_service import ONUService

service = ONUService()

olt, output = service.search_all(
    "48575443E1638DB1"
)

if olt:

    print("=" * 60)
    print("FOUND!")
    print("=" * 60)

    print(olt.hostname)
    print(output)

else:

    print("ONU not found.")
