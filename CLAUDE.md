# CLAUDE.md — zasady pracy nad projektem GPW Pulse

Ten plik jest długi celowo. Do 08.09.2026 był skracany do ~300 słów
i przez to nie mieścił ustaleń z rozmów — ginęły po jednej sesji. Od dziś
trzyma **wszystkie** zasady współpracy. Historia sesji nadal idzie do
dziennika, nie tutaj.

## Kim jest użytkownik

Gracjan, uczy się data engineeringu. GitHub: `gracjan20022002-prog`.

**Zna (potwierdzone we własnym kodzie):** `if/else`, pętle, listy,
słowniki, funkcje `def` z typami, `try/except`, `logging`, `requests`
i API, zapis do plików, list comprehensions, `lambda`/`map`/`filter`/`zip`,
pandas w praktyce (`read_csv`, typy, `groupby`, `pct_change`, `agg`,
`merge`, `drop_duplicates`, `to_parquet`), `matplotlib` podstawy, Power BI
podstawy, `pytest` podstawy, `kafka-python` (Producent/Konsument, `group_id`,
`commit`), `boto3` (`put_object`, `upload_file`, `delete_object`),
`pyathena` + SQL w Athenie (w tym `UNION`, `GROUP BY`, `HAVING`, `"$path"`),
Harmonogram Windows, `cron`, `systemd` na poziomie „enable/start/status",
SSH, `git` (w tym `git mv`, `git rm --cached`, `.gitignore`).

**Nie zna jeszcze:** klas, `async`, dekoratorów poza `@pytest.mark`,
testów z mockowaniem, CI/CD, HTML/CSS/JS (strona to nowy obszar).

## Zasady — obowiązkowe, wszystkie

1. **Kod i testy projektu pisze Gracjan sam.** Claude tłumaczy i pokazuje
   kształt rozwiązania na **innych danych** (lody, pogoda, SMS-y — nigdy
   spółki z projektu), zawsze z pokazanym wejściem **i** wyjściem, nie
   tylko opisem. Linijkę do wklejenia do pliku projektu Claude podaje
   tylko na wyraźną prośbę.

2. **Tłumaczyć bardzo szczegółowo.** Każde nowe słowo, wyrażenie,
   funkcja, moduł, flaga — wyjaśnione przy pierwszym użyciu, prostym
   językiem, bez zakładania, że Gracjan je zna. Krótkie zdania. Nowe
   pojęcia trafiają do `notatki/Slownik.md` tego samego dnia.

3. **Każda instrukcja jako ponumerowane kroki** w kolejności wykonania,
   jeden numer = jedna rzecz. Przy każdym kroku: gdzie (plik + linia
   albo maszyna), co zrobić, **co ma zobaczyć**, żeby odróżnić sukces od
   porażki. Analiza i tło w osobnej sekcji, nie między krokami.

4. **Każda komenda z etykietą maszyny i środowiska**, bez wyjątku,
   także ostatnia w sesji, także `git`: `[lokalny PowerShell, (.venv)
   włączone]`, `[lokalny PowerShell, venv nieistotne]`, `[EC2, przez
   SSH]`. Gdy komenda zależy od `venv` — najpierw komenda włączająca
   i sprawdzenie `(.venv)` w wierszu poleceń.

5. **Terminal, git, AWS, EC2 — zawsze Gracjan sam.** Claude może czytać
   lokalne pliki i stan gita. Nie dotyka EC2 ani AWS nawet do odczytu
   (żadnych `aws`, `ssh`, `Test-NetConnection`) — podaje komendę i czeka
   na wynik.

6. **Decyzje należą do Gracjana.** Claude przedstawia możliwości
   z konsekwencjami i mówi, którą by wybrał i dlaczego — ale nie
   wybiera, nie narzuca tematu sesji, nie rozpisuje planu dla tematu,
   którego Gracjan nie wybrał. Sesja zaczyna się od pytania, co robimy,
   nie od gotowego planu.

7. **Sesję kończy Gracjan.** Claude nie proponuje podsumowania, commitu
   ani „następnej sesji" bez pytania. Gdy wątek się kończy — meldunek
   wyniku i pytanie, co dalej.

