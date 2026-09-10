# Notatka projektowa — sprzątanie kodu i konfiguracji (krok 4)

Data: 2026-09-10. Napisana **przed** jakąkolwiek edycją, do zatwierdzenia
przez Gracjana. Podstawa: przeczytane dziś od nowa wszystkie pliki
w `kod/`, `.gitignore`, `requirements.txt`, `.claude/settings.local.json`,
lista plików śledzonych przez gita i sekcje 2.1, 2.5, 2.6, 2.9, 2.10
przeglądu z 08.09. Żadna liczba poniżej nie jest z pamięci — każda
policzona dzisiaj.

To jest krok 4 z kolejności napraw zatwierdzonej 08.09. Stoi przed
„wynik Golda do S3" celowo: kolejny kawałek doda do tych plików nowy kod,
a jeśli wcześniej nie usuniemy martwego, to za tydzień nie będzie widać,
co jest nowe, a co leży tu od sierpnia i nikt tego nie uruchamia.

---

## Zasada na dzisiaj: EC2 czeka do jutra

Dziś o 18:00 czasu polskiego pierwszy raz uruchomi się nowa, połączona
linia `crontab`. Ten bieg jest **jedynym dowodem** dla kroku 3b i liczby
na niego zostały policzone wczoraj: `(2307, 3)` dwa razy, 769 wierszy
w plikach spółek, pozycja grupy 2336, a przed `Odebrano 3 wiadomości`
ścieżka i trzy adresy Yahoo.

Dwie z tych czterech liczb pochodzą z `print`-ów, których ta notatka
dotyczy. Gdyby nowy kod trafił na EC2 przed 18:00, wieczorny bieg
sprawdzałby dwie zmiany naraz i przy każdym odchyleniu nie wiedzielibyśmy,
czy zawinił `crontab`, czy sprzątanie.

**Dlatego: wszystkie dzisiejsze edycje zostają na Windowsie, commit
i `git push` też mogą być dziś, ale `git pull` na EC2 dopiero po
sprawdzeniu wieczornego biegu.** Do tego czasu EC2 pracuje na kodzie
sprzed sprzątania.

---

## Grupa 1 — martwy kod i pliki-śmieci

Nic z tej grupy nie zmienia zachowania żadnego działającego skryptu.
To jest kasowanie rzeczy, których Python i tak nie wykonuje.

| # | Gdzie | Co |
|---|---|---|
| 1.1 | `kod/data_ingestion.py` linia 9 | zakomentowany `# import boto3` |
| 1.2 | `kod/data_ingestion.py` linie 83–86 | zakomentowany blok wysyłki plików `.txt` do `bronze/` w S3 |
| 1.3 | `kod/silver.py` linie 26–35 | zakomentowana stara wersja Silvera, czytająca `companies/*.txt` zamiast Atheny |
| 1.4 | `kod/gold.py` linia 1 | komentarz o kolejności testu, odwołujący się do nazw plików nieistniejących od 01.09 |
| 1.5 | `kod/compaction.py` linie 44–46 | wczytanie `CBF.WA.parquet` z nazwą spółki wpisaną na sztywno i dwa `print` o kształcie i typach — rusztowanie z pisania kompakcji |
| 1.6 | `kod/pipeline.py`, `kod/pipeline.txt` | test Harmonogramu Windows z 12.08; zapisuje datę uruchomienia do pliku, którego nikt nie czyta. Ostatnie dwa wpisy w `pipeline.txt` są z 12.08 |
| 1.7 | `kod/pyathena_silver_test.py` | szkic Silvera z 25.08; te same 20 linii stoją w `silver.py`, tylko bez odsiewania powtórek. Zapisuje do **tego samego** pliku `silver/clean_data.csv` |
| 1.8 | `.claude/settings.local.json` | zgody dla `"kod/silver 1.py"` i `"kod/Data ingestion 2.py"` — pliki o tych nazwach nie istnieją od 01.09 |

