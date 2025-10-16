import datetime
import xml.etree.ElementTree as Et
from functools import lru_cache
from logging import getLogger

import requests

from messages.decorators import mute_exceptions

logger = getLogger("console")


@mute_exceptions
@lru_cache
def get_exchange_rates():
    currency_codes = [
        "R01239",
        "R01375",
        "R01235",
    ]

    row = "{name}/{short} - {value} руб."
    rows = ["Курсы валют, источник - Центробанк РФ.", ]

    date_str = datetime.datetime.now().strftime("%d/%m/%Y")
    res = requests.get(
        f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date_str}"
    )
    if res.ok:
        root = Et.fromstring(res.content)
        for i in root:
            if i.attrib.get("ID") in currency_codes:
                rows.append(row.format(
                    name=next(i.iter("Name")).text,
                    short=next(i.iter("CharCode")).text,
                    value=str(round(float(next(i.iter("Value")).text.replace(',', '.')), 2)),
                ))
    else:
        logger.warning(f"Status code is {res.status_code}")
    return rows





