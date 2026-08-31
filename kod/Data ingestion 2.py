import requests
from datetime import datetime
import logging
import os
from config import ticker
from kafka import KafkaProducer
from json import dumps
from kafka.errors import KafkaError
# import boto3
print(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logging.basicConfig(
    filename = os.path.join(BASE_DIR, "companies", "errors.log"),
    level = logging.ERROR,
    format = "%(asctime)s - %(levelname)s - %(message)s",
    encoding = "utf-8"
)
BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP", "13.63.105.190:9092")
try:
    producer = KafkaProducer(
        bootstrap_servers=[BOOTSTRAP],
        value_serializer=lambda x: dumps(x).encode('utf-8')
)
except KafkaError:
    logging.error(f"Wystąpił błąd przy pobieraniu danych spółki.")
    producer = None


for tick in ticker:
    dane = {}                        
    try:                              
        with open(os.path.join(BASE_DIR, "companies", f"{tick}.txt"), "r", encoding="utf-8") as plik:
            for linia in plik:
                linia = linia.strip()
                if linia:
                    data_str, cena_str = linia.split(", ")
                    try:
                        dane[data_str] = float(cena_str)
                    except ValueError:
                        pass
    except FileNotFoundError:
        pass
    stare_daty = set(dane.keys())
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
            for t, c in con:
                if t and c is not None:
                    data = datetime.fromtimestamp(t)
                    dane[str(data)] = c
            posortowane = sorted(dane.keys())
            nowe_daty = set(dane.keys()) - stare_daty
            for data in nowe_daty:
                if producer is not None:
                    producer.send('gpw_tracker', value={"spółka":f"{tick}", "data": data, "cena": dane[data]})
            with open(os.path.join(BASE_DIR, "companies", f"{tick}.txt"), "w", encoding = "utf-8") as plik:
                for data in posortowane:
                    plik.write(f"{data}, {dane[data]}\n")
        else:
            logging.error(f"Wystąpił błąd przy pobieraniu danych spółki {tick}. Status błędu: {response.status_code}")
    except (requests.exceptions.RequestException, TypeError, KeyError):
        logging.error(f"Wystąpił błąd przy pobieraniu danych spółki {tick}")
if producer is not None:
    producer.flush()

# s3 = boto3.client("s3")
# for tick in ticker:
#     path = os.path.join(BASE_DIR, "companies", f"{tick}.txt")
#     s3.upload_file(path, "gpw-tracker-bucket", f"bronze/spolka={tick}/{tick}.txt")