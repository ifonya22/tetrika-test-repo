from urllib.parse import urljoin

import pytest
from bs4 import BeautifulSoup

from solution import LETTERS, get_next_url, parse_page

HTML_FIXTURE = """
<div class="mw-category-group">
  <h3>А</h3>
  <ul>
    <li><a href="/wiki/Акула" title="Акула">Акула</a></li>
    <li><a href="/wiki/Аист" title="Аист">Аист</a></li>
    <li><a href="/wiki/Ворона" title="Ворона">Ворона</a></li>
    <li><a href="/wiki/Tiger" title="Tiger">Tiger</a></li>
  </ul>
</div>
<a href="/wiki/Следующая_страница">Следующая страница</a>
"""


@pytest.fixture
def mock_total():
    return {letter: 0 for letter in "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"}


def test_parse_page(mock_total):
    soup = BeautifulSoup(HTML_FIXTURE, "html.parser")
    result = parse_page(soup, mock_total)
    assert result["А"] == 2
    assert result["Б"] == 0
    assert result["В"] == 1


def test_get_next_url():
    soup = BeautifulSoup(HTML_FIXTURE, "html.parser")
    next_url = get_next_url(soup)
    expected_url = urljoin("https://ru.wikipedia.org", "/wiki/Следующая_страница")
    assert next_url == expected_url


def test_get_next_url_no_link():
    empty_html = "<div>No links here</div>"
    soup = BeautifulSoup(empty_html, "html.parser")
    assert get_next_url(soup) is None


def test_parse_page2():
    html = """
    <div class="mw-category-group">
        <h3>А</h3>
        <ul>
            <li><a title="Акула"></a></li>
            <li><a title="Аист"></a></li>
        </ul>
    </div>
    <div class="mw-category-group">
        <h3>Б</h3>
        <ul>
            <li><a title="Бобр"></a></li>
        </ul>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    total = {letter: 0 for letter in LETTERS}
    result = parse_page(soup, total)

    assert result["А"] == 2
    assert result["Б"] == 1
    assert all(result[letter] == 0 for letter in "ВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")
