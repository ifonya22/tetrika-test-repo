import csv
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

letters = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

total = {letter: 0 for letter in letters}

base_url = "https://ru.wikipedia.org/wiki/ Категория:Животные_по_алфавиту"


def beast_count():
    session = requests.Session()
    next_url = base_url

    while True:
        try:
            response = session.get(next_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

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
                                    else:
                                        break

            next_link = soup.find("a", text="Следующая страница")
            if not next_link or "href" not in next_link.attrs:
                break

            next_url = urljoin("https://ru.wikipedia.org", next_link["href"])
            print(next_url)
            print(total)
            time.sleep(0.5)

        except requests.RequestException as e:
            print(f"Ошибка сети: {e}")
            break
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            break


if __name__ == "__main__":
    try:
        beast_count()
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
    finally:
        with open("beasts.csv", "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["", "Количество"])
            for letter in letters:
                writer.writerow([letter, total[letter]])
