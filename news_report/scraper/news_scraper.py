import requests
from bs4 import BeautifulSoup

from news_report.scraper.scraper_constants import (
    OMNI_URL,
    SCRAPER_HEADERS,
    OMNI_CLUSTER_CONTAINER_CLASS,
    OMNI_HEADER_CLASS,
    OMNI_TEASER_CLASS,
    OMNI_TITLE_CLASS,
    OMNI_TIMESTAMP_CLASS,
    NO_HEADER_MSG,
    NO_TEXT_MSG,
    NO_TITLE_MSG,
    UNDEFINED_TIME_MSG,
)


def scrape_omni(output_path: str):

    # Fetch the page content
    response = requests.get(OMNI_URL, headers=SCRAPER_HEADERS)

    if response.status_code != 200:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all containers
    containers = soup.find_all("div", class_=OMNI_CLUSTER_CONTAINER_CLASS)

    with open(output_path, "w") as f:
        for container in containers:
            # Extract the title and text within each container
            container_header = container.find(class_=OMNI_HEADER_CLASS)
            container_header = (
                container_header.get_text(strip=True)
                if container_header
                else NO_HEADER_MSG
            )

            titles = container.find_all(class_=OMNI_TITLE_CLASS)
            teasters = container.find_all(class_=OMNI_TEASER_CLASS)
            timestamps = container.find_all(class_=OMNI_TIMESTAMP_CLASS)

            title_texts = [
                title.get_text(strip=True) if title else NO_TITLE_MSG
                for title in titles
            ]
            teaser_texts = [
                text.get_text(strip=True) if text else NO_TEXT_MSG for text in teasters
            ]
            timestamps = [
                timestamp.get_text(strip=True) if timestamp else UNDEFINED_TIME_MSG
                for timestamp in timestamps
            ]

            if len(timestamps) == 0:
                continue

            f.write(f"Header: {container_header}\n")
            f.write("-" * 40 + "\n")
            for title_text, teaser_text, timestamp in zip(
                title_texts, teaser_texts, timestamps
            ):
                timestamp_pretty = (
                    timestamp + " sedan" if timestamp.endswith("tim") else timestamp
                )
                f.write(f"{title_text}     {timestamp_pretty}\n{teaser_text}\n")
                f.write("-" * 40 + "\n")
            f.write("\n")


if __name__ == "__main__":
    scrape_omni("test_scraper.txt")
