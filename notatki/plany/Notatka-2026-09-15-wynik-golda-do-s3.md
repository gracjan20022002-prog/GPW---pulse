# Notatka projektowa — wynik Golda do S3 i Atheny

Napisana 15 września 2026, przed kodem. **Status: zatwierdzona 15 września.**
Wszystkie pięć decyzji zgodnie z rekomendacją: nadpisywać, CSV, przełącznik
tylko na EC2, tabele ręcznie, bez kolumny z godziną obliczenia. Przed kodem
sprawdzamy dwie rzeczy z części „Niesprawdzone": uprawnienia i folder `gold/`
w S3.

**Stan 16 września wieczorem:** uprawnienia sprawdzone, kod napisany, test
bez przełącznika i jednorazowa wysyłka z laptopa zgodne z przewidywaniami,
**tabele w Athenie założone i sprawdzone** (szczegóły niżej). **Nie ma
jeszcze:** kodu na EC2, zmiennej `GOLD_DO_S3=1` w `crontab`, głośnej
awarii. Zostało wdrożenie na EC2.

To piąta naprawa z kolejności ustalonej 8 września (przegląd, część 5):
„Wynik Golda do S3 i do Atheny".

---

## Sedno w trzech zdaniach

Gold co wieczór liczy ranking i dane dzienne, ale zapisuje je **tylko na
dysku EC2**, a tam nikt ich nie zobaczy bez SSH. Po zmianie Gold po zapisie
na dysk **wyśle te same dwa pliki do S3**, zawsze pod tą samą nazwą, więc
nowy wynik zastąpi wczorajszy. W Athenie **raz** założymy dwie tabele, które
czytają te pliki. Od tej chwili wynik da się odczytać zapytaniem SQL,
a później także w Power BI albo na stronie.

---

## Na innym przykładzie: ranking lodów na wystawie

**Wejście.** Kucharz co wieczór liczy sprzedaż i wpisuje ją do zeszytu na
zapleczu. Zeszyt to plik `ranking_lodow.csv` na dysku:

```
smak,sprzedane
waniliowe,40
czekoladowe,35
```

Klienci zeszytu nie widzą.

**Zmiana:**
- kucharz przepisuje kartkę na szybę wystawy, zawsze do tej samej ramki,
  i zdejmuje wczorajszą kartkę;
- w katalogu lodziarni leży karta z opisem: „ranking wisi w ramce
  `wyniki/ranking_lodow/`, dwie kolumny: `smak` (tekst) i `sprzedane`
  (liczba), pierwsza linijka to nagłówek".

**Wyjście. Dzień 1**, zapytanie `SELECT * FROM ranking_lodow`:

| smak | sprzedane |
|---|---|
| waniliowe | 40 |
| czekoladowe | 35 |

**Dzień 2.** Kucharz powiesił w tej samej ramce nową kartkę:
`waniliowe 42`, `czekoladowe 50`. To samo zapytanie zwraca **2 wiersze
z nowymi liczbami, a nie 4**:

| smak | sprzedane |
|---|---|
| waniliowe | 42 |
| czekoladowe | 50 |

**Co psuje obraz.** Ktoś zostawił w ramce drugą kartkę,
`ranking_lodow_kopia.csv`. Zapytanie zwraca **4 wiersze** i nie pokazuje
żadnego błędu. Tabela czyta **wszystko, co leży w jej folderze**.

---

## Jak to wygląda u nas

| Lodziarnia | Nasz projekt |
|---|---|
| zeszyt na zapleczu | `gold/ranking.csv` i `gold/dane_dzienne.csv` na dysku EC2 |
| szyba wystawy | bucket S3 `gpw-tracker-bucket` |
| ramka na szybie | folder w S3: `gold/ranking/` i `gold/dane_dzienne/` |
| zdjęcie wczorajszej kartki | nadpisanie pliku o tej samej nazwie |
| karta w katalogu | tabela w Athenie w bazie `gpw-tracker_db` |
| klient pyta o ranking | zapytanie SQL, później Power BI albo strona |

