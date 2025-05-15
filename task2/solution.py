import csv
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

LETTERS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

base_url = "https://ru.wikipedia.org/wiki/ Категория:Животные_по_алфавиту"


def parse_page(soup: BeautifulSoup, total: dict[str, int]) -> dict[str, int]:
    for h3 in soup.find_all("h3"):
        current_letter = h3.get_text().strip()
        if current_letter in total:
            parent = h3.find_parent("div", class_="mw-category-group")
            if parent:
                for li in parent.find_all("li"):
                    a_tag = li.find("a")
                    if a_tag and a_tag.has_attr("title"):
                        title = a_tag["title"].strip()
                        if title:
                            first_letter = title[0].upper()
                            if first_letter in total:
                                total[first_letter] += 1
    return total


def get_next_url(soup: BeautifulSoup):
    next_link = soup.find("a", text="Следующая страница")
    return urljoin("https://ru.wikipedia.org", next_link["href"]) if next_link and "href" in next_link.attrs else None


def beast_count(total: dict[str, int]):
    session = requests.Session()
    next_url = base_url

    while True:
        try:
            response = session.get(next_url)
            response.raise_for_status()
            soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")

            total = parse_page(soup, total)

            next_url = get_next_url(soup)
            print(next_url)
            print(total)
            print()
            time.sleep(0.5)

        except requests.RequestException as e:
            print(f"Ошибка сети: {e}")
            break
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            break


if __name__ == "__main__":
    total = {letter: 0 for letter in LETTERS}
    try:
        beast_count(total=total)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
    finally:
        with open("beasts.csv", "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["", "Количество"])
            for letter in LETTERS:
                writer.writerow([letter, total[letter]])
