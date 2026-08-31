from kafka import KafkaConsumer
from json import loads, dumps
from datetime import datetime
import boto3
from config import ticker
import os
BOOTSTRAP = os.environ.get("KAFKA_BOOTSTRAP", "13.63.105.190:9092")
consumer = KafkaConsumer(
    bootstrap_servers=[BOOTSTRAP],
    group_id='gpw_consumer',
    auto_offset_reset='latest',
    value_deserializer=lambda x: loads(x.decode('utf-8')),
    consumer_timeout_ms=5000
)
consumer.subscribe(["gpw_tracker"])
odebrane = {}
for wiadomosc in consumer:
    dane = wiadomosc.value
    tick = dane["spółka"]
    if tick not in odebrane:
        odebrane[tick] = []
    odebrane[tick].append(dane)
if odebrane:
    s3 = boto3.client("s3")
    for tick, wiadomosci in odebrane.items():
        zawartosc = "\n".join(dumps(w) for w in wiadomosci)
        nowy_plik = datetime.now().strftime(f"%Y-%m-%dT%H-%M-%S-{tick}") + ".json"
        s3.put_object(Bucket="gpw-tracker-bucket", Key=f"live/spolka={tick}/{nowy_plik}", Body=zawartosc.encode("utf-8"))
consumer.commit()
print(f"Odebrano {sum(len(w) for w in odebrane.values())} wiadomości")