Dwa słowa, które tu wracają:
- **Folder w S3 to tylko początek nazwy pliku** (prefiks, z angielskiego
  *prefix*). `gold/ranking/ranking.csv` to jedna długa nazwa. `aws s3 ls`
  i Athena pokazują ją tak, jakby to były foldery.
- **Tabela w Athenie nie kopiuje danych.** To tylko opis: gdzie leżą pliki
  i jakie mają kolumny. Tak samo działają już tabele `bronze` i `live`.

---

## Co się zmienia, a czego nie ruszamy

**Zmienia się:**
- **`gold.py`.** Po zapisie dwóch plików na dysk wysyła oba do S3 i dopisuje
  do logu jedną linię. Do wysyłki służy `upload_file`, znane
  z `compaction.py`. Zapis na dysk zostaje bez zmian.
- **Athena.** Dochodzą dwie nowe tabele, założone raz, ręcznie.
- **`crontab` na EC2.** Dochodzi jedna linia, jeśli wybierzesz pierwszą
  możliwość w decyzji 3.
- **Blok jednego biegu w `errors.txt`.** ~~Jest o jedną linię dłuższy:
  w dzień giełdowy 24 → 25, bez nowych wiadomości 22 → 23.~~
  **Poprawka 15.09, pomyłka Claude'a:** dochodzą też **2 linie ostrzeżenia
  `boto3`**. Gold to osobny program, a ostrzeżenie o Pythonie 3.9 wypisuje
  każdy program, który tworzy klienta S3 (tak jak Konsument). **Decyzja
  Gracjana 15.09: jedna linia „wysłano" na każdy plik**, żeby przy awarii
  drugiej wysyłki było widać, że pierwszy plik dotarł. Razem **+4 linie**:
  w dzień giełdowy **24 → 28**, bez nowych wiadomości **22 → 26**. Bieg
  bez przełącznika (laptop) dopisuje jedną linię „pominięto".

**Nie ruszamy:**
- Producenta, Konsumenta ani Silvera;
- kompakcji. Kasuje tylko pliki, które zwraca zapytanie o tabelę `live`,
  więc `gold/` w S3 jest bezpieczne. Sprawdzone w `compaction.py`.

---

## Jak sprawdzimy

Liczby do porównania, zapisane przed biegiem:

| Co | Oczekiwane | Co to znaczy |
|---|---|---|
| linia w logu | napis „wysłano" przy obu plikach | Gold doszedł do końca |
| pliki w S3 | oba z datą dnia biegu | wynik jest świeży, a nie wczorajszy |
| rozmiar pliku w S3 | co do bajta taki jak na dysku EC2 | wysłany cały plik |
| `COUNT(*)` rankingu w Athenie | **3** | ani nagłówka w danych, ani drugiego pliku w folderze |
| `COUNT(*)` danych dziennych | tyle, ile Silver wypisał tego dnia (dziś `2316`) | Athena czyta cały plik |

Zła liczba i jej znaczenie:
- **4 w rankingu:** nagłówek czytany jako dane albo w folderze leży drugi
  plik;
- **wczorajsza data pliku w S3:** Gold nie wysłał wyniku.

---

## Co może pójść źle

- **Rola EC2 nie ma prawa zapisu do `gold/`.** W logu pojawi się
  `AccessDenied`, a wynik zostanie tylko na dysku. *Chroni:* sprawdzenie
  uprawnień przed kodem.
- **Pierwszy plik dotarł do S3, drugi nie.** Wtedy dzisiejsze dane dzienne
  leżą obok wczorajszego rankingu, a Athena nie zgłasza błędu. *Chroni:*
  daty obu plików w S3. Głośno zrobi się dopiero po naprawie „sygnał
  awarii".
- **Gold się nie uruchomi,** na przykład gdy padnie Silver. W S3 zostaje
  wczorajszy wynik, który wygląda na aktualny. *Chroni:* to samo, data
  pliku.
