import requests
headers = {"User-Agent": "Chrome/5.0"}
adres = "https://query1.finance.yahoo.com/v8/finance/chart/CBF.WA?range=5d&interval=1d"
response = requests.get(adres, headers = headers)
print(response.json())

from datetime import datetime
# liczba = 150
# data = datetime.fromtimestamp(liczba)
head = response.json()["chart"]["result"][0]
close = head["indicators"]["quote"][0]["close"]
timestamp = head["timestamp"]
for t, c in zip(timestamp, close):
    data = datetime.fromtimestamp(t)
    print(data, c)
    
print(type(response.json()))
print(response.json().keys())
print(type(response.json()["chart"]))
print(response.json()["chart"].keys())
print(type(response.json()["chart"]['result']))
print(len(response.json()["chart"]['result']))
print(type(response.json()["chart"]['result'][0]))
print(response.json()["chart"]['result'][0].keys())
print(response.json()["chart"]['result'][0]["indicators"].keys())
# print(type(response.json()["chart"]['result'][0]["indicators"]))
# print(response.json()["chart"]['result'][0]["indicators"].keys())
# print(type(response.json()["chart"]['result'][0]["indicators"]["quote"]))
# print(len(response.json()["chart"]['result'][0]["indicators"]["quote"]))
# print(len(response.json()["chart"]['result'][0]["indicators"]["quote"][0]))
# print(type(response.json()["chart"]['result'][0]["indicators"]["quote"][0]))
# print(response.json()["chart"]['result'][0]["indicators"]["quote"][0].keys())
# print(len(response.json()["chart"]['result'][0]["indicators"]["quote"][0]["close"]))