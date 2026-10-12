# Notatka projektowa: naprawy 1 i 2 z przeglądu z 08.10 (12.10, do zatwierdzenia)

## Sedno w trzech zdaniach

1. Yahoo dla **wszystkich** spółek z GPW (nasze trzy, PKO BP, Orlen; Apple w porządku) podaje dobrą
   cenę tylko za dzień, w którym odpowiada. Wcześniejsze dni tygodnia mają zamknięcie z piątku sprzed
   tygodnia, a po weekendzie zły jest także ostatni dzień tygodnia. Poprawka przychodzi
   najwcześniej we wtorek, a najpóźniej w piątek rano następnego tygodnia.
2. Dziś to nie szkodzi, bo bieg o 18:00 wysyła tylko dzisiejszą świecę. Szkoda powstaje, gdy
   Producent **nadrabia** dzień z przeszłości (poprzedni bieg padł, Yahoo spóźniło się ze świecą).
   Wtedy do S3 idzie zła cena, a kontrola jej nie widzi.
3. Naprawa 1: Producent wysyła tylko dzisiejszą świecę, zaległe dni wstrzymuje i podnosi alarm,
   a nadrabia je człowiek, po sprawdzeniu z GPW. Naprawa 2: bez zapasowego adresu brokera, czyli brak
   `KAFKA_BOOTSTRAP` to głośny błąd.

## Co wiemy (stan 12.10)

| Kiedy | Co pokazało Yahoo |
|---|---|
| 03.09 | poniedziałek bieżącego tygodnia (31.08) z dobrą ceną — zjawiska jeszcze nie było |
| 08.10, 18:00 | 05–07.10 = zamknięcie z 02.10, 08.10 dobre |
| 09.10, rano | tydzień 28.09–02.10 dobry (poprawiony) |
| 09.10, 18:00 | 05–08.10 = zamknięcie z 02.10, 09.10 dobre |
| 11.10, 18:00 | **05–09.10** = zamknięcie z 02.10 (piątek 09.10 też zepsuty) |
| 12.10, po 13:21 i 18:00 | jak wyżej; 12.10 po 18:00: 200,0 / 355,0 / 135,9 (z GPW jeszcze nie porównane) |
| 12.10, po 18:52 | PKO BP i Orlen: to samo zjawisko; Apple: pięć różnych cen |

Czego nie wiemy: w który dzień przychodzi poprawka (odczyty pamięci wt–czw wieczorem) i jaka będzie
jutro cena za 12.10 (dzień wcześniejszy, ale z nowego tygodnia).

## Przykład na innych danych: lodziarnia i raport dostawcy

Dostawca co wieczór przysyła raport sprzedaży lodów za cały tydzień. Dobra jest tylko liczba
z dzisiaj; wcześniejsze dni tygodnia to kopia z zeszłego piątku (28 porcji), a poprawiony raport
przychodzi po kilku dniach. Lodziarnia przepisuje do księgi tylko dni, których jeszcze nie ma.

Zasada: **do księgi wpisuję tylko dzisiejszy dzień; dzień z przeszłości, którego nie ma w księdze,
wstrzymuję i dzwonię do szefa.**

| Dziś | Nowe dni w raporcie (liczby od dostawcy) | Do księgi | Wstrzymane | Alarm |
|---|---|---|---|---|
| wt 16.06 | 16.06: 41 | 16.06: 41 | — | nie |
| czw 18.06 (środowy wpis nie wyszedł) | 17.06: 28 (kopia, prawdziwie 39), 18.06: 44 | 18.06: 44 | 17.06 | **tak** |
| sob 20.06 (piątkowy wpis nie wyszedł) | 19.06: 28 (kopia, prawdziwie 37) | — | 19.06 | **tak** |
| nd 21.06 (oba dni dalej wstrzymane) | 17.06: 28, 19.06: 28 | — | 17.06, 19.06 | **tak** |
| wt 23.06, szef po sprawdzeniu w kasie: „nadrób” | 17.06: 39, 19.06: 37 (poprawione) | 17.06: 39, 19.06: 37 | — | nie |

Gdyby lodziarnia przepisywała wszystko, co nowe (jak dziś Producent), w księdze byłoby 17.06: 28
i 19.06: 28 — daty dobre, liczby złe, a nikt by tego nie zauważył.

| Przykład | Projekt |
|---|---|
| raport dostawcy | odpowiedź Yahoo (`range=3y`) |
| księga | Kafka → `live/` w S3 (i pamięć `companies/*.WA.txt` jako spis dni już wpisanych) |
| „dziś” | data polska, ta sama co w warunku sesji (`kod/session.py`) |
| wstrzymanie | daty nie idą do Kafki **i nie trafiają do pamięci**, więc jutro znów są „nowe” |
| telefon do szefa | linia w logu, na którą kontrola o 18:30 odpowiada alarmem (`/fail` u stróża) |
| „nadrób” po sprawdzeniu | ręczny bieg Producenta ze zmienną włączającą wysyłkę zaległych dni |

## Naprawa 1 — możliwości

