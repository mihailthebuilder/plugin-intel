import requests
from bs4 import BeautifulSoup, ResultSet, Tag
from http import HTTPStatus
from dataclasses import dataclass
import csv

WORKSPACE_CATEGORY_BASE_URL = "https://workspace.google.com/marketplace/category"
WORKSPACE_CATEGORIES = [
    "intelligent-apps",
    "work-from-everywhere",
    "business-essentials",
    "apps-to-discover",
    "google-apps",
    "popular-apps",
    "top-rated",
    "business-tools/accounting-and-finance",
    "business-tools/administration-and-management",
    "business-tools/erp-and-logistics",
    "business-tools/hr-and-legal",
    "business-tools/marketing-and-analytics",
    "business-tools/sales-and-crm",
    "productivity/creative-tools",
    "productivity/web-development",
    "productivity/office-applications",
    "productivity/task-management",
    "education/academic-resources",
    "education/teacher-and-admin-tools",
    "communication",
    "utilities",
]


@dataclass
class App:
    name: str
    developer: str
    description: str
    average_rating: int | None
    user_count: int
    url: str


def main():
    apps: dict[str, App] = {}

    for category in WORKSPACE_CATEGORIES:
        url = f"{WORKSPACE_CATEGORY_BASE_URL}/{category}"
        scrape_from_page(url, apps)

    with open("apps.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(
            file, delimiter=" ", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )

        for app in apps.values():
            writer.writerow(
                [
                    app.name,
                    app.developer,
                    app.description,
                    app.average_rating,
                    app.user_count,
                    app.url,
                ]
            )


def scrape_from_page(url: str, apps: dict[str, App]):
    try:
        res = requests.get(url)

        if res.status_code != HTTPStatus.OK:
            raise Exception(
                f"HTTP request for workspace results failed. Expected 200, got {res.status_code}: {res.text}"
            )

        soup = BeautifulSoup(res.text, features="html.parser")

        app_soups: ResultSet[Tag] = soup.find_all(
            lambda tag: tag.has_attr("data-card-index")
        )

        if len(app_soups) == 0:
            raise Exception("invalid HTML locator for entries")

        for app_soup in app_soups:
            extracted = extract_app(app_soup)
            apps[extracted.name] = extracted

    except Exception as e:
        e.add_note(f"url scraped: {url}")
        raise e


def extract_app(soup: Tag) -> App:
    name = soup.find("div", {"class": "M0atNd"})
    if name == None:
        raise Exception("invalid html locator for name")

    developer = soup.find("span", {"class": "y51Cnd"})
    if developer == None:
        raise Exception("invalid html locator for developer")

    description = soup.find("div", {"class": "BiEFEd"})
    if description == None:
        raise Exception("invalid html locator for description")

    anchorWithUrl = soup.find("a", {"class": "RwHvCd"})
    if anchorWithUrl == None:
        raise Exception("invalid html locator for url - can't find element")

    if type(anchorWithUrl) is not Tag:
        raise Exception("invalid html locator for url - can only find string")

    url = anchorWithUrl["href"]
    if url == None:
        raise Exception("invalid html locator for url - can't find valid href")

    if type(url) is not str:
        raise Exception(
            "invalid html locator for url - can't find valid href with type str"
        )

    averagerating_usercount_container: ResultSet[Tag] = soup.find_all(
        "span", {"class": "wUhZA"}
    )
    if (
        len(averagerating_usercount_container) > 2
        or len(averagerating_usercount_container) == 0
    ):
        raise Exception("invalid html locator for average rating and user count")

    usercount_string = averagerating_usercount_container[-1].text.strip()
    usercount = 0
    if usercount_string[-2:] == "K+":
        usercount = int(usercount_string.replace("K+", "")) * 1000
    if usercount_string[-2:] == "M+":
        usercount = int(usercount_string.replace("M+", "")) * 1000000

    app = App(
        name=name.text,
        developer=developer.text,
        description=description.text,
        user_count=usercount,
        average_rating=None,
        url=url,
    )

    if len(averagerating_usercount_container) == 2:
        averagerating = int(averagerating_usercount_container[0].text.replace(".", ""))
        app.average_rating = averagerating

    return app


def extract_path(url: str) -> str:
    parts = url.split("/")
    return "/".join(parts[-2:])


if __name__ == "__main__":
    main()
