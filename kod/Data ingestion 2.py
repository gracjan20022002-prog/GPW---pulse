import requests
from datetime import datetime
ticker = ["CBF.WA", "XTB.WA", "SNT.WA"]
for tick in ticker:
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{tick}"
    print(url)
    params = {"range": "3y", "interval": "1d"}
    headers = {"User-Agent": "Chrome/5.0"}
    response = requests.get(url, params = params, headers = headers)
    print(response.url)
    head = response.json()["chart"]["result"][0]
    timestamp = head["timestamp"]
    close = head["indicators"]["quote"][0]["close"]
    con = list(zip(timestamp, close))
    with open(f"{tick}.txt", "w", encoding = "utf-8") as plik:
        for t, c in con:
            data = datetime.fromtimestamp(t)
            plik.write(f"{data}, {c}\n")
    for t, c in con:
        data = datetime.fromtimestamp(t)
        print(data, c)
        