- **(a) Tylko dzisiejsza świeca; zaległe wstrzymane z alarmem; nadrabianie ręczne po sprawdzeniu
  z GPW.** Rekomendacja Claude'a. Od 12.09 żaden bieg nie nadrabiał, więc alarm będzie rzadki,
  a człowiek i tak musi sprawdzić ceny. Koszt: zmiana w `data_ingestion.py` (podział dat, pamięć bez
  wstrzymanych dat, nowy dopisek w linii wyniku), w `control.py` (dopisek = awaria) i nowe testy.
  Luka w danych trwa do ręcznego nadrobienia, a stróż alarmuje codziennie, dopóki luka jest.
- **(b) Jak (a), ale zaległe dni nadrabiane same po 7 dniach.** Mniej ręcznej pracy. Ryzyko: znamy
  jeden tydzień obserwacji; jeśli Yahoo kiedyś poprawi później, zła cena przejdzie po cichu.
- **(c) Zaległe dni z drugiego źródła** (archiwum GPW albo inny serwis z notowaniami). Bez luki
  i bez ręcznej pracy, ale nowy kod, nowe źródło do nauki i nowe awarie. **Niesprawdzone**, czy
  i jak da się je pobrać. Do rozważenia, gdyby Yahoo zaczęło psuć także dzisiejszą świecę.
- **(d) Zostawić i opisać w README.** Bez pracy; ryzyko jak dziś: zła cena po każdym dniu z awarią.

## Naprawa 2 — zapasowy adres brokera

Dziś `data_ingestion.py:16` i `kafka_consumer.py:7` mają `os.environ.get("KAFKA_BOOTSTRAP",
"13.63.105.190:9092")`. Bieg z laptopa bez zmiennej łączy się z brokerem na EC2 i wysyła drugi raz
wszystko, czego nie ma w pamięci laptopa (kończy się na 01.09), także ze złymi cenami.

- **(a) Bez zapasowego adresu w obu plikach:** brak zmiennej = błąd z jasnym komunikatem na starcie.
  Rekomendacja Claude'a. Na EC2 nic się nie zmienia (`crontab` i ręczne biegi podają zmienną).
- **(b) Tylko w Producencie.** Konsument z laptopa nie ma powodu chodzić, ale gdyby chodził,
  zabrałby wiadomości z kolejki i zapisał je z laptopa.
- **(c) Zostawić i opisać.**

## Co może pójść źle (przy 1a i 2a)

- **Yahoo spóźni się z dzisiejszą świecą o 18:00** → jutro ten dzień jest zaległy → wstrzymany,
  alarm. Tak ma być: nie wiemy, jaką cenę Yahoo poda za niego jutro.
- **Czwarta spółka albo pierwszy zalew historii** → wszystkie dni zaległe → potrzebna zmienna
  „nadrób”; bieżący tydzień przed tym sprawdzić z GPW (w historii starszej niż tydzień ceny są dobre).
- **Zmienna „nadrób” zostawiona w `crontab` albo w oknie** → wysyłka bez sprawdzenia. Zmienna tylko
  przed komendą, nigdy w `crontab` (jak `KONTROLA_DATA`).
- **Zła strefa „dziś”** → ta sama funkcja daty co w warunku sesji, data polska.
- **Bieg dwa razy jednego dnia** → drugi bieg nie ma nowych dni → nic się nie dzieje.
- **Święto (11.11)** → brak świecy → nic nowego, bez alarmu od Producenta (fałszywy alarm kontroli
  z innego powodu zostaje, jak w terminach).
- **Brak `KAFKA_BOOTSTRAP` w `crontab`** (2a) → Producent i Konsument padają głośno, kontrola
  nie widzi `stan: zapisane` → `/fail` u stróża.
- **Yahoo zepsuje także dzisiejszą świecę** → naprawa tego nie złapie; to byłby sygnał do (c).

## Jak sprawdzimy

- Testy podziału dat: przypadki z tabeli lodziarni, przeniesione na daty bez spółek, wynik
  przewidziany przed uruchomieniem.
- Test kontroli: blok z dopiskiem o wstrzymanych dniach → awaria.
- Na EC2 pierwszy bieg `cron` po wdrożeniu: blok 28 linii, `nowych dni: 1, wysłane: 1` bez dopisku,
  liczby z tabeli przewidywań.
- Ścieżka wstrzymania na prawdziwej drodze: sposób do ustalenia w krokach po zatwierdzeniu
  (np. bieg na laptopie z udawaną datą „dziś”).

## Co to zmieni za miesiąc

Kompakcja i Gold bez zmian. Strona po wdrożeniu pokaże lukę zamiast złej ceny, dopóki ktoś nie
nadrobi dnia. README: ograniczenie „złe ceny Yahoo przy kilku nowych dniach” zmienia się w opis
wstrzymania i nadrabiania.

## Decyzje Gracjana (12.10 wieczorem) — notatka zatwierdzona

1. Naprawa 1: **(a)** tylko dzisiejsza świeca, zaległe dni wstrzymane z alarmem, nadrabianie ręczne
   po sprawdzeniu z GPW.
2. Naprawa 2: **(a)** bez zapasowego adresu w `data_ingestion.py` i `kafka_consumer.py`.
3. Kod **od jutra (13.10)**, z pełną instrukcją przed kodem (zasada 3). Odczyty pamięci wt–czw
   wieczorem idą równolegle (dzień poprawki Yahoo).

## Powiązane notatki

- [[Przeglad-2026-10-08-calosc]] — punkt 1.1, decyzje 1 i 2
- [[Notatka-2026-10-04-producent-przed-zamknieciem]] — warunek sesji (`kod/session.py`)