8. **Dokumentację pisze Claude, w całości:** dziennik
   (`notatki/dziennik/RRRR-MM-DD.md`, wszystkie sekcje, łącznie z „Czego
   się nauczyłem" w pierwszej osobie), `README.md`, ten plik, plany
   w `notatki/plany/`, słownik. Na koniec sesji, gdy Gracjan powie, że
   kończymy. **Gracjan nigdy nie pisał w dzienniku** — Claude nie cytuje
   dziennika jako słów Gracjana („sam napisałeś…").

9. **Definicja „zrobione".** Claude nie pisze „ukończone", „działa",
   „zautomatyzowane", „w pełni" o niczym, co nie spełnia **wszystkich**
   pięciu warunków: (a) działa na prawdziwej drodze danych; (b) ma
   sprawdzenie, które to udowadnia — liczba policzona **przed** biegiem
   i potwierdzona po; (c) awaria jest głośna, nie cicha; (d) wdrożone
   i sprawdzone tam, gdzie ma działać (EC2); (e) opisane zgodnie
   z prawdą, łącznie z tym, czego jeszcze nie ma. Jeśli któryś warunek
   nie jest spełniony, Claude pisze który.

10. **Notatka projektowa przed kodem mechanizmu.** Przed nowym
    skryptem, tabelą, wpisem `cron`, narzędziem: co, po co, **co może
    pójść źle** (broker nie odpowiada, Athena zwraca pół tabeli, skrypt
    odpala się dwa razy, odpala się o złej godzinie, dochodzi czwarta
    spółka), jak sprawdzimy, co to zepsuje za miesiąc. Gracjan
    zatwierdza, potem kod. **Notatka ma być zrozumiała** (14.09 — pierwsza
    wersja notatki o teście zakładki była dla Gracjana niezrozumiała):
    najpierw sedno w trzech zdaniach, potem przykład na innych danych
    z wejściem i wyjściem i tabela „przykład → projekt", ryzyka i decyzje
    po jednej linii. Numery linii i dokładne komendy idą do kroków po
    zatwierdzeniu, nie do notatki.

11. **Sprawdzać, nie zakładać.** Przed stwierdzeniem o plikach, danych,
    gicie — czytać i liczyć. Przewidywany wynik pisany **przed**
    uruchomieniem. Gdy Claude nie sprawdził — mówi „nie sprawdziłem".
    **I szybko** (prośba Gracjana z 13.09): sprawdzać tylko to, co zmienia
    następny krok albo liczbę do porównania; wszystkie odczyty w jednej
    rundzie; bez długich objazdów po kodzie źródłowym i starych
    rozmowach; krótkie wiadomości.

12. **Bez żargonu numerów.** „Wątek 3 punkt 2", „Część D", „Etap 5 E" —
    tylko z wyjaśnieniem w tym samym zdaniu, co to jest. Lepiej nazwać
    rzecz: „wynik Golda poza EC2".

13. **`git push` zawsze** w sekwencji commitu — EC2 widzi tylko GitHub.

14. **Na EC2 przed `git pull`: `git checkout -- silver/ gold/`. Nigdy
    `git stash`** — to on wysadził projekt 01.09. Po zmianie nazwy pliku
    — ręcznie poprawić `crontab`.

15. **Najpierw naprawa, potem budowa.** Żadnej nowej funkcji, dopóki
    lista wad z przeglądu 08.09 nie jest zamknięta w kolejności
    ustalonej z Gracjanem.

16. **Przegląd całości** (cały kod + wszystkie notatki od początku) po
    zamknięciu każdego większego kawałka i zawsze na prośbę Gracjana —
    wynik do pliku przeglądu, nie do pamięci.

## Stan projektu — uczciwie (14.09 wieczorem)

Repo: `GPW - pulse`, GitHub `github.com/gracjan20022002-prog/GPW---pulse`.
**Źródło prawdy o wadach i kolejności napraw:**
[`notatki/plany/Przeglad-2026-09-08-co-nie-gra.md`](notatki/plany/Przeglad-2026-09-08-co-nie-gra.md),
nie README.

### Jak dziś płyną dane, sprawdzone

Na EC2 (`t3.micro`, Elastic IP `13.63.105.190`, 24/7) `cron` uruchamia
codziennie **o 18:00 czasu polskiego** jedną linię
`data_ingestion.py ; kafka_consumer.py` i **o 18:10** `silver.py &&
gold.py`. Od 13.09 na górze `crontab` stoi `CRON_TZ=Europe/Warsaw`, więc
godziny w pliku (`0 18`, `10 18`) są polskie przez cały rok. Sprawdzone
wpisem `RELOAD` w dzienniku systemowym i biegami 13.09 (niedziela) oraz
14.09 (dzień giełdowy). Pełny tekst `crontab`:
`notatki/plany/Notatka-2026-09-13-strefa-czasowa-cron.md`, część 4.

**UWAGA przy czytaniu logu:** strefa działa **tylko wewnątrz `cron`**.
Skrypty, log, `ls -l`, narzędzia Kafki i dziennik systemowy dalej chodzą
w UTC. Latem bieg o 18:00 polskiego ma w linii startu `16:00:0X`. **Od
25.10 pokaże `17:00:0X` i to będzie poprawne**, nie przesunięcie biegu.
Przy każdej godzinie mówić, w jakiej strefie jest.

- **Producent** (`data_ingestion.py`): Yahoo `range=3y` → Kafka, topic
  `gpw_tracker`. Każda wiadomość z potwierdzeniem brokera
  (`send(...).get(timeout=10)`); pamięć `companies/*.txt` zapisywana tylko
  po potwierdzeniu. W logu linia startu z datą i godziną UTC, potem jedna
  linia na spółkę: `nowych dni`, `wysłane`, `stan: zapisane|nietknięte`.
- **Konsument** (`kafka_consumer.py`): grupa `gpw_consumer`,
  `auto_offset_reset='earliest'`, czyta do 5 s ciszy, pisze po jednym
  pliku JSON na spółkę do S3 `live/spolka=…/`, na końcu `commit()`.
- **Silver** (`silver.py`): Athena `bronze UNION live`, odsiewa powtórzone
  dni → `silver/clean_data.csv` na dysku EC2.
- **Gold** (`gold.py`): zmiany procentowe i ranking „najbardziej zmiennego
  **pełnego** miesiąca" (bez pierwszego i ostatniego miesiąca historii
  spółki i bez miesięcy poniżej 15 dni notowań) → `gold/*.csv` na dysku EC2.
- **`bronze`** w S3 to Parquet do końca poprzedniego miesiąca, przepisywany
  ręcznie przez `compaction.py`, **wyłącznie z laptopa** (pierwszy bieg
  z prawdziwym kasowaniem: 1 października).
- **Lokalny Harmonogram Windows** liczy Silver+Gold równolegle o 18:10 jako
  „zapas" (`kod/pipeline.bat`, pełne ścieżki do `.venv\Scripts\python.exe`).

**Normalny blok jednego biegu w `errors.txt`:**
- w dzień giełdowy **24 linie**: Producent 4, ostrzeżenie `kafka-python` 2,
  `boto3` 2, `Odebrano` 1, `pandas` 2, Silver 1, Gold 12;
- bez nowych wiadomości **22 linie**, bo Konsument tworzy klienta S3,
  a z nim ostrzeżenie `boto3`, tylko wtedy, gdy ma co zapisać.

Stan 14.09 po biegu i teście: `errors.txt` 506, `errors.log` 8, pliki spółek
po 771, zakładka `2342`, najstarsza wiadomość w topicu 2327, w S3 `live/`
27 plików.

### Kolejność napraw — gdzie jesteśmy

Kolejność z Części 5 przeglądu, zatwierdzona 08.09.

1. **Producent nie gubi danych** — ✅ 08.09.
2. **Strażnik kompakcji** — ✅ 08.09.
3. **Konsument `earliest` i jedna linia `crontab`** — ✅ 08–10.09.
   **Ścieżka bez zakładki sprawdzona testem 14.09.**
4. **Sprzątanie kodu** — ✅ 11.09 na EC2. Do tego:
   - podsumowanie Producenta, ✅ trzy ścieżki: awaria brokera 11.09
     lokalnie, „nic nowego" 12.09 na EC2, dzień giełdowy 14.09 na EC2;
   - spisy wymagań dla dwóch maszyn, ✅ 11.09;
   - `CRON_TZ`, ✅ 13–14.09.
5. **Wynik Golda do S3 i Atheny** — ⬜, następny w kolejności, zaczyna się
   od notatki projektowej.
6. **Wyłączenie lokalnego Harmonogramu, `silver/` i `gold/` poza gitem** —
   ⬜.
7. **Test prawdziwej drogi** — ⬜.
8. **Sygnał awarii** — ⬜. Dotyczy wszystkiego: **każde ✅ wyżej ma
   niespełniony warunek (c)**, bo awarię widać tylko w logu, którego nikt
   nie czyta.
9. **Pełne miesiące w rankingu** — ✅ 12.09 lokalnie, 14.09 na EC2, wzięte
   poza kolejnością.
10. **Dokumentacja** — ⬜ w tle: README od nowa, dziesięć wpisów dziennika
    bez „Czego się nauczyłem", plany do posprzątania.

### Wciąż otwarte (najkrócej, pełne opisy w przeglądzie)

- Wynik Golda kończy na dysku EC2 i nic go nie czyta.
- Producent uruchomiony przed 17:00 zapisuje cenę z trwającej sesji jako
  zamknięcie.
- Okno na kurs zamknięcia u Yahoo ma najwyżej kwadrans zapasu (11.09:
  o 17:45 brak świecy, o 18:00 jest).
- Testy sprawdzają rzeczy obok potoku.
- Nikt nie dowie się o awarii. Log jest podwójny, a czytamy tylko połowę:
  `logging.error` → `errors.log`, `print` i `Traceback` → `errors.txt`.
- Korekty cen Yahoo nie docierają do S3.
- Nierówne okna `range=3y` dla nowej spółki (13.09).
- README obiecuje więcej, niż jest.
- **Nowe 14.09, wszystkie w przeglądzie:**
  - Konsument bez `consumer.close()`, więc broker przez kilkanaście sekund
    widzi go jako członka grupy;
  - **podejrzenie, niesprawdzone:** `kafka-python` sam zapisuje zakładkę
    co 5 s, możliwe że zanim wiadomości trafią do S3;
  - CBF 14.09 `201.0`, identycznie jak 11.09, niesprawdzone ze źródłem
    zewnętrznym.
- **Poza kolejnością, do decyzji Gracjana:**
  - Python 3.10 na EC2, jedyna sprawa, która pogarsza się sama, bo `boto3`
    porzucił 3.9 w kwietniu 2026;
  - `pd.read_sql` przez SQLAlchemy;
  - ostrzeżenie `value_deserializer`;
  - słowa „niedobór pamięci" w komentarzu `compaction.py` (prawdziwy powód
    to brak biblioteki);
  - plan B dla źródła danych.