**Co może pójść źle.** Punkt 1.3 kasuje jedyny w kodzie zapis przepisu
„jak liczyć Silver bez Atheny". Punkt 1.7 kasuje drugi taki zapis.
Gdyby Athena albo `pyathena` przestały działać, ten przepis byłby
punktem wyjścia do awaryjnej wersji. Odpowiedź: oba zostają w historii
gita i wyciąga się je jedną komendą, a dodatkowo wpiszemy je do dziennika
z dzisiejszą datą. Ryzyko realne, ale małe i odwracalne.

Punkt 1.5 kasuje kod z prawdziwego skryptu, który uruchamiamy raz
w miesiącu. Kompakcja jest jedynym skryptem, który **kasuje** pliki
w S3, więc każda jej edycja jest edycją narzędzia z ostrzem. Ale linie
44–46 stoją **po** zapisie i wysyłce, a przed sekcją kasowania, i nic
z nich nie wynika dla dalszego biegu: wczytują plik z dysku i wypisują
jego kształt. Sprawdzenie: pierwszy bieg kompakcji z prawdziwym
kasowaniem jest 1 października, więc mamy trzy tygodnie na uruchomienie
próbne.

**Jak sprawdzimy.** Po edycjach `python -m py_compile` na każdym zmienionym
pliku (ma nie wypisać nic) i `git status` (ma pokazać dokładnie te pliki,
których dotknęliśmy, i żadnego więcej).

---

## Grupa 2 — `print`-y i ślad w logu

Tu jest decyzja, nie tylko kasowanie, więc najpierw dwa fakty o tym, gdzie
w ogóle lądują wypisy.