- **Drugi plik w folderze tabeli.** Każdy dodatkowy plik w `gold/ranking/`
  po cichu podwaja wiersze. *Chroni:* `COUNT(*)` = 3 i zasada, że do folderów
  tabel nic nie wgrywamy ręcznie.
- **Nagłówek czytany jako dane.** Bez ustawienia „pomiń pierwszą linię"
  tabela pokaże dodatkowy wiersz ze słowami `spolka`, `miesiac`. *Chroni:*
  ustawienie tabeli i `COUNT(*)`.
- **Kolumny w innej kolejności niż w tabeli.** Athena dopasowuje kolumny
  z pliku CSV po kolejności, a nie po nazwie. *Chroni:* zasada w `CLAUDE.md`
  i zapytanie kontrolne po każdej zmianie w Goldzie.
- **Laptop nadpisuje wynik z EC2.** Temu służy decyzja 3.
- **Gold odpala się dwa razy.** Ten sam plik zostaje nadpisany drugi raz
  i nic się nie dubluje. Ochrona niepotrzebna.
- **Dochodzi czwarta spółka.** Ranking ma wtedy 4 wiersze, a tabele zostają
  bez zmian. Liczba do porównania rośnie do 4.
- **Zła godzina biegu.** Nic nowego. Do S3 trafia dokładnie to, co dziś
  ląduje na dysku, razem ze znanymi wadami, na przykład ceną z trwającej
  sesji, gdy bieg jest przed 17:00.

---

## Co to zmieni za miesiąc

- **Przewidywania bloku w logu:** więcej linii, w tym 2 ostrzeżenia `boto3`
  (poprawka 15.09, patrz wyżej).
- **Każda zmiana kolumn w `gold.py`** (tak jak 12 września, kiedy doszły
  `miesiac` i `dni`) wymaga zmiany tabeli w Athenie w tej samej sesji.
  Inaczej wartości trafią pod złe nazwy bez żadnego błędu.
- **Wynik w S3 wygląda na świeży, nawet gdy Gold padnie.** Dopóki nie ma
  sygnału awarii, jedyną ochroną jest data pliku.
- **Koszt:** 157 KB w S3 i zapytania na tych 157 KB. Grosze.

---

## Decyzje do zatwierdzenia

1. **Nadpisywać jeden plik czy co dzień zapisywać nowy?**
   - *Nadpisywać:* Athena zawsze pokazuje ostatni bieg, bez partycji
     (podziału tabeli na foldery), nic nie rośnie. Minus: nie ma historii
     rankingu. Da się ją policzyć od nowa, bo surowe ceny zostają
     w `bronze` i `live`.
   - *Co dzień nowy plik:* jest historia. Minusy: dane dzienne rosną o około
     2300 wierszy dziennie, prawie same powtórki, każde zapytanie musi
     wybierać dzień, a partycje wymagają `MSCK REPAIR`.
   - **Polecam: nadpisywać.**
2. **CSV czy Parquet?**
   - *CSV:* pandas już dziś go zapisuje, a EC2 nie ma `pyarrow`.
   - *Parquet:* zgodny z `bronze`, typy kolumn zapisane w pliku. Minus:
     wymaga `pyarrow` na EC2 z Pythonem 3.9.
   - **Polecam: CSV.**
3. **Kto wysyła do S3?** Dziś Gold uruchamiają dwie maszyny: EC2 z `cron`
   i laptop z Harmonogramu, obie o 18:10.
   - *Przełącznik tylko na EC2:* zmienna środowiskowa w `crontab`, ten sam
     pomysł co `KAFKA_BOOTSTRAP` w Konsumencie. Laptop i ręczne testy nie
     dotykają S3, a Gold pisze w logu „wysłano" albo „pominięto". Minus: gdy
     zmienna zniknie z `crontab`, Gold po cichu przestanie wysyłać.
     Zobaczymy to tylko po dacie pliku.
   - *Każdy bieg wysyła:* bez zmian w `crontab`. Minusy: o 18:10 laptop
     i EC2 nadpisują ten sam plik i wygrywa ten, kto skończy później; do tego
     każdy ręczny bieg z niegotowym kodem trafia prosto do S3.
   - *Najpierw wyłączyć Harmonogram:* zmienia kolejność napraw i nie chroni
     przed ręcznymi biegami na laptopie.
   - **Polecam: przełącznik tylko na EC2.**
