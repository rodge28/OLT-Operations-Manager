from drivers.huawei_driver import HuaweiDriver
from services.subscriber_service import SubscriberService

HOST = "172.29.1.59"
USERNAME = "defutz"
PASSWORD = "Avchi-s@d1k123."

SERIAL = "48575443DA250FB1"


def main():

    driver = HuaweiDriver(
        host=HOST,
        username=USERNAME,
        password=PASSWORD,
    )

    try:
        print("Connecting...")
        driver.connect()

        service = SubscriberService(driver)

        subscriber = service.find(SERIAL)

        print(subscriber)

    finally:
        print("Disconnecting...")
        driver.disconnect()


if __name__ == "__main__":
    main()
