# CLAUDE.md — zasady pracy nad projektem GPW Pulse

Ten plik jest długi celowo. Do 08.09.2026 był skracany do ~300 słów
i przez to nie mieścił ustaleń z rozmów — ginęły po jednej sesji. Od dziś
trzyma **wszystkie** zasady współpracy. Historia sesji nadal idzie do
dziennika, nie tutaj. **Od 10.10** (decyzja 6 z przeglądu z 08.10) codzienne
sekcje stanu z liczbami są w `notatki/plany/Historia-stanu.md`. Tutaj zostają
zasady, stan bieżący, kontrola, przewidywania, otwarte sprawy i terminy.
Stan z dnia sesji dopisywać tutaj krótko, szczegóły do dziennika.

## Kim jest użytkownik

Gracjan, uczy się data engineeringu. GitHub: `gracjan20022002-prog`.

**Zna (potwierdzone we własnym kodzie):** `if/else`, pętle, listy,
słowniki, funkcje `def` z typami, `try/except`, `logging`, `requests`
i API, zapis do plików, list comprehensions, `lambda`/`map`/`filter`/`zip`,
pandas w praktyce (`read_csv`, typy, `groupby`, `pct_change`, `agg`,
`merge`, `drop_duplicates`, `to_parquet`, od 03.10 `read_sql` z `pyathena` i `sort_values`
z `ascending=False` w wykresach), `matplotlib` podstawy, Power BI
podstawy, `pytest` podstawy, strefy czasowe (`ZoneInfo`, `.astimezone`, `time(17, 55)`,
od 05.10) i flaga z `continue` w pętli (06.10), `except ClientError as e` z
`e.response["Error"]["Code"]` i samo `raise` (09.10), `kafka-python` (Producent/Konsument, `group_id`,
`commit`), `boto3` (`put_object`, `upload_file`, `delete_object`),
`pyathena` + SQL w Athenie (w tym `UNION`, `GROUP BY`, `HAVING`, `"$path"`),
Harmonogram Windows, `cron`, `systemd` na poziomie „enable/start/status",
SSH, `git` (w tym `git mv`, `git rm --cached`, `.gitignore`), zmienne
środowiskowe (`os.environ.get`, `$env:`, `Remove-Item Env:`). **Pracuje
zwykle w PowerShellu** (15.09) — składnia `$env:NAZWA`, nie `%NAZWA%`;
przed komendą zależną od powłoki patrzeć, czy wklejony wiersz zaczyna się
od `PS`.

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
   **Kroki do kodu (18.09, dwie prośby Gracjana: „rozpisz lepiej", potem
   „skróć"):** najpierw same kroki, jedna krótka linia na krok, potem
   przykład na innych danych. Kroków z wcześniejszej wiadomości nie odsyłać
   („są wyżej") — powtórzyć je. Przy ocenie kodu: numer linii, co jest, co
   ma być, skutek — i przewidywany wynik testów przed uruchomieniem.
   **Pełna instrukcja przed kodem (23.09, prośba Gracjana: „co chwilę
   zmieniasz zasady… przygotuj mi gotową notatkę"):** zanim Gracjan zacznie
   pisać kawałek kodu albo testów, dostaje jedną kompletną notatkę:
   wszystkie zasady, wszystkie nowe pojęcia z wejściem i wyjściem, wszystkie
   przypadki z wynikami sprawdzonymi uruchomieniem przykładu i tabelę
   błędów. Przy ocenie kodu Claude odwołuje się tylko do niej. Coś nowego
   = przyznanie, że notatka tego nie miała, i dopisanie. Wzór:
   `notatki/plany/Notatka-2026-09-23-jak-napisac-testy-drogi.md`.
   **Ocena po każdej zmianie (06.10, Gracjan: „miałeś to robić za każdym
   razem”):** gdy Gracjan zmieni plik projektu, Claude sam, bez proszenia,
   czyta `git diff` i opisuje każdą nową linię: numer, co w niej jest, czy
   zgodna z instrukcją, co robi i co zmienia w biegu (na konkretnych
   wartościach). Potem przewidywany wynik testów, dopiero potem następne kroki.

4. **Każda komenda z etykietą maszyny i środowiska**, bez wyjątku,
   także ostatnia w sesji, także `git`: `[lokalny PowerShell, (.venv)
   włączone]`, `[lokalny PowerShell, venv nieistotne]`, `[EC2, przez
   SSH]`. Gdy komenda zależy od `venv` — najpierw komenda włączająca
   i sprawdzenie `(.venv)` w wierszu poleceń.
   **Każda komenda (i zapytanie SQL) w osobnym okienku kodu**, jedna na
   okienko, pod swoim krokiem, żeby dało się ją od razu skopiować (25.09,
   prośba Gracjana: „wcześniej lepiej wysyłałeś komendy… w oknie"). Etykieta
   i oczekiwany wynik jako zwykły tekst obok, nie w okienku.
   **Przy pisaniu kodu — krok po kroku** (25.09, „rozpisuj mi każdy krok po
   kolei"): porcja kilku–kilkunastu kroków, każdy = jedna czynność w edytorze
   (plik, numer linii, wcięcie w spacjach, co ma być widać), na końcu porcji
   uruchomienie i prośba o wynik; następna porcja po wyniku.
   **Krok PRZEŁĄCZENIE** (03.10, Gracjan: „miałeś mnie informować gdy
   przełączamy się między lokalnym a ec2, albo między venv”): każda zmiana
   maszyny albo środowiska (nowe okno, `ssh`, wyjście z EC2, włączenie `venv`)
   to osobny, numerowany krok oznaczony **PRZEŁĄCZENIE**, z komendą i z tym,
   jak ma wyglądać wiersz (`(.venv) PS …>`, `GPW---pulse]$`). Stoi na początku
   **każdej** porcji, także gdy poprzednia skończyła się w tym samym miejscu.
   **Etykieta opisuje stan okna**, nie potrzeby komendy: po kroku, który
   włącza `venv`, każda następna komenda w tym oknie ma „(.venv) włączone”
   („venv nieistotne” obok „włącz venv” — Gracjan: „bez sensu”). „venv
   nieistotne” tylko w oknie, w którym `venv` nigdy nie był włączony.

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

14. **Na EC2 `git pull` już nie wymaga rytuału `git checkout -- silver/
    gold/`** — od 21.09 oba foldery są w `.gitignore` (`.gitkeep` jedyny
    plik pod kontrolą wersji), sprawdzian 22.09 potwierdził `git status
    --short` pusty po pełnym biegu `cron`. **Nigdy `git stash`** — to on
    wysadził projekt 01.09. Po zmianie nazwy pliku — ręcznie poprawić
    `crontab`.

15. **Najpierw naprawa, potem budowa.** Żadnej nowej funkcji, dopóki
    lista wad z przeglądu 08.09 nie jest zamknięta w kolejności
    ustalonej z Gracjanem. **Lista z 08.09 zamknięta 04.10.** Od 08.10
    obowiązują wady i kolejność z `Przeglad-2026-10-08-calosc.md` (decyzja 7,
    zmieniona 10.10: duża dokumentacja przed naprawami 1 i 2, kod strony po nich).

16. **Przegląd całości** (cały kod + wszystkie notatki od początku) po
    zamknięciu każdego większego kawałka i zawsze na prośbę Gracjana —
    wynik do pliku przeglądu, nie do pamięci.

## Stan projektu (10.10)

Repo: `GPW - pulse`, GitHub `github.com/gracjan20022002-prog/GPW---pulse`.
- **Źródło prawdy o wadach i kolejności napraw (od 08.10, decyzja Gracjana):**
  [`notatki/plany/Przeglad-2026-10-08-calosc.md`](notatki/plany/Przeglad-2026-10-08-calosc.md),
  tabela „Stan punktów” na górze. Przegląd z 08.09 to historia.
- **Historia stanu dzień po dniu (12.09–10.10):**
  [`notatki/plany/Historia-stanu.md`](notatki/plany/Historia-stanu.md). Są tam:
  - wszystkie dawne sekcje „Stan …” z liczbami;
  - tabele przewidywań do 16.10;
  - kolejność napraw z 08.09 (lista zamknięta 04.10);
  - sygnał awarii z 21.09 i test zakładki z 14.09;
  - stare „Wciąż otwarte” i pełna lista pomyłek Claude'a.

  Plik przeniesiony 10.10 bez zmian (decyzja 6 z 08.10). Stan sprzed 12.09:
  `notatki/plany/Historia-projektu.md` i dziennik.

### Jak dziś płyną dane

**Maszyna.** EC2 `t3.micro`, Elastic IP `13.63.105.190`, chodzi 24/7, Amazon Linux
`2023.12.20260817`.

**`crontab` ma siedem linii.** Cztery zmienne na górze:
- `CRON_TZ=Europe/Warsaw`;
- `KAFKA_BOOTSTRAP=localhost:9094`;
- `GOLD_DO_S3=1`;
- `STROZ_URL=…` — adres stróża, **nigdy w gicie, nigdy na zrzucie ekranu**.

Pod nimi trzy biegi. Wszystkie idą na `~/GPW---pulse/venv314/bin/python` (Python 3.14.6 od 03.10)
i piszą przez `>> companies/errors.txt 2>&1`:
- **18:00** `data_ingestion.py ; kafka_consumer.py`;
- **18:10** `silver.py && gold.py`;
- **18:30** `control.py`.

Godziny są polskie przez cały rok, bo `crontab` ma `CRON_TZ`.

**UWAGA przy czytaniu logu:** strefa działa **tylko wewnątrz `cron`**. Skrypty, log, `ls -l`,
narzędzia Kafki, `aws s3 ls` i dziennik systemowy chodzą w UTC. Latem bieg o 18:00 polskiego ma
w linii startu `16:00:0X`. **Od 25.10 pokaże `17:00:0X` i to będzie poprawne.** Przy każdej
godzinie mówić, w jakiej jest strefie.

#### Producent (`data_ingestion.py`)

- Pobiera z Yahoo `range=3y` i wysyła do Kafki, topic `gpw_tracker`.
- **Przed 17:55 polskiego pomija dzisiejszą świecę** (`kod/session.py`, na EC2 od 07.10) i dopisuje
  w logu `dziś pominięte (przed 17:55)`.
- Każda wiadomość czeka na potwierdzenie brokera (`send(...).get(timeout=10)`).
- Pamięć `companies/*.WA.txt` zapisuje tylko po potwierdzeniu, **cały plik od nowa i z cenami
  z bieżącej odpowiedzi Yahoo** (linia 62). Do Kafki idą tylko nowe daty.
- Błędy (`ERROR`) idą na stderr, czyli do `errors.txt`. Linia startu ma `flush=True`.
- Linia 16 ma zapasowy adres brokera `13.63.105.190:9092`. Do usunięcia w naprawie 2.

#### Konsument (`kafka_consumer.py`)

- Grupa `gpw_consumer`, `auto_offset_reset='earliest'`, `enable_auto_commit=False`.
- Czyta, aż przez 5 s nic nie przyjdzie. Zapisuje jeden plik JSON na spółkę do
  `live/spolka=…/`. Potem `commit()`, na końcu `close()`.
- Klienta S3, a z nim plik, tworzy tylko wtedy, gdy ma co zapisać.
- `close()` stoi za `put_object`, a nie w `finally`. Przy awarii zapisu broker przez kilkanaście
  sekund widzi więc martwego członka grupy, co blokuje `--reset-offsets`.

#### Silver (`silver.py`)

- Athena `bronze UNION live`, odsiewa powtórzone dni i zapisuje `silver/clean_data.csv` na EC2.
- Przy dwóch różnych cenach tego samego dnia wybiera przypadkowo (znana wada).

#### Gold (`gold.py`)

- Liczy zmiany procentowe i ranking najbardziej zmiennego **pełnego** miesiąca. Pełny znaczy: bez
  pierwszego i ostatniego miesiąca historii spółki i bez miesięcy poniżej 15 dni notowań.
- Zapisuje `gold/*.csv` na EC2. Przy `GOLD_DO_S3=1` wysyła też oba pliki do S3:
  `gold/dane_dzienne/dane_dzienne.csv` i `gold/ranking/ranking.csv` (linia `S3: wysłano …`).

#### Kontrola (`control.py`, 18:30)

Sprawdza dwie rzeczy:
1. **Ostatni blok `errors.txt`, czyli dowód sukcesu:** `stan: zapisane` przy każdej spółce,
   `Odebrano`, 2 × `S3: wysłano`, zero `Traceback`.
2. **Tabelę `gold_dane_dzienne` w Athenie**, przez `pobierz_dane()` i `sprawdz_daty()` z
   `kod/path.py`. Szuka czterech problemów: brak dzisiejszej świecy w dzień pon–pt, wpis
   z przyszłości, różna liczba dni między spółkami, spółka bez wierszy.

Wysyła jedno zgłoszenie do stróża: `GET` przy `OK`, a przy awarii `POST …/fail` z treścią
w UTF-8. Każda linia wyniku zaczyna się od `Kontrola:`, żeby powtórny bieg tego samego dnia
pominął własne linie.

#### `bronze` i kompakcja (`compaction.py`)

- `bronze` to Parquet do końca poprzedniego miesiąca.
- Kompakcja przepisuje go ręcznie, **tylko z laptopa** (EC2 nie ma `pyarrow`), raz w miesiącu,
  nigdy między 17:55 a 18:35.
- **Strażnik od 09.10:** kopia poprzedniego `bronze` pobierana przed zapytaniem do Atheny, kod
  `"404"` znaczy nową spółkę, każdy inny kod → `raise`.
- Ostatnie biegi:
  - 03.10 z kasowaniem: `bronze` do 30.09, 783 wiersze na spółkę, `Usunięto 66 plików`;
  - 09.10 próba generalna: `Usunięto 0 plików`.
- Następna: początek listopada.

#### Laptop

- `silver/` i `gold/` są poza gitem od 21.09. `.gitignore` przepuszcza tylko `.gitkeep`.
- Harmonogram Windows (`GPW Pulse - pipeline`) jest wyłączony od 21.09, więc lokalne `silver/`
  i `gold/` stoją od 20.09. Powrót: `Enable-ScheduledTask`.
- Wykresy (`wykresy.py`, `ranking.py`) czytają Athenę od 03.10.
- Power BI odłożony, pokazuje dane do 20.09.

### Normalny blok jednego biegu w `errors.txt`

**Od 03.10 blok ma 28 linii w każdym rodzaju dnia**, razem z `Kontrola: OK`. Kolejno:

| Linie | Co |
|---|---|
| 1 | linia startu |
| 3 | wynik Producenta, po jednej linii na spółkę |
| 2 | ostrzeżenie `value_deserializer` |
| 1 | `Odebrano N wiadomości` |
| 2 | ostrzeżenie `pandas` z `silver.py` |
| 2 | `(M, 3)` z Silvera i z Golda |
| 11 | reszta Golda: tabela 4, `Pełna liczba … 117, Prawidłowa … 111` (październik) 1, ranking 6 |
| 2 | `S3: wysłano` |
| 2 | ostrzeżenie `pandas` z `kod/path.py:32` |
| 2 | `Kontrola: Dane M wierszy`, `Kontrola: OK` |

Jak czytać rozjazd:
- **Inna liczba linii** znaczy, że zmieniło się coś jeszcze.
- **Martwy broker:** blok rośnie o 4 linie `ERROR`.
- **Awaria Atheny:** zamiast 4 linii kontroli będzie `Traceback` od `pyathena` (25 linii na
  Pythonie 3.9, na 3.14 więcej) i 1 linia wyniku (pandas 3.0.5). **Na EC2 na 3.14 niesprawdzone.**
- **`PythonDeprecationWarning` w bloku** znaczy, że `cron` wrócił do starego `venv`.

### Ostatnie liczby (bieg 09.10, sprawdzony 10.10)

- Log: start w linii **1196**, `wc -l` **1223**.
- Dane: 2 × `(2370, 3)`, `Kontrola: Dane 2370 wierszy`, pliki spółek **790 × 3**.
- Zakładka **`2399 2399 0`**, `errors.log` **8**.
- S3 `gold/`: **158692 B** i **338 B**, z `16:10:08` UTC.
- Stróż: **#25**.
- Ranking: CBF 200,00, SNT 344,00, XTB 139,72 — zgodne z GPW.
- Ceny w S3 porównane z archiwum GPW: 90, wszystkie zgodne co do grosza (66 z historii, 17, 18
  i 21.09 oraz 05–09.10).

### Przewidywania od 10.10

Zapisane przed biegami: wiersze 10–16.10 dnia 08.10, a 17–25.10 dnia 10.10.
- Blok ma 28 linii.
- W październiku nie ma świąt. Gold daje `117`/`111` do końca miesiąca.
- **Numery u stróża przesuwa każdy ręczny `control.py` ze `STROZ_URL`.**
- S3 `dane_dzienne.csv` rośnie o ok. 193–218 B na dzień giełdowy (09.10: +193). `ranking.csv`
  ma 330–370 B.

| Dzień | Start | `wc -l` po biegu | `Odebrano` | `Kontrola: Dane` | Zakładka | Pliki spółek | Stróż |
|---|---|---|---|---|---|---|---|
| sob. 10.10 | 1224 | 1251 | 0 | 2370 | 2399 | 790 | #26 |
| niedz. 11.10 | 1252 | 1279 | 0 | 2370 | 2399 | 790 | #27 |
| pon. 12.10 | 1280 | 1307 | 3 | 2373 | 2402 | 791 | #28 |
| wt. 13.10 | 1308 | 1335 | 3 | 2376 | 2405 | 792 | #29 |
| śr. 14.10 | 1336 | 1363 | 3 | 2379 | 2408 | 793 | #30 |
| czw. 15.10 | 1364 | 1391 | 3 | 2382 | 2411 | 794 | #31 |
| pt. 16.10 | 1392 | 1419 | 3 | 2385 | 2414 | 795 | #32 |
| sob. 17.10 | 1420 | 1447 | 0 | 2385 | 2414 | 795 | #33 |
| niedz. 18.10 | 1448 | 1475 | 0 | 2385 | 2414 | 795 | #34 |
| pon. 19.10 | 1476 | 1503 | 3 | 2388 | 2417 | 796 | #35 |
| wt. 20.10 | 1504 | 1531 | 3 | 2391 | 2420 | 797 | #36 |
| śr. 21.10 | 1532 | 1559 | 3 | 2394 | 2423 | 798 | #37 |
| czw. 22.10 | 1560 | 1587 | 3 | 2397 | 2426 | 799 | #38 |
| pt. 23.10 | 1588 | 1615 | 3 | 2400 | 2429 | 800 | #39 |
| sob. 24.10 | 1616 | 1643 | 0 | 2400 | 2429 | 800 | #40 |
| niedz. 25.10 | 1644 | 1671 | 0 | 2400 | 2429 | 800 | #41 |

25.10 to pierwszy bieg po zmianie czasu. Linia startu ma wtedy `17:00:0X` UTC, a u stróża
zgłoszenie dalej ok. 18:30 polskiego.

### Wciąż otwarte

**Pełne opisy:** przegląd z 08.10. Decyzje Gracjana 08.10 (wszystkie w wariancie (a)), a 10.10
zmieniona kolejność: duża dokumentacja przed naprawami 1 i 2.

1. **Naprawa 1 — złe ceny Yahoo przy kilku nowych dniach naraz** (🔴 warunkowo).
   - Dobrą cenę ma tylko ostatnia świeca. Wcześniejsze dni tygodnia mają zamknięcie
     z poprzedniego piątku.
   - Zakres zapytania nic nie zmienia (09.10, `3y` = `5d`).
   - W piątek o 18:00 tydzień był jeszcze niepoprawiony (10.10).
   - **Zostaje zbadać:** kiedy Yahoo poprawia tydzień. Odczyt pamięci (krok 16 kontroli) po
     biegach 10, 11 i 12.10.
   - Potem jedna notatka projektowa na naprawy 1 i 2, pełna instrukcja, kod Gracjana i wdrożenie.
2. **Naprawa 2 — zapasowy adres brokera** w Producencie (`data_ingestion.py:16`). Brak
   `KAFKA_BOOTSTRAP` ma być głośnym błędem. Konsument (`kafka_consumer.py:7`) ma ten sam adres —
   do rozważenia w notatce.
3. **Git w OneDrive:** zostawione (decyzja 4). Przy pytaniu `Deletion of directory … (y/n)` po
   commicie: Ctrl+C. Commit jest już zrobiony, potem `git push`. 10.10: 755 luźnych obiektów,
   wszystkie w paczkach. Repozytorium nie przenosić, bo dziennik ma jedyną kopię w chmurze
   w OneDrive.
4. **Strona:** decyzje 06.10 niżej. Kod strony po naprawach 1 i 2, ustalenia wyglądu mogą iść
   wcześniej.
5. **Osobne decyzje, później:**
   - stary `venv` na EC2 (ok. 17.10);
   - aktualizacja Amazon Linux (nie w tygodniu 25.10);
   - zawężenie `AWSGlueConsoleFullAccess`;
   - Power BI na Athenę (sterownik ODBC na laptopie).

**Ograniczenia opisane w README** (decyzja 04.10, uzupełnione 10.10):
- kwadrans zapasu u Yahoo;
- poprawki Yahoo dni już wysłanych nie docierają do S3;
- `close()` bez `finally`;
- ostrzeżenia `pandas` i `value_deserializer` w logu;
- jedno źródło danych, bez planu B;
- nowa spółka wymaga ręcznych kroków (partycja w Athenie, okno `range=3y`);
- rozjazd nazw kolumn rankingu (plik a tabela);
- granice kontroli: zła cena przy dobrej dacie, ubytek u wszystkich spółek naraz, fałszywy alarm
  w święto;
- kompakcja ręczna; strażnik nie odróżni skasowanego pliku od nowej spółki; kopia ma jedno
  pokolenie;
- brak testów reszty Producenta.

**Niesprawdzone:**
- treść zgłoszenia #21 u stróża (polskie litery);
- czy port 9092 brokera jest otwarty dla laptopa;
- rozmiar `athena-results/`;
- liczba linii przy awarii Atheny na EC2 na 3.14.

### Terminy

- **ok. 17.10** — decyzja o starym `venv` na EC2, razem z nim `~/porownanie-1003/`. Dwa tygodnie
  spokoju na 3.14 mijają.
- **25.10 (niedziela)** — pierwszy bieg po zmianie czasu:
  - `17:00:0X` w linii startu i to jest poprawne;
  - u stróża pierwszy prawdziwy sprawdzian strefy.
- **26.10 (poniedziałek)** — pierwszy dzień giełdowy zimą: `nowych dni: 1` bez dopisku.
- **01.11** — Gold zmieni `117`/`111`. Przeliczyć przed biegiem, nie z pamięci.
- **początek listopada** — kompakcja za październik, z laptopa, nie między 17:55 a 18:35.
  Pierwsza z prawdziwym kasowaniem na nowym strażniku. Przewidywania z Atheny przed biegiem.
- **11.11 (środa)** — pierwszy fałszywy alarm kontroli w święto: mail `DOWN`, 12.11 `UP`.
- **19.02.2027** — koniec darmowego planu AWS albo wcześniej koniec kredytu. 04.10 zostało
  83,44 USD, „140 days remaining”. Przed tą datą decyzja: płatny plan, wyłączenie albo zmiana
  architektury.

### Codzienna kontrola po biegu (ułożona 20.09, przeliczona 21.09, 26.09 i 03.10)

Kiedy: po 18:32 polskiego, bo skrypt kontrolny kończy o 18:30, a Silver i Gold o
18:10. Godziny w logu są w UTC (patrz UWAGA wyżej). Przewidywania zapisać **przed**
puszczeniem komend. „Dzień giełdowy" to dzień z nowymi świecami, „weekend/święto" to
dzień bez. **Od 03.10 (Python 3.14) blok ma 28 linii w obu rodzajach dni**, więc zawsze
`tail -n 28`. Wcześniej: 32/30 (26.09–02.10), 29/27 (21–25.09). **Przy kontroli kilku dni
naraz** w krokach 5–7 brać wszystkie linie startu (`grep -n "=== Data pomiaru"
companies/errors.txt | tail -n N`, N = liczba dni) i porównać z tabelą „Przewidywania od
10.10” wyżej. Przy podawaniu kroków Gracjanowi kroki 1–2 są krokami
**PRZEŁĄCZENIE** (zasada 4), każda komenda w osobnym okienku.

1. **PRZEŁĄCZENIE [lokalny PowerShell, nowe okno, venv nieistotne]** `cd "C:\Users\gracj\OneDrive\Dokumenty\DE\GPW - pulse\aws\aws ec2 key"` — wiersz kończy się na `aws ec2 key>`.
2. **PRZEŁĄCZENIE [lokalny PowerShell, venv nieistotne]** `ssh -i "gpw-tracker-key.pem"
   ec2-user@13.63.105.190` — ma być wiersz `[ec2-user@ip-… ~]$`.
3. **[EC2, przez SSH]** `cd ~/GPW---pulse` — wiersz ma się kończyć na
   `GPW---pulse]$`.
4. **[EC2, przez SSH]** `date` — dzisiejszy dzień, UTC, po 16:32 (latem).
5. **[EC2, przez SSH]** `grep -n "=== Data pomiaru" companies/errors.txt | tail -n 2` —
   dwie ostatnie linie startu; dzisiejsza z `16:00:0X` (od 25.10 `17:00:0X`); jej numer =
   numer poprzedniej + rozmiar poprzedniego bloku **z linią `Kontrola:`** (21.09: 663).
6. **[EC2, przez SSH]** `wc -l companies/errors.txt` — numer dzisiejszej linii startu +
   rozmiar bloku z `Kontrola:` − 1 (od 03.10 blok 28, np. 03.10: 1028 + 28 − 1 = 1055).
7. **[EC2, przez SSH]** `tail -n 28 companies/errors.txt` — pierwsza linia to dzisiejszy
   start; 3 × `nowych dni: N, wysłane: N, stan: zapisane` (N = 1 albo 0), 2 linie
   `value_deserializer`, `Odebrano 3` albo `Odebrano 0`, 2 linie ostrzeżenia `pandas`
   z `silver.py`, 2 × `(M, 3)` **bez** linii `PythonDeprecationWarning` między nimi, tabela
   Golda, `Pełna liczba … 117, Prawidłowa … 111` (październik), ranking w 6 liniach,
   2 × `S3: wysłano`, brak `Traceback`, 2 linie ostrzeżenia `pandas` z `kod/path.py:32`,
   **przedostatnia `Kontrola: Dane M wierszy`, ostatnia `Kontrola: OK`**. M = poprzednie
   + 3 w dzień giełdowy, bez zmian w weekend (03.10: 2355). M w `Kontrola: Dane` = M
   w `(M, 3)` — to ta sama liczba z dwóch stron (plik Silvera i tabela w Athenie).
   Pojawienie się `PythonDeprecationWarning` znaczyłoby, że `cron` wrócił do starego `venv`.
8. **[EC2, przez SSH]** `grep -n -E "Traceback|Error|ERROR|nietknięte" companies/errors.txt`
   — nic.
9. **[EC2, przez SSH]** `wc -l companies/*.WA.txt` — po tyle wierszy, ile dni ma spółka
   (21.09: 776), +1 na dzień giełdowy; `total` = 3 × ta liczba. Maska `*.WA.txt` celowo
   omija `errors.txt`.
10. **[EC2, przez SSH]** `wc -l companies/errors.log` — 8, bez zmian (od 19.09 Producent
    pisze błędy do `errors.txt`).
11. **[EC2, przez SSH]** `~/kafka_2.13-4.3.1/bin/kafka-consumer-groups.sh
    --bootstrap-server localhost:9094 --describe --group gpw_consumer` — `CURRENT-OFFSET`
    = `LOG-END-OFFSET`, `LAG 0`; `no active members` jest normalne. Dzień giełdowy: +3
    względem poprzedniego (21.09: 2357).
12. **[konsola Athena w przeglądarce, region eu-north-1, baza `gpw-tracker_db`]**
    `SELECT spolka, COUNT(*) AS wiersze, COUNT(DISTINCT data) AS dni, MIN(data) AS od,
    MAX(data) AS do FROM gold_dane_dzienne GROUP BY spolka;` — 3 wiersze, `wiersze` = `dni`
    = liczba z kroku 9, `do` = ostatnia sesja (21.09: `2026-09-21 17:00:00`). Od 26.09
    liczbę wierszy daje też linia `Kontrola: Dane N wierszy` w logu; konsola Atheny
    potrzebna tylko do `od`/`do` albo przy rozjeździe.
13. **[EC2, przez SSH]** `aws s3 ls s3://gpw-tracker-bucket/gold/ --recursive` — dwa pliki
    z dzisiejszą datą i godziną `16:10` (UTC, bo z EC2; od 25.10 `17:10`). Rozmiar
    `dane_dzienne.csv`: 158692 B na 2370 wierszy (09.10), rośnie o ok. 64–73 B na wiersz (ok.
    +193–218 B na dzień giełdowy; krótkie ceny jak `200.0` dają mniej);
    `ranking.csv` 330–370 B. **Lokalnego pliku do porównania rozmiaru nie ma od 21.09**
    (Harmonogram wyłączony).
14. **[przeglądarka]** stróż: `Up`, ostatnie zgłoszenie ok. 18:30 (`Europe/Warsaw`), typ `GET`
    z `13.63.105.190`, `python-requests/2.34.2`, liczba zgłoszeń +1 na dzień (21.09: 3; 26.09
    po testach E4: 9; 06.10 `cron` #20, po teście `/fail` #22; 07.10 #23; 08.10 #24; 09.10 #25). Zrzuty przycinać bez pola z adresem zgłoszenia. Na Interii: żadnego
    `DOWN` (mail przychodzi ok. 15 minut po zmianie stanu).
15. **[EC2, przez SSH]** (od 22.09, po punkcie 6) `ls -a silver gold` — w każdym
    `.gitkeep` i pliki `.csv`; `git status --short` — pusty.
16. **[EC2, przez SSH]** (od 09.10, na czas badania punktu 1.1 przeglądu z 08.10)
    `tail -n 6 companies/*.WA.txt` — sześć ostatnich dni pamięci każdej spółki. Pamięć ma ceny
    z odpowiedzi Yahoo z 18:00. Szukamy dnia, w którym dni bieżącego tygodnia przestaną mieć
    piątkowe zamknięcie z poprzedniego tygodnia (08.10 i 09.10: za 05–08.10 CBF 201,0, SNT
    341,6, XTB 138,56; prawdziwe zamknięcia w „Na następną sesję”, punkt 1, i w archiwum GPW,
    adres w „Gdzie co jest”). Wynik zapisywać w dzienniku.

Przy rozjeździe: wkleić wynik, porównać liczba po liczbie, niczego nie uruchamiać
ponownie. To kontrola ręczna, która uzupełnia sygnał awarii, a go nie zastępuje: sygnał
(od 21.09 w `cron`) łapie brak zgłoszenia, `Traceback`, brak `stan: zapisane`, `Odebrano`
albo `S3: wysłano`, ale **nie** łapie złych danych przy udanym biegu ani braku świecy
w dzień giełdowy.

### Strona — decyzje 06.10

Pięć otwartych pytań z Plan-06 (wątek 4) rozstrzygniętych 06.10, wszystkie zgodnie z rekomendacją:
1. ogląda **każdy z linkiem, bez logowania** (ceny są publiczne, link trafi do README);
2. **skrypt w Pythonie składa gotowy plik HTML** — strona statyczna, bez aplikacji chodzącej 24/7
   na `t3.micro`;
3. wykresy w **Plotly** (interaktywne, bez pisania JavaScriptu); Power BI nie na stronę;
4. **najpierw plik na laptopie, potem GitHub Pages** (odświeżanie np. przez GitHub Actions
   z osobnym kluczem AWS tylko do odczytu `gold/`; strona przeżyje wyłączenie AWS 19.02.2027);
5. pierwsza wersja to **jedna strona**: kafelki (ostatnia cena, zmiana dzienna, data ostatniej
   świecy), wykres trzech spółek, ranking. Zakładki spółek i słownik później.

Następny krok: notatka projektowa (zasada 10), po zatwierdzeniu pełna instrukcja (zasada 3);
w niej instalacja Plotly w `.venv` i dopisanie do `requirements-lokalny.txt`. **Kod strony idzie
po naprawach 1 i 2 z przeglądu z 08.10** (decyzja 7). Duża dokumentacja zrobiona 10.10, przed
naprawami. Ustalenia wyglądu strony (bez kodu) mogą iść wcześniej — wybór Gracjana 10.10.

### Na następną sesję

Stan 10.10 (sobota, w trakcie sesji).
- **Zrobione:**
  - kontrola biegu 09.10, zgodna;
  - commit `5fa6098` (strażnik i dokumentacja 09.10), wypchnięty;
  - duża dokumentacja: README, ten plik, `Historia-stanu.md`.
- **Czeka:** odświeżone obrazki (bieg Gracjana na laptopie) i commit dużej dokumentacji.
- **Przed każdym kawałkiem kodu:** notatka projektowa (zasada 10) i pełna notatka-instrukcja
  (zasada 3). **Po każdej zmianie Gracjana:** opis każdej nowej linii (zasada 3).

0. **Na starcie:**
   - `git log -1` i `git status --short` na laptopie: commit jest, drzewo czyste, gałąź nie przed
     GitHubem;
   - `date`;
   - lista sesji: czy po ostatniej była jakaś bez dziennika.
1. **Kontrola biegów od 10.10** według tabeli „Przewidywania od 10.10”, **z krokiem 16** (pamięć
   spółek). Pytanie: czy i kiedy Yahoo poprawiło 05–08.10. Prawdziwe zamknięcia z GPW:
   - CBF 202,80 / 203,00 / 199,20 / 196,00;
   - SNT 339,80 / 343,80 / 342,20 / 342,80;
   - XTB 134,80 / 136,12 / 135,00 / 137,00.

   Pamięć ma ceny z ostatniego biegu, więc odczyt w niedzielę nie odróżni soboty od niedzieli,
   chyba że ktoś zajrzy w sobotę po 18:00.
2. **Notatka projektowa na naprawy 1 i 2**, gdy będzie wiadomo, kiedy Yahoo poprawia tydzień.
   Możliwości do opisania, między innymi:
   - przy kilku nowych dniach wysłać tylko ostatni i dać alarm;
   - starsze dni wstrzymać do poprawki;
   - przed 17:55 nie wysyłać nic.
3. **Strona — ustalenia wyglądu** (decyzje 06.10 niżej). Kod strony po naprawach 1 i 2.
4. **ok. 17.10:** decyzja o starym `venv` na EC2.
5. Terminy wyżej, w „Terminy”.

**EC2 jest na `5676575` od 07.10 18:57 UTC.** Laptop i GitHub są dalej:
- `5fa6098` — strażnik w `compaction.py`, który chodzi tylko z laptopa;
- notatki i dokumentacja.

Na EC2 nic z tego nie jest potrzebne, przyjdzie przy najbliższym wdrożeniu (naprawy 1 i 2).
Poprzednio EC2 było na: `4aca12d` od 03.10, `fc6e262` od 26.09, `6af7b48` od 21.09.

### Pomyłki Claude'a — wnioski

Pełna lista z datami: `notatki/plany/Historia-stanu.md`, sekcja „Pomyłki Claude'a”. Od 10.10
nowe pomyłki idą do dziennika dnia. Tutaj zostają wnioski, które obowiązują:

1. **Godzina tylko z `date`.** Dolną granicę liczyć od ostatniego odczytu + kilka minut, nigdy
   z szacunku tempa rozmowy (17.09, 21.09, 07.10, 08.10).
2. **Przewidywanie zapisać w wiadomości przed komendą** (20.09). Przewidywać liczby i słowa,
   nie układ linii (21.09).
3. **Przy `git commit` podawać sumę wszystkich plików w commicie**, przy `git diff plik` — liczbę
   dla pliku (17.09).
4. **Przewidywania na kilka dni zawsze jako tabela z wierszem na każdy dzień kalendarza**, także
   weekend. Nigdy jedna liczba na „następny dzień giełdowy” (25.09, 03.10).
5. **Przed rekomendacją naprawy otworzyć plik, którego dotyczy** (04.10). **Przed nazwaniem
   pojęcia „nowym” sprawdzić słownik** (26.09, 08.10). Przed stwierdzeniem, że plik nie istnieje,
   sprawdzić (04.10).
6. **Dziwną liczbę najpierw szukać w źródle** (archiwum GPW), dopiero potem stawiać hipotezę
   (08.10). Wartości z wyszukiwarki, przy których nie domyka się arytmetyka, nie podawać nawet
   jako poszlaki (17.09).
7. **Dziennik i CLAUDE.md pisać w dniu sesji, także gdy sesja się urwie.** Brak wpisu z dnia
   znaczy, że trzeba sprawdzić transkrypt (`list_events`), a nie zakładać, że nic się nie stało
   (21.09, 24.09, 09.10).
8. **Claude czyta stan gita, ale go nie zmienia.** Także `git add -N` jest zmianą (04.10).
9. **Zasady i nowe pojęcia podawać od razu, w pełnej instrukcji**, nie po kawałku przy ocenie
   kodu (23.09). Kroki krótkie, w kolejności, z PRZEŁĄCZENIEM i komendą w osobnym okienku
   (18.09, 25.09, 03.10).
10. **Jedno słowo na jedną rzecz** („skrypt kontrolny” i „stróż”, 18.09). Maile od stróża idą na
    **Interię**, nie na Gmaila (19.09).
11. **Bez form rodzajowych wobec Gracjana bez podstawy** (06.10).
12. **Przy hipotezie o zachowaniu kodu przeczytać kod**, zanim się przewidzi wynik. Przykład:
    cena w pamięci, której linia 62 nadpisuje stare wartości (08.10).

### Kopie

- **Pamięć Producenta:** `~/pamiec-kopia-0809/` (Windows).
- **Poprzedni `bronze`:** `bronze/poprzedni/` (poza gitem).
- **Na EC2:**
  - `~/crontab-kopia-0913.txt` to **jedyny** powrót do stanu sprzed
    `CRON_TZ`: `crontab ~/crontab-kopia-0913.txt`;
  - `~/crontab-kopia-0909.txt` to harmonogram sprzed 09.09 (cofnąłby o cztery
    dni);
  - `~/crontab-nowy.txt` to plik wgrany 09.09;
  - `~/crontab-nowy-0913.txt` to plik wgrany 13.09;
  - `~/crontab-kopia-0917.txt` to stan sprzed `GOLD_DO_S3` — powrót:
    `crontab ~/crontab-kopia-0917.txt`;
  - `~/crontab-nowy-0917.txt` to plik wgrany 17.09 (pięć linii);
  - `~/crontab-kopia-0919.txt` to stan pięciu linii z 19.09 (bez adresu
    stróża) — powrót sprzed sygnału awarii: `crontab ~/crontab-kopia-0919.txt`;
  - `~/crontab-nowy-0919.txt` to plik z `STROZ_URL` nad linią `0 18`
    i linią `30 18 … control.py` (siedem linii, `chmod 600`, **zawiera adres
    stróża** — nigdy do gita, nigdy na zrzut ekranu). Przygotowany 19.09,
    **wgrany 21.09 o 14:53:03 UTC (16:53 polskiego)** i był żywym `crontab` do 03.10.
    Powrót sprzed sygnału awarii: `crontab ~/crontab-kopia-0919.txt`;
  - `~/crontab-kopia-1003.txt` to stan sprzed Pythona 3.14 (siedem linii, stary `venv`,
    `chmod 600`, **zawiera adres stróża**) — powrót do Pythona 3.9: `crontab
    ~/crontab-kopia-1003.txt`;
  - `~/crontab-nowy-1003.txt` (siedem linii, `venv314`, `chmod 600`, **zawiera adres
    stróża**) — wgrany 03.10, `RELOAD` 09:45:01 UTC, **od tego dnia żywy `crontab`**;
  - stary `~/GPW---pulse/venv` (Python 3.9.25) — nietknięty, do skasowania najwcześniej
    ok. 17.10; `~/porownanie-1003/` — trzy pliki Silver/Gold ze starego `venv` z 03.10.

## Gdzie co jest

Kod, dane i notatki razem w folderze projektu: `kod/`, `companies/`
(pamięć Producenta, **poza gitem**, każda maszyna ma własną), `bronze/`
(poza gitem), `silver/`, `gold/` (**od 21.09 poza gitem**, w folderach tylko `.gitkeep`;
dawniej w gicie, do czasu, gdy wynik trafi
do S3), `wykresy/`, `notatki/`, `aws/` (klucz SSH, poza gitem). Skrypt
kontrolny (od 18.09): `kod/control.py`, testy `kod/test_control.py`, wzór
prawdziwego bloku logu `kod/dane_testowe/blok_2026-09-18.txt`. Testy
uruchamiane z folderu projektu: `pytest kod/test_control.py -v`. Test prawdziwej
drogi (od 23.09): `kod/path.py`, testy `kod/test_path.py` (`pytest kod/test_path.py -v`),
bieg na Athenie z laptopa `python kod/path.py`, udawany dzień
`$env:DROGA_DATA = "RRRR-MM-DD"` (potem `Remove-Item Env:DROGA_DATA`). Od 25.09
`control.py` importuje z `path.py` `sprawdz_daty` i `pobierz_dane`, więc testy obu plików
uruchamiać razem: `pytest kod/test_path.py kod/test_control.py -v` (18 testów). Ręczny bieg
`control.py` na laptopie: `KONTROLA_LOG` = `kod\dane_testowe\blok_2026-09-18.txt`,
`KONTROLA_DATA` = `2026-09-18`; awaria Atheny wymuszana zmyślonymi `AWS_ACCESS_KEY_ID`
i `AWS_SECRET_ACCESS_KEY` w oknie (po teście usunąć i sprawdzić `Get-ChildItem Env:`).
**Ręczny bieg `control.py` na EC2** (od 26.09), z `~/GPW---pulse`, **bez `>>`** (wynik tylko na
ekran, log nietknięty): `KONTROLA_DATA=RRRR-MM-DD venv314/bin/python kod/control.py` (od 03.10
`venv314`; wcześniej `venv`) — zmienna
przed komendą działa tylko dla niej. Przed 18:30 brać ostatni dzień z biegiem (dzisiejszego
bloku jeszcze nie ma). Awaria Atheny: dopisać przed komendą zmyślone `AWS_ACCESS_KEY_ID=…
AWS_SECRET_ACCESS_KEY=…`. Ze stróżem: `export STROZ_URL=$(crontab -l | grep '^STROZ_URL=' |
cut -d= -f2-)`, sprawdzić `echo ${#STROZ_URL}` → `56`, po testach `unset STROZ_URL` → `0`.
Każde zgłoszenie ręczne przesuwa numery u stróża. **Od 03.10 wszystkie testy jedną komendą:**
`pytest kod/ -v` (od 06.10 28 testów: 11 w `test_control.py`, 7 w `test_path.py`, 10
w `test_session.py`; `test_plikow.py` usunięty) — **z włączonym `(.venv)`**, bo Python systemowy na laptopie nie ma `pyathena`.
**Wykresy** (od 03.10 z Atheny, tylko laptop, `(.venv)` włączone): `python kod/wykresy.py`
(`Wiersze: N, stan na: RRRR-MM-DD`, obrazek `wykresy/wykres3spolek.png`) i `python
kod/ranking.py` (tabela 3 spółek malejąco, `stan na: …`, `wykresy/ranking.png`). Bez dostępu
do Atheny padają z błędem i nie nadpisują obrazka. Nauka Pythona (osobny projekt): `DE/Python_l/`.
**Archiwum notowań GPW** (punkt odniesienia dla cen, od 18.09): jeden dzień, wszystkie akcje —
`https://www.gpw.pl/archiwum-notowan?fetch=0&type=10&instrument=&date=DD-MM-RRRR`, kurs zamknięcia
w szóstej kolumnie (CBF to wiersz `CYBERFLKS`, SNT `SYNEKTIK`). Claude czyta je narzędziem
w przeglądarce. Archiwum z dzisiejszego dnia o 18:48 jeszcze puste (08.10).

**Co z `notatki/` jest w gicie, sprawdzone 11.09.** `notatki/plany/`
i `notatki/Slownik.md` **są śledzone**. Poza gitem, przez `.gitignore`, są
`notatki/dziennik/` i `notatki/.obsidian/`. Znaczy to, że **wszystkie wpisy
dziennika (51 plików na 10.10), czyli cały zapis nauki z tego projektu,
istnieją wyłącznie na laptopie i w OneDrive, ani jeden nie jest
w repozytorium**. **Decyzja Gracjana 06.10: zostaje tak** — dziennik tylko lokalnie (laptop
i OneDrive), poza gitem. Świadomy koszt: jedna kopia, w zamian prywatność.

**Środowiska Pythona.**
- **Laptop:** `.venv` (z kropką), Python 3.14.2, spis
  `requirements-lokalny.txt` (32 paczki).
- **EC2 od 03.10:** `venv314`, Python 3.14.6 (z `dnf`, wołany jako `python3.14`), spis
  `requirements-ec2.txt` (18 paczek, wersje z laptopa przez `-c requirements-lokalny.txt`,
  `pandas` 3.0.5, `boto3` 1.43.75, `urllib3` 2.7.0). Systemowy `python3` zostaje 3.9.25 —
  używa go sam system (`dnf`), **nigdy go nie podmieniać**. Stary `venv` (bez kropki, 3.9.25)
  stoi nietknięty do ok. 17.10. W Amazon Linux 2023 (`2023.12.20260817`) do wzięcia są
  3.11–3.14, 3.10 nie ma.
- Pliku `requirements.txt` **celowo nie ma**. To konwencja, z której ktoś
  odruchowo zainstalowałby zły zestaw.
- `crontab` i `pipeline.bat` wołają Pythona pełną ścieżką z `venv`, bez
  aktywacji.
- Folderu z `venv` nie przenosić: w środku są zapisane pełne ścieżki
  (EC2, 31.08).

**EC2:**
- połączenie z folderu `aws\aws ec2 key`:
  `ssh -i "gpw-tracker-key.pem" ec2-user@13.63.105.190`;
- repo `~/GPW---pulse`, Python `~/GPW---pulse/venv314/bin/python` (od 03.10);
- log `cron`: `~/GPW---pulse/companies/errors.txt`;
- narzędzia Kafki `~/kafka_2.13-4.3.1/bin/`, broker `localhost:9094`,
  topic `gpw_tracker`, grupa `gpw_consumer`;
- ręczny bieg Producenta albo Konsumenta **tylko** z
  `KAFKA_BOOTSTRAP=localhost:9094` przed komendą.

**S3** (z laptopa, narzędzie `aws` zainstalowane): bucket
`gpw-tracker-bucket`, podgląd `aws s3 ls s3://gpw-tracker-bucket/live/
--recursive --summarize`.

**Athena:** baza `gpw-tracker_db`, region `eu-north-1`, wyniki zapytań
w `s3://gpw-tracker-bucket/athena-results/` (konsola ma własne ustawienie,
niezależne od `silver.py`). Cztery tabele:

| Tabela | Czyta | Format |
|---|---|---|
| `bronze` | `bronze/`, partycje `spolka`, `data` | Parquet |
| `live` | `live/`, partycje `spolka` | JSON |
| `gold_dane_dzienne` | `gold/dane_dzienne/` | CSV z nagłówkiem, 5 kolumn |
| `gold_ranking_spolek` | `gold/ranking/` | CSV z nagłówkiem, 7 kolumn |

Obie tabele `gold_*` założone 16.09 ręcznie, z pominięciem pierwszej linii
(`skip.header.line.count`). Kolumny Athena dopasowuje **po kolejności**,
nie po nazwie, więc **każda zmiana kolumn w `gold.py` wymaga zmiany tabeli
w tej samej sesji**. Do folderów tabel nic nie wgrywamy ręcznie — każdy
dodatkowy plik po cichu dokłada wiersze.

**Kolumny `gold_ranking_spolek` (stan 17.09):** `spolka`, `miesiac`,
`odchylenie_standardowe`, `dni`, `pierwotna_cena`, `aktualna_cena`,
`zmiana_caly_okres`. Dwie ostatnie nazwy zmienił Gracjan 17.09
(`ALTER TABLE … CHANGE COLUMN`) z `pierwsza_cena` i `ostatnia_cena`.
**Plik CSV w S3 ma nadal stare nazwy w nagłówku** — nie szkodzi, bo nagłówek
jest pomijany, ale przy czytaniu pliku i tabeli obok siebie widać rozjazd.

**Zmiana nazwy kolumny w Athenie nie rusza danych.** Trzy drogi:
`ALTER TABLE … CHANGE COLUMN stara nowa typ` (typ trzeba podać, nawet
niezmieniony), `ALTER TABLE … REPLACE COLUMNS (…)` dla kilku naraz, albo
`DROP TABLE` i `CREATE EXTERNAL TABLE` od nowa. Przy tabeli `EXTERNAL`
`DROP` kasuje sam opis, pliki w S3 zostają. **Niesprawdzone:** jak
`CHANGE COLUMN` zachowa się na `bronze` — Parquet trzyma nazwy kolumn
w samym pliku, więc dopasowanie może iść po nazwie, nie po pozycji.
