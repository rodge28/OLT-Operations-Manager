from pathlib import Path
import json


def load_config():
    config_file = Path("config.json")

    if not config_file.exists():
        raise FileNotFoundError("config.json not found")

    with config_file.open("r", encoding="utf-8") as file:
        return json.load(file)


def main():
    config = load_config()

    print("=" * 50)
    print(config["app_name"])
    print(f"Version: {config['version']}")
    print("=" * 50)
    print("Application started successfully.")


if __name__ == "__main__":
    main()