### Test „zakładki nie ma" — wynik z 14.09

Notatka: `notatki/plany/Notatka-2026-09-14-test-zakladki.md`.

- **Bramka:** najstarsza wiadomość w topicu miała numer 2327, czyli segment
  z zalewem z 01.09 został skasowany tak, jak przewidzieliśmy 09.09.
- **Test:** grupa `gpw_consumer` skasowana `--delete`, potem ręczny bieg
  Konsumenta z `KAFKA_BOOTSTRAP=localhost:9094`. Wynik: `Odebrano 15
  wiadomości` i zakładka 2342.
- **S3:** w `live/` 24 → 27 plików. Nowe pliki są bajt w bajt sklejeniem
  pięciu dziennych plików spółki.
- **Silver** na laptopie po teście: `(2313, 3)`, plik z tą samą sumą SHA256
  co przed testem.
- **Pomyłka Claude'a:** przewidział `no active members` zaraz po biegu,
  a wyszedł jeszcze członek grupy (brak `close()`).
- **Brakuje:** potwierdzenia Silvera na EC2 (bieg 15.09) i sygnału awarii.
- **Skutek za miesiąc:** 3 pliki powtórek w `live/`, więc kompakcja 1.10
  wypisze o 3 więcej w `Usunięto N plików`.

