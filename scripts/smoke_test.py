import requests


def main():
    r = requests.get("https://httpbin.org/get", timeout=5)
    print("status:", r.status_code)


if __name__ == "__main__":
    main()
