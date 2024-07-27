import requests
from bs4 import BeautifulSoup
from http import HTTPStatus


def main():
    res = requests.get(
        "https://workspace.google.com/marketplace/category/intelligent-apps"
    )

    if res.status_code != HTTPStatus.OK:
        raise Exception(
            f"HTTP request for workspace results failed. Expected 200, got {res.status_code}: {res.text}"
        )

    soup = BeautifulSoup(res.text, features="html.parser")

    entries = soup.find_all(lambda tag: tag.has_attr("data-card-index"))

    if len(entries) == 0:
        raise Exception("Can't locate HTML element for entries")

    print(f"Found {len(entries)} addons")


if __name__ == "__main__":
    main()