### Pomyłki Claude'a z ostatnich dni, wszystkie sprostowane

- **11.09:** trzy commity zapowiedziane przy `git pull`, było sześć;
  decyzja o `pyarrow` „nigdzie niezapisana", a była w trzech miejscach;
  wada rankingu „znana tylko z opisu", a była zaobserwowana.
- **11–12.09:** „po `CRON_TZ` linia startu pokaże 18:00". Nieprawda, zostaje
  UTC. Sprostowane w notatce z 11.09.
- **12.09:** sobotni blok „23 linie". Było 21, bez `boto3`.
- **12.09:** „o 17:00 świecy tym bardziej nie będzie". Za pewne: 08.09
  o 16:43 była świeca z ceną z trwającej sesji.
- **13.09:** „dokładnie siedem linii `diff`". Było osiem, treść zgodna.
- **14.09:** `no active members` zaraz po ręcznym biegu Konsumenta. Członek
  grupy był jeszcze na liście.
- **14.09:** pierwsza wersja notatki o teście zakładki niezrozumiała, stąd
  dopisek w zasadzie 10.

### Priorytet Gracjana (08.09)

Czysty, działający łańcuch `data_ingestion → Kafka → S3/Athena → silver →
gold` → wynik na stronie. Wykresy, README pod pracodawcę, Power BI —
dopiero potem.

### Na następną sesję

Zgodnie z zasadą 6 temat wybiera Gracjan. Ustalony jest tylko odczyt.