4. **Jak założyć tabele w Athenie?**
   - *Ręcznie,* poleceniem `CREATE EXTERNAL TABLE` z laptopa: kilkanaście
     linii SQL na tabelę, typy wybieramy sami i dokładnie wiemy, co tabela
     robi. Minus: nowe polecenie SQL do nauki.
   - *Crawler Glue,* czyli narzędzie, które samo przegląda pliki i zakłada
     tabelę; znane z 25 sierpnia. Minusy: sam zgaduje typy i nazwy,
     a trudniej sprawdzić, co zrobił.
   - **Polecam: ręcznie.**
5. **Kolumna z godziną obliczenia w obu plikach?**
   - *Plusy:* jedno zapytanie pokaże, czy oba pliki są z tego samego biegu.
     Strona i tak będzie potrzebować napisu „stan na".
   - *Minusy:* zmieniają się kolumny i wypis rankingu w logu, więc więcej
     zmian naraz.
   - **Polecam: nie teraz.** Datę sprawdzamy w S3, a do kolumny wracamy przy
     stronie.

---

## Sprawdzone 15 września przed kodem, wszystko zgodnie z przewidywaniem

| Co | Przewidziane | Wyszło |
|---|---|---|
| kto pyta z laptopa | `user/gpw-tracker-admin` | tak |
| podpięte polityki roli `gpw_tracker_ec2_role` | `AmazonS3FullAccess`, `AmazonAthenaFullAccess` | tak, obie, żadnej innej |
| polityki wpisane wprost w rolę | pusta lista | `[]` |
| polityka bucketa | brak (`NoSuchBucketPolicy`) | brak |
| `gold/` w S3 | 0 obiektów | `Total Objects: 0` |
| najwyższy poziom bucketa | `athena-results/`, `bronze/`, `live/` | te trzy, nic więcej |

Nic nie blokuje zapisu z EC2 do `gold/`. Dowodem, że zapis naprawdę
przechodzi, będzie dopiero pierwszy bieg Golda na EC2.

## Test 15 września na laptopie, bez przełącznika, około 17:50

| Co | Przewidziane | Wyszło |
|---|---|---|
| pierwsza linia | `(2313, 3)` | tak |
| tabela miesięczna | `114` i `108` | tak |
| ostatnia linia | napis „pominięto" | `S3: Pominięto, brak GOLD_DO_S3 == 1` |
| `git status` | tylko `kod/gold.py` i ta notatka, nic w `gold/` | tak |

Kod po zmianie liczy to samo co przed nią, a bez zmiennej nic nie wysyła.
**Wysyłka do S3 jeszcze niesprawdzona.**

**Pomyłka Claude'a:** krok „sprawdź, że przełącznika nie ma" podany jako
`echo %GOLD_DO_S3%`, czyli składnia cmd. Test szedł w PowerShellu, gdzie
ta komenda zawsze wypisuje sam napis i niczego nie sprawdza. W PowerShellu:
`echo $env:GOLD_DO_S3`, pusta linia = brak zmiennej. Brak przełącznika
i tak udowodniła ostatnia linia Golda.

## Wyjątek od decyzji 3: jednorazowa wysyłka z laptopa

Decyzja Gracjana 15 września po odczycie biegu: pierwsza prawdziwa wysyłka
idzie **z laptopa**, z przełącznikiem włączonym ręcznie w jednym oknie
PowerShella. Powód: błąd w kodzie wysyłki wyjdzie przed wdrożeniem na EC2,
a pliki w S3 pozwolą założyć tabele w Athenie. Do biegu EC2 z przełącznikiem
w S3 leżą pliki z laptopa, 15 września zgodne co do cyfry z EC2. Po teście
laptop wraca do zasady „nigdy nie wysyła".

