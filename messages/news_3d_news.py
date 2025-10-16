import requests
from bs4 import BeautifulSoup

from messages.decorators import mute_exceptions

SITE_URL = 'https://3dnews.ru'


@mute_exceptions
def get_3dnews_news():
    rows = [f"Новости с сайта {SITE_URL}"]
    row = "{title} {url}"

    res = requests.get(SITE_URL, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")

    main_page = soup.find(attrs={"class": "mainpage"})

    left_col = main_page.find(attrs={"class": "lncol"})
    right_col = main_page.find(attrs={"class": "rncol"})

    for i in [
        *left_col.find_all("li", attrs={"class": "strong"}),
        *right_col.find_all("li", attrs={"class": "strong"}),
    ]:
        if isinstance(i, str):
            rows.append(i)
        else:
            rows.append(row.format(title=i.a.text, url=SITE_URL + i.a["href"]))

    return rows


