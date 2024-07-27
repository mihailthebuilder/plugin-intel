import requests


def main():
    res = requests.get(
        "https://workspace.google.com/marketplace/category/intelligent-apps"
    )
    print(res.text)


if __name__ == "__main__":
    main()
