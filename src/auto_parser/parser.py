from bs4 import BeautifulSoup


def parse_cars_from_html(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    result = []

    for car_block in soup.select("a.search__car"):
        name = car_block.select_one(".car_name")
        if name:
            result.append(name.get_text(strip=True))

    return result
