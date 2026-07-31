import requests
from datetime import datetime
import logging
import os
print(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ticker = ["CBF.WA", "XTB.WA", "SNT.WA"]
logging.basicConfig(
    filename = os.path.join(BASE_DIR, "companies", "errors.log"),
    level = logging.ERROR,
    format = "%(asctime)s - %(levelname)s - %(message)s"
)
for tick in ticker:
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{tick}"
        params = {"range": "3y", "interval": "1d"}
        headers = {"User-Agent": "Chrome/5.0"}
        response = requests.get(url, params = params, headers = headers)
        if response.status_code == 200:
            print(response.url)
            head = response.json()["chart"]["result"][0]
            timestamp = head["timestamp"]
            close = head["indicators"]["quote"][0]["close"]
            con = list(zip(timestamp, close))
            with open(os.path.join(BASE_DIR, "companies", f"{tick}.txt"), "w", encoding = "utf-8") as plik:
                for t, c in con:
                    data = datetime.fromtimestamp(t)
                    plik.write(f"{data}, {c}\n")
            for t, c in con:
                data = datetime.fromtimestamp(t)
                print(data, c)
        else:
            logging.error(f"Wystąpił błąd przy pobieraniu danych spółki {tick}. Status błędu: {response.status_code}")
    except (requests.exceptions.RequestException, TypeError, KeyError):
        logging.error(f"Wystąpił błąd przy pobieraniu danych spółki {tick}")
        