1. **15.09 po 18:15, odczyt biegu `cron`.** Zamyka test zakładki na EC2.
   Przewidywania:
   - `507:=== Data pomiaru Producenta: 2026-09-15 16:00:0X ===`;
   - `errors.txt` 530, blok 24, `errors.log` 8, pliki spółek po 772;
   - `Odebrano 3 wiadomości`;
   - dwa razy `(2316, 3)`;
   - linia Golda `114` i `108`;
   - zakładka `2345 2345 0`.
2. **Do wyboru Gracjana:**
   - wynik Golda do S3 i Atheny (następny w kolejności napraw);
   - trzy drobiazgi z 14.09;
   - Python 3.10 na EC2;
   - pozostałe punkty „poza kolejnością".
3. **Terminy:**
   - najbliższy weekend: blok 22 linie;
   - 1.10: kompakcja z laptopa;
   - 26.10: pierwszy bieg po zmianie czasu (`17:00:0X`).

**EC2 stoi na `3c488f1`.** Commity z 14.09 to dokumentacja i dane z laptopa,
bez kodu. EC2 nie musi ich pobierać przed biegiem 15.09. Przy następnym
`git pull` — rytuał z zasady 14.

### Kopie

- **Pamięć Producenta:** `~/pamiec-kopia-0809/` (Windows).
- **Poprzedni `bronze`:** `bronze/poprzedni/` (poza gitem).
- **Na EC2:**
  - `~/crontab-kopia-0913.txt` to **jedyny** powrót do stanu sprzed
    `CRON_TZ`: `crontab ~/crontab-kopia-0913.txt`;
  - `~/crontab-kopia-0909.txt` to harmonogram sprzed 09.09 (cofnąłby o cztery
    dni);
  - `~/crontab-nowy.txt` to plik wgrany 09.09;
  - `~/crontab-nowy-0913.txt` to plik wgrany 13.09.

## Gdzie co jest

Kod, dane i notatki razem w folderze projektu: `kod/`, `companies/`
(pamięć Producenta, **poza gitem**, każda maszyna ma własną), `bronze/`
(poza gitem), `silver/`, `gold/` (w gicie — do zmiany, gdy wynik trafi
do S3), `wykresy/`, `notatki/`, `aws/` (klucz SSH, poza gitem). Nauka
Pythona (osobny projekt): `DE/Python_l/`.

**Co z `notatki/` jest w gicie, sprawdzone 11.09.** `notatki/plany/`
i `notatki/Slownik.md` **są śledzone**. Poza gitem, przez `.gitignore`, są
`notatki/dziennik/` i `notatki/.obsidian/`. Znaczy to, że **wszystkie wpisy
dziennika (31 plików na 14.09), czyli cały zapis nauki z tego projektu,
istnieją wyłącznie na laptopie i w OneDrive, ani jeden nie jest
w repozytorium**. Decyzja, czy ma tak zostać, należy do Gracjana i nie była
dotąd nigdzie uzasadniona.

**Środowiska Pythona.**
- **Laptop:** `.venv` (z kropką), Python 3.14.2, spis
  `requirements-lokalny.txt` (32 paczki).
- **EC2:** `venv` (bez kropki), Python 3.9.25, spis `requirements-ec2.txt`
  (19 paczek).
- Pliku `requirements.txt` **celowo nie ma**. To konwencja, z której ktoś
  odruchowo zainstalowałby zły zestaw.
- `crontab` i `pipeline.bat` wołają Pythona pełną ścieżką z `venv`, bez
  aktywacji.
- Folderu z `venv` nie przenosić: w środku są zapisane pełne ścieżki
  (EC2, 31.08).

**EC2:**
- połączenie z folderu `aws\aws ec2 key`:
  `ssh -i "gpw-tracker-key.pem" ec2-user@13.63.105.190`;
- repo `~/GPW---pulse`, Python `~/GPW---pulse/venv/bin/python`;
- log `cron`: `~/GPW---pulse/companies/errors.txt`;
- narzędzia Kafki `~/kafka_2.13-4.3.1/bin/`, broker `localhost:9094`,
  topic `gpw_tracker`, grupa `gpw_consumer`;
- ręczny bieg Producenta albo Konsumenta **tylko** z
  `KAFKA_BOOTSTRAP=localhost:9094` przed komendą.

**S3** (z laptopa, narzędzie `aws` zainstalowane): bucket
`gpw-tracker-bucket`, podgląd `aws s3 ls s3://gpw-tracker-bucket/live/
--recursive --summarize`.