Przewidywania: dwie linie `S3: wysłano …`, w S3 `gold/dane_dzienne/dane_dzienne.csv`
157240 bajtów i `gold/ranking/ranking.csv` 365 bajtów, razem 2 obiekty
i 157605 bajtów.

**Wykonane 15 września o 19:19 czasu polskiego:**

| Co | Przewidziane | Wyszło |
|---|---|---|
| S3 `gold/` przed | 0 obiektów | tak |
| Gold | `(2316, 3)`, `114` i `108`, dwie linie „wysłano" | tak |
| przełącznik po teście | usunięty, pusta linia | tak |
| S3 `gold/` po | 157240 + 365 = 157605 bajtów, 2 obiekty | tak, co do bajta |
| `git status` | 5 linii | **6**: doszła notatka z 14.09 |

**Pomyłka Claude'a:** przewidział 5 linii `git status`, zapominając, że sam
chwilę wcześniej dopisał wynik do notatki z 14.09.

**Przy okazji sprawdzone:** `aws s3 ls` na laptopie pokazuje godzinę
w czasie laptopa (polskim): `19:19:08`, a nie w UTC.

Wysyłka działa z laptopa. **Z EC2 jeszcze nie była uruchomiona.**

## Tabele w Athenie — założone 16 września

Ręcznie, poleceniem `CREATE EXTERNAL TABLE` z konsoli Atheny, w bazie
`gpw-tracker_db` w regionie `eu-north-1`.

| Tabela | Czyta folder | Kolumn |
|---|---|---|
| `gold_dane_dzienne` | `s3://gpw-tracker-bucket/gold/dane_dzienne/` | 5 |
| `gold_ranking_spolek` | `s3://gpw-tracker-bucket/gold/ranking/` | 7 |

Trzy decyzje przy zakładaniu:
1. **`data` jako `string`, nie `timestamp`** — spójnie z `bronze` i `live`.
2. **Nazwa zaczyna się od warstwy**, tak jak `bronze` i `live`. Nazwę
   rankingu Gracjan zmienił na `gold_ranking_spolek`.
3. **Konsola Atheny**, nie skrypt — dwa polecenia uruchamiane raz w życiu.

Sprawdzenie, wszystko zgodnie z przewidywaniem:

| Co | Oczekiwane | Wyszło |
|---|---|---|
| `COUNT(*)` danych dziennych | 2316 | 2316 |
| `COUNT(*)` rankingu | 3 | 3 |
| puste `zmiana_proc` | 3 wiersze, po `1` na spółkę | CBF.WA 1, SNT.WA 1, XTB.WA 1 |
| `Data scanned` | tyle, ile ważą pliki | 153.55 KB i 0.36 KB przy 157240 i 365 bajtach |

**Pusta komórka to `NULL`** — punkt z sekcji „Niesprawdzone" jest zamknięty.

`Data scanned` wyszło przy okazji jako darmowy dowód, że tabele czytają
dokładnie te pliki, które laptop wysłał 15.09.

## Niesprawdzone

- **Komplet kolumn na ekranie.** 16.09 oglądaliśmy `COUNT(*)`, kolumnę
  `spolka` i puste komórki. Jedno `SELECT *` na obu tabelach domknie sprawę.
- **Zapis z EC2.** Dowodem będzie dopiero pierwszy bieg Golda na EC2
  z przełącznikiem: pliki w S3 z datą tego dnia i `COUNT(*)`
  `gold_dane_dzienne` większy o liczbę nowych dni.

## Poza zakresem

- Silver do S3.
- Wyłączenie lokalnego Harmonogramu oraz `silver/` i `gold/` poza gitem.
  To następna naprawa w kolejności.
- Sygnał awarii.
- Strona.