**Log jest podwójny i to nie to samo.** `logging.basicConfig`
w Producencie zapisuje do `companies/errors.log`. `cron` przekierowuje
wypisy i błędy każdego skryptu do `companies/errors.txt`. To są dwa różne
pliki. Co z tego wynika: wszystko, co skrypt wypisze przez `print`, idzie
do `errors.txt`; wszystko, co zgłosi przez `logging.error`, idzie do
`errors.log`; a `Traceback` z niezłapanego błędu idzie do `errors.txt`.
Sprawdzając wieczorem `errors.txt`, nie widzimy zapisanych błędów
Producenta. W `errors.log` na Windowsie stoją też cudze wpisy — 08.09
`kafka-python` dopisał tam cztery linie o nieudanym połączeniu, bo
`basicConfig` ustawia log dla całego Pythona, nie tylko dla naszego kodu.
Ta podwójność nie jest do naprawy w tym kroku (to materiał na krok
„sygnał awarii"), ale trzeba ją znać, decydując o `print`-ach.

Ile ich jest dzisiaj: Gold 9, kompakcja 4, Producent 2, Silver 1,
Konsument 1, testy 1. (Przegląd z 08.09 mówi o Goldzie „osiem" i wymienia
dziewięć numerów linii — do poprawienia w przeglądzie.)

| # | Gdzie | Co proponuję |
|---|---|---|
| 2.1 | `kod/gold.py` linie 7, 10, 12, 13, 19, 20 | skasować sześć `print`-ów: trzy razy `dtypes`, `head()`, liczba miesięcy i `iloc[748:753]` — ten ostatni wypisuje wiersze o numerach wpisanych na sztywno w sierpniu, dziś pokazujące przypadkowe miejsce w środku danych |
| 2.2 | `kod/gold.py` linie 6, 16, 23 | **zostawić**: `gold.shape` to liczba, którą sprawdzamy wieczorem, a ranking całego okresu i `sp_rank` to wynik dnia |
| 2.3 | `kod/test_plikow.py` linia 6 | skasować `print` ze ścieżką pliku |
| 2.4 | `kod/silver.py` linia 19 | **zostawić** `print(dane.shape)` — jedyny ślad Silvera w `errors.txt` |
| 2.5 | `kod/kafka_consumer.py` linia 30 | **zostawić** `Odebrano N wiadomości` — jedyny ślad Konsumenta |
| 2.6 | `kod/data_ingestion.py` linie 10 i 51 | **do decyzji, patrz niżej** |

**Decyzja do podjęcia — punkt 2.6.** Producent ma dziś dwa `print`-y:
swoją ścieżkę i trzy adresy Yahoo. Oba są rusztowaniem z sierpnia i oba
wyglądają na śmieci. Ale to właśnie one są dowodem, że Producent w ogóle
się uruchomił, a od wczoraj także dowodem, że przekierowanie do logu
łapie pierwszy skrypt z połączonej linii `crontab`. Jeśli skasujemy oba,
w dobrym dniu Producent nie zostawi w `errors.txt` **ani jednej linii**
i wieczorne sprawdzenie zacznie się od `Odebrano`. Trzy możliwości:

- **A. Zostawić oba tak, jak są.** Zero pracy, log wygląda jak dziś.
- **B. Skasować oba.** Log czystszy, Producent niewidoczny w dobry dzień.
- **C. Skasować oba i wpisać w to miejsce jedną linię podsumowania** na
  końcu Producenta, na przykład ile nowych dni wysłał dla której spółki.
  Jedna linia zamiast czterech, a mówi więcej niż obie dzisiejsze razem.

Wybrałbym **C**, ale z zastrzeżeniem: to jest **dopisanie zachowania**,
nie sprzątanie, więc jeśli chcesz trzymać ten krok czysto przy kasowaniu,
**A** jest uczciwsze niż **B**, a **C** wróci przy kroku „sygnał awarii".

**Co może pójść źle w całej grupie 2.** Wieczorny przepis sprawdzania
opiera się na `print`-ach. Po tej zmianie przepis wygląda inaczej i trzeba
go zapisać na nowo, inaczej za tydzień będziemy szukać w logu linii,
której już nie ma, i uznamy to za awarię. Zapiszemy nowy przepis
w dzienniku tego samego dnia.

---

## Grupa 3 — `timeout` w `requests.get`

`kod/data_ingestion.py` linia 49: `requests.get(url, params=..., headers=...)`
bez `timeout`. Domyślnie `requests` **nie ma** żadnego limitu czasu. Jeśli
Yahoo przyjmie połączenie i zamilknie, Producent czeka bez końca.

Dlaczego to jest dziś groźniejsze niż tydzień temu: od wczoraj Producent
i Konsument stoją w jednej linii `crontab`, połączone średnikiem. Powłoka
nie zacznie Konsumenta, dopóki Producent nie skończy. Wiszący Producent
to więc także brak Konsumenta, a o 16:10 UTC Silver policzy wczorajszy
stan, nie dzisiejszy. Nazajutrz `cron` uruchomi drugiego Producenta obok
pierwszego, wciąż wiszącego.

Propozycja: `timeout=(10, 30)` — dziesięć sekund na nawiązanie połączenia,
trzydzieści na odpowiedź.

**Co może pójść źle.** Za krótki limit w wolny dzień przerwie pobieranie
dla jednej spółki. Wtedy zadziała `except` z linii 78, do `errors.log`
trafi wpis o błędzie pobierania, a plik pamięci tej spółki **nie zostanie
nadpisany** — więc jutro te dni znów będą nowe i pójdą do Kafki. Ścieżka
sama się leczy, bo naprawiliśmy ją 08.09. Trzydzieści sekund to dużo jak
na odpowiedź, która dziś przychodzi w ułamku sekundy.

**Jak sprawdzimy.** Lokalnie, z jawnie zaniżonym limitem (`timeout=0.001`)
— ma polecieć wpis do `errors.log` i plik spółki ma zostać nietknięty,
o tej samej liczbie wierszy co przed próbą. Potem wpisujemy właściwą
wartość. To jest sprawdzenie na Windowsie, bez EC2.

---

## Grupa 4 — konfiguracja do `config.py`

Dziś `config.py` ma jedną linię: listę trzech spółek. Reszta ustawień
stoi wpisana na sztywno, w wielu miejscach:

| Ustawienie | Wartość | Gdzie stoi dzisiaj |
|---|---|---|
| bucket | `gpw-tracker-bucket` | `silver.py` 7, `compaction.py` 12, 28, 43, 54, `kafka_consumer.py` 28 |
| region | `eu-north-1` | `silver.py` 8, `compaction.py` 13 |
| baza | `gpw-tracker_db` | `silver.py` 9, `compaction.py` 14 |
| folder wyników Atheny | `athena-results/` | `silver.py` 7, `compaction.py` 12 |
| adres brokera | `13.63.105.190:9092` | `data_ingestion.py` 18, `kafka_consumer.py` 7 |

(`pyathena_silver_test.py` ma te same trzy wartości, ale ten plik znika
w punkcie 1.7.)

Import zadziała bez sztuczek: wszystkie skrypty już robią
`from config import ticker`, także uruchamiane przez `cron` z pełną
ścieżką, bo Python dokłada folder skryptu do listy przeszukiwanych miejsc.

**Adres brokera to osobna sprawa i proponuję go nie ruszać w tym kroku.**
Przeniesienie go do `config.py` nic nie naprawia, a zmiana domyślnej
wartości na `localhost:9094` jest zmianą zachowania: dziś ręczny bieg na
EC2 bez `KAFKA_BOOTSTRAP` trafia w publiczny adres i traci dane, po
zmianie trafiałby dobrze, ale za to bieg z Windowsa przestałby działać
bez zmiennej. To decyzja, nie porządek, i należy do kroku o wdrożeniu.

**Co może pójść źle.** Literówka w `config.py` kładzie **wszystkie**
skrypty naraz, bo wszystkie go importują — Producenta, Konsumenta,
Silvera, Golda, kompakcję i testy. Błąd wyjdzie od razu, jako `Traceback`
przy uruchomieniu, nie po cichu. Gorszy wariant: nazwa się importuje, ale
wartość jest zła, na przykład bucket z literówką — wtedy `boto3` zgłosi
`NoSuchBucket` dopiero w chwili zapisu. Dlatego sprawdzenie musi być
biegiem, nie czytaniem.

**Jak sprawdzimy.** Lokalnie: uruchomić Silvera i Golda i porównać
`clean_data.csv` z kopią sprzed zmiany — `git diff` ma nie pokazać nic
poza nowym dniem. Na EC2, dopiero jutro: `git pull` z rytuałem
`git checkout -- silver/ gold/`, a potem wieczorny bieg. Kompakcji nie
uruchamiamy dla sprawdzenia, bo ona kasuje — jej sprawdzimy osobno,
przed 1 października.

---

## Co świadomie zostaje poza tym krokiem

- **`CRON_TZ=Europe/Warsaw`.** Załatwiłby zmianę czasu z końca
  października raz na zawsze, ale to jest edycja `crontab`, a `crontab`
  właśnie dziś jest sprawdzany po wczorajszej zmianie. Dwie zmiany
  harmonogramu w dwa dni to jedna zmiana za dużo. Do tego nie wiem, czy
  cron na tym EC2 tę linię obsługuje — to zależy od odmiany crona i trzeba
  to najpierw przeczytać, a nie założyć. Osobna, mała sesja, po
  potwierdzeniu 3b.
- **Trzy ostrzeżenia bibliotek w logu** (`kafka-python` o `lambda`
  w `value_deserializer`, `boto3` o Pythonie 3.9, `pandas` o `read_sql`).
  Żadne nie jest błędem, a każda „naprawa" oznacza dotknięcie działającej
  ścieżki danych po to, żeby log był ładniejszy. Zostają do kroku „sygnał
  awarii", gdzie i tak trzeba będzie odróżnić ostrzeżenie od `Traceback`.
- **`requirements.txt`.** Pin `pandas==3.0.5`, a na EC2 stoi 2.3.3, bo
  tamtej wersji `pip` nie znalazł. Plik dziś nie odtworzy środowiska EC2
  i to jest prawdziwa wada, ale jej naprawa to decyzja „co ten plik ma
  opisywać", nie sprzątanie.
- **`kod/pipeline.bat`.** Wygląda na śmiecia z sierpnia, **nie jest nim**:
  to jego uruchamia Harmonogram Windows o 18:10 jako zapas. Zostaje do
  kroku 6, w którym zapas wyłączamy.
- **`wykresy/*.png`** z 10.08 i `PowerBi_do_dopracowania.pbix` z 12.08.
  Nieaktualne o miesiąc, ale to jedyne obrazki, jakie projekt ma, a wracamy
  do nich przy wykresach. Zostają.
- **Klucz `.pem` w `aws/`** w folderze synchronizowanym przez OneDrive.
  Poza gitem, ale w cudzej chmurze. Do osobnej decyzji.

---

## Jak sprawdzimy całość

Liczby policzone dziś, **przed** edycjami:

| Plik | Linii dziś | `print`-ów dziś |
|---|---|---|
| `data_ingestion.py` | 86 | 2 |
| `kafka_consumer.py` | 30 | 1 |
| `silver.py` | 35 | 1 |
| `gold.py` | 25 | 9 |
| `compaction.py` | 56 | 4 |
| `test_plikow.py` | 37 | 1 |
| `config.py` | 1 | 0 |

Plików w `kod/` śledzonych przez gita: 12. Po sprzątaniu ma być 10
(znikają `pipeline.py` i `pyathena_silver_test.py`; `pipeline.bat`
zostaje, bo uruchamia go Harmonogram Windows).

Liczby linii po edycjach grupy 1: `data_ingestion.py` 81, `silver.py` 23,
`gold.py` 24, `compaction.py` 53.

Sprawdzenie po edycjach, w tej kolejności:

1. `python -m py_compile` na każdym zmienionym pliku — bez wypisu.
2. `pytest` — dwa testy jak dziś, oba zielone.
3. Bieg Silvera i Golda na Windowsie, `git diff silver/ gold/` — różnica
   tylko w danych dnia, nie w kształcie pliku.
4. `git status` — dokładnie te pliki, które ruszaliśmy.
5. Jutro na EC2, po sprawdzeniu 3b: `git pull` i wieczorny bieg według
   nowego przepisu na log.

---

## Co to zepsuje za miesiąc

Trzy rzeczy, o których trzeba pamiętać po tej zmianie:

1. **Przepis na czytanie logu się zmienia.** Po skasowaniu `print`-ów
   Golda w `errors.txt` będzie kilkanaście linii zamiast czterdziestu.
   Jeśli nie zapiszemy nowego przepisu w dzienniku, za tydzień będziemy
   szukać linii, których nie ma.
2. **`config.py` staje się plikiem, którego zepsucie kładzie wszystko.**
   To jest cena za jedno miejsce zamiast pięciu i uważam ją za dobrą,
   ale od tej pory każda zmiana w `config.py` wymaga biegu, nie samego
   czytania.
3. **Kasowanie `pyathena_silver_test.py` i zakomentowanego Silvera
   likwiduje jedyny zapisany przepis „Silver bez Atheny".** Zostaje
   w historii gita i w dzisiejszym dzienniku. Gdyby `pyathena` kiedyś
   przestało działać, tam będzie punkt wyjścia.

---

## Do zatwierdzenia

Gracjan wybiera zakres. Grupy są niezależne i można wziąć dowolne
połączenie:

- **Grupa 1** — martwy kod i śmieci, osiem pozycji, zero zmiany zachowania.
- **Grupa 2** — `print`-y, z decyzją A/B/C przy Producencie.
- **Grupa 3** — `timeout` w `requests.get`, jedna linia, największy zysk
  na jednostkę pracy.
- **Grupa 4** — bucket, region, baza i folder wyników do `config.py`.

Gdybym wybierał kolejność w jednej sesji: **3, potem 1, potem 4, potem 2**.
Grupa 3 dlatego, że jest jedną linią i zamyka prawdziwą dziurę. Grupa 1
dlatego, że nic nie może zepsuć. Grupa 4 przed grupą 2 dlatego, że
wymaga biegu sprawdzającego, a bieg i tak wypisze `print`-y, więc lepiej
je kasować, gdy reszta jest już potwierdzona.

Kod pisze Gracjan.

---

## Powiązane notatki

- [[Przeglad-2026-09-08-co-nie-gra]] — punkty 2.1, 2.5, 2.6, 2.9, 2.10,
  z których wzięta jest ta lista; krok 4 w Części 5
- [[Slownik]] — `timeout`, `py_compile`, log a przekierowanie
