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

## Stan projektu — uczciwie (21.09 wieczorem)

Repo: `GPW - pulse`, GitHub `github.com/gracjan20022002-prog/GPW---pulse`.
**Źródło prawdy o wadach i kolejności napraw:**
[`notatki/plany/Przeglad-2026-09-08-co-nie-gra.md`](notatki/plany/Przeglad-2026-09-08-co-nie-gra.md),
nie README.

### Jak dziś płyną dane, sprawdzone

Na EC2 (`t3.micro`, Elastic IP `13.63.105.190`, 24/7) `cron` uruchamia
codziennie **o 18:00 czasu polskiego** jedną linię
`data_ingestion.py ; kafka_consumer.py` i **o 18:10** `silver.py &&
gold.py`, a **od 21.09 o 18:30** skrypt kontrolny `control.py`. Od 13.09 na górze
`crontab` stoi `CRON_TZ=Europe/Warsaw`, więc
godziny w pliku (`0 18`, `10 18`) są polskie przez cały rok. Sprawdzone
wpisem `RELOAD` w dzienniku systemowym i biegami 13.09 (niedziela) oraz
14.09 (dzień giełdowy). Pełny tekst `crontab`:
`notatki/plany/Notatka-2026-09-13-strefa-czasowa-cron.md`, część 4 (stan z 13.09).
**Od 21.09 `crontab` ma siedem linii:** `CRON_TZ`, `KAFKA_BOOTSTRAP`, `GOLD_DO_S3`,
`STROZ_URL` (adres stróża, **nigdy w gicie**), `0 18`, `10 18` i `30 18` (skrypt
kontrolny). Wgrany 21.09 o 14:53:03 UTC (16:53 polskiego).

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
  **Od 17.09 na EC2:** `enable_auto_commit=False` w konstruktorze
  i `consumer.close()` w ostatniej linii. Zakładka przesuwa się **tylko** po
  udanym zapisie do S3 — wcześniej biblioteka zapisywała ją sama co 5 s,
  w trakcie pętli, czyli przed zapisem. Dowody, testy i ograniczenia:
  `notatki/plany/Notatka-2026-09-17-zakladka-przed-zapisem.md`.
  **Uwaga:** `close()` stoi za `put_object`, więc przy awarii zapisu się nie
  wykonuje i broker przez kilkanaście sekund widzi martwego członka grupy.
  To blokuje `--reset-offsets`, który wymaga grupy nieaktywnej.
  **18.09 pierwszy bieg z `cron` na nowym Konsumencie:** `Odebrano 3
  wiadomości`, blok zgodny co do linii. Zakładka odczytana 20.09: `2354 2354 0`
  i `no active members` — stan zostawiony przez bieg piątkowy, bo w weekend
  nic nie wpadło.
- **Silver** (`silver.py`): Athena `bronze UNION live`, odsiewa powtórzone
  dni → `silver/clean_data.csv` na dysku EC2.
- **Gold** (`gold.py`): zmiany procentowe i ranking „najbardziej zmiennego
  **pełnego** miesiąca" (bez pierwszego i ostatniego miesiąca historii
  spółki i bez miesięcy poniżej 15 dni notowań) → `gold/*.csv` na dysku EC2.
  **Na EC2 od 17.09, działa z `cron`:** po zapisie na dysk, gdy zmienna
  `GOLD_DO_S3` jest równa `1`, wysyła oba pliki do S3
  (`gold/dane_dzienne/dane_dzienne.csv`, `gold/ranking/ranking.csv`) i pisze
  `S3: wysłano …` na plik; bez zmiennej pisze
  `S3: Pominięto, brak GOLD_DO_S3 == 1`. Zmienna stoi w `crontab` na górze,
  pod `KAFKA_BOOTSTRAP` — musi być **nad** linią `10 18`.
- **`bronze`** w S3 to Parquet do końca poprzedniego miesiąca, przepisywany
  ręcznie przez `compaction.py`, **wyłącznie z laptopa** (pierwszy bieg
  z prawdziwym kasowaniem: 1 października).
- **Lokalny Harmonogram Windows (WYŁĄCZONY 21.09)** liczył Silver+Gold równolegle o 18:10 jako
  „zapas" (`kod/pipeline.bat`, pełne ścieżki do `.venv\Scripts\python.exe`).
  Od 15.09 z nowym `gold.py`, bez przełącznika, więc nic nie wysyłał do S3.
  **21.09:** zadanie `GPW Pulse - pipeline` (codziennie od 02.09 o 18:10, akcja
  `cmd.exe /c … kod\pipeline.bat`) ma stan `Disabled`; wraca komendą
  `Enable-ScheduledTask`. `kod/pipeline.bat` zostaje w gicie.
- **Silver i gold poza gitem (od 21.09, commit `6af7b48`).** `.gitignore` ma
  `silver/*`, `!silver/.gitkeep`, `gold/*`, `!gold/.gitkeep`; w obu folderach leży
  pusty `.gitkeep`, bo git nie trzyma pustych folderów, a `silver.py` i `gold.py`
  nie zakładają folderu (`to_csv`). EC2 na `6af7b48` od 21.09 ok. 19:03, w folderach
  sam `.gitkeep`; pliki `.csv` wracają z pierwszym biegiem o 18:10 (**sprawdzian
  22.09**). Lokalne pliki stoją od 20.09 20:22:04. Notatka:
  `notatki/plany/Notatka-2026-09-21-jedno-miejsce-liczenia.md`.

**Normalny blok jednego biegu w `errors.txt`, stan od 17.09:**
- w dzień giełdowy **28 linii**: Producent 4, ostrzeżenie `kafka-python` 2,
  `boto3` 2, `Odebrano` 1, `pandas` 2, Silver 1, Gold 12, ostrzeżenie
  `boto3` w Goldzie 2 (osobny program), 2 × `S3: wysłano`;
- bez nowych wiadomości **26 linii**, bo Konsument tworzy klienta S3,
  a z nim ostrzeżenie `boto3`, tylko wtedy, gdy ma co zapisać.
- Zmiany w Konsumencie z 17.09 **nie dodają ani nie ujmują linii**. Gdyby
  blok się zmienił, znaczyłoby to, że zmieniło się coś jeszcze.
- **Od 21.09** po bloku z 18:00 dochodzi jedna linia skryptu kontrolnego z 18:30
  (`Kontrola: OK`): w dzień giełdowy **29 linii**, bez nowych wiadomości **27**.
  Potwierdzone 21.09 (start w linii 663, `Kontrola: OK` w linii 691). Przy
  martwym brokerze blok urośnie o 4 linie `ERROR` (trzy z biblioteki Kafki, jedna
  nasza).

Stan 20.09 wieczorem, odczytany na EC2 i w Athenie: `errors.txt` **662
linie**. Linie startu biegów: 441 (12.09), 462, 483, 507, 531, 555, 583
(18.09), 611, 637 (20.09), wszystkie `16:00:02` UTC — jeden bieg na dzień,
bez dziury. Rozmiary bloków 21, 21, 24, 24, 24, 28, 28, 26, 26; skoki mają
wyjaśnienie: Gold z pełnymi miesiącami +1 linia (od 14.09), zmiany z 17.09
+4 (dwie linie `boto3` w Goldzie i dwa razy `S3: wysłano`), a weekend po
17.09 to 22 + 4. 18.09 Silver i Gold po `(2325, 3)`: trzy powtórki z testu
B (17.09) odsiane, jak przewidzieliśmy. Weekend bez sesji (19 i 20.09):
3 × `nowych dni: 0`, `Odebrano 0 wiadomości`, 2 × `(2325, 3)`,
2 × `S3: wysłano`. Zakładka `2354 2354 0`, pliki spółek po 775, `COUNT(*)`
na `gold_dane_dzienne` 2325 (po spółce 775 dni od 2023-08-14 do
2026-09-18). W S3 `gold/` oba pliki z 20.09 16:10:07 UTC (odczyt z EC2);
`dane_dzienne.csv` 155560 bajtów = lokalny 157886 − 2326 linii (Windows
kończy linię dwoma znakami, Linux jednym), `ranking.csv` 360 = 364 − 4.
**Zero linii `Traceback`, `Error`, `ERROR`, `nietknięte` w całym pliku.**
Log przed linią 441 ma stary kształt bez linii startu, więc biegów sprzed
12.09 tą metodą nie liczymy. Ranking bez zmian: CBF 202,80, SNT 352,60,
XTB 150,34. `errors.log` 8 (stan z 17.09; potwierdzone 21.09). W `live/`
trzy powtórki z testu B — kompakcja 1.10 wypisze o trzy pliki więcej.

**Stan 21.09 wieczorem** (dzień giełdowy, po pierwszym biegu skryptu kontrolnego z
`cron`): `errors.txt` **691** linii; start biegu w linii **663** (`16:00:02` UTC), blok
28 linii (663–690), `Kontrola: OK` w linii 691 (18:30:02 polskiego); Silver i Gold po
`(2328, 3)`; zakładka `2357 2357 0`, `no active members`; pliki spółek po 776 (razem
2328); `COUNT(*)` na `gold_dane_dzienne`: 776 dni na spółkę, `do` = `2026-09-21
17:00:00`; S3 `gold/` z 16:10:07 UTC: `dane_dzienne.csv` 155778 B, `ranking.csv`
359 B (lokalnego pliku do porównania rozmiaru już nie ma). `errors.log` 8. Zero linii
`Traceback`, `Error`, `ERROR`, `nietknięte`. Ranking: CBF 212,80, SNT 351,40, XTB
148,58 — zgodne z archiwum GPW (odczyt narzędziem, streszczenie strony; procenty
+4,93 / −0,34 / −1,17 zgodne z liczonymi od cen z 18.09).

**Kompletność sesji** (lokalny `gold/dane_dzienne.csv`, rozmiar zgodny
z S3 po odjęciu końców linii): po 775 unikalnych dni na spółkę, te same
daty u wszystkich trzech, 810 dni roboczych − 35 świąt = 775. Wszystkie 35
przerw to święta lub dni bez sesji (24.12 i 31.12 z pamięci, nie
z kalendarza GPW). Największy skok dzienny −16,4% (SNT 30.06.2025);
pojedynczych skoków nie porównywaliśmy z archiwum. **Niepotwierdzone
zewnętrznie:** ceny sprzed 14.09, poza CBF z 14–17.09 oraz SNT i XTB
z 17.09; ceny z 18.09 i z 21.09 potwierdzone w archiwum GPW (przez narzędzie, nie
własnym okiem). **Lokalny `gold/dane_dzienne.csv` stoi od 20.09** (Harmonogram
wyłączony), więc kompletność od 22.09 liczyć przez Athenę albo z pliku pobranego
z S3.

### Codzienna kontrola po biegu (ułożona 20.09, przeliczona 21.09)

Kiedy: po 18:32 polskiego, bo skrypt kontrolny kończy o 18:30, a Silver i Gold o
18:10. Godziny w logu są w UTC (patrz UWAGA wyżej). Przewidywania zapisać **przed**
puszczeniem komend. „Dzień giełdowy" to dzień z nowymi świecami, „weekend/święto" to
dzień bez. Od 21.09 blok ma **29 linii** w dzień giełdowy (28 + `Kontrola: OK`) i **27**
w weekend/święto (26 + `Kontrola:`).

1. **[lokalny PowerShell, venv nieistotne]** `cd "C:\Users\gracj\OneDrive\Dokumenty\DE\GPW - pulse\aws\aws ec2 key"`.
2. **[lokalny PowerShell, venv nieistotne]** `ssh -i "gpw-tracker-key.pem"
   ec2-user@13.63.105.190` — ma być wiersz `[ec2-user@ip-… ~]$`.
3. **[EC2, przez SSH]** `cd ~/GPW---pulse` — wiersz ma się kończyć na
   `GPW---pulse]$`.
4. **[EC2, przez SSH]** `date` — dzisiejszy dzień, UTC, po 16:32 (latem).
5. **[EC2, przez SSH]** `grep -n "=== Data pomiaru" companies/errors.txt | tail -n 2` —
   dwie ostatnie linie startu; dzisiejsza z `16:00:0X` (od 25.10 `17:00:0X`); jej numer =
   numer poprzedniej + rozmiar poprzedniego bloku **z linią `Kontrola:`** (21.09: 663).
6. **[EC2, przez SSH]** `wc -l companies/errors.txt` — numer dzisiejszej linii startu +
   rozmiar bloku z `Kontrola:` − 1 (21.09: 663 + 29 − 1 = 691).
7. **[EC2, przez SSH]** `tail -n 29 companies/errors.txt` w dzień giełdowy, `tail -n 27`
   w weekend/święto — pierwsza linia to dzisiejszy start; 3 × `nowych dni: N, wysłane: N,
   stan: zapisane` (N = 1 albo 0), `Odebrano 3` albo `Odebrano 0`, 2 × `(M, 3)`,
   2 × `S3: wysłano`, brak `Traceback`, **ostatnia linia `Kontrola: OK`**. M = poprzednie
   + 3 w dzień giełdowy, bez zmian w weekend (21.09: 2328).
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
    = liczba z kroku 9, `do` = ostatnia sesja (21.09: `2026-09-21 17:00:00`).
13. **[EC2, przez SSH]** `aws s3 ls s3://gpw-tracker-bucket/gold/ --recursive` — dwa pliki
    z dzisiejszą datą i godziną `16:10` (UTC, bo z EC2). Rozmiar `dane_dzienne.csv`: 155778 B
    na 21.09, rośnie o ok. 73 B na wiersz (ok. +220 B na dzień giełdowy); `ranking.csv`
    ok. 360 B. **Lokalnego pliku do porównania rozmiaru nie ma od 21.09** (Harmonogram
    wyłączony).
14. **[przeglądarka]** stróż: `Up`, ostatnie zgłoszenie ok. 18:30 (`Europe/Warsaw`), typ `GET`
    z `13.63.105.190`, liczba zgłoszeń +1 na dzień (21.09: 3). Zrzuty przycinać bez pola
    z adresem zgłoszenia.
15. **[EC2, przez SSH]** (od 22.09, po punkcie 6) `ls -a silver gold` — w każdym
    `.gitkeep` i pliki `.csv`; `git status --short` — pusty.

Przy rozjeździe: wkleić wynik, porównać liczba po liczbie, niczego nie uruchamiać
ponownie. To kontrola ręczna, która uzupełnia sygnał awarii, a go nie zastępuje: sygnał
(od 21.09 w `cron`) łapie brak zgłoszenia, `Traceback`, brak `stan: zapisane`, `Odebrano`
albo `S3: wysłano`, ale **nie** łapie złych danych przy udanym biegu ani braku świecy
w dzień giełdowy.

### Kolejność napraw — gdzie jesteśmy

Kolejność z Części 5 przeglądu, zatwierdzona 08.09.

1. **Producent nie gubi danych** — ✅ 08.09.
2. **Strażnik kompakcji** — ✅ 08.09.
3. **Konsument `earliest` i jedna linia `crontab`** — ✅ 08–10.09.
   **Ścieżka bez zakładki sprawdzona testem 14.09, Silver na EC2 potwierdził
   15.09** (`(2316, 3)`, powtórki nie dodały wiersza).
   **Domknięty głębiej 17.09:** naprawione gubienie danych przy **awarii**
   zapisu do S3. Wada dopisana 14.09 jako podejrzenie, 17.09 potwierdzona
   w kodzie `kafka-python 3.0.11`, pokazana na żywo (zakładka przeskoczyła
   2348 → 2351 przy pustym `live/`), naprawiona przez
   `enable_auto_commit=False` + `consumer.close()`. Dwa testy po zmianie:
   zapis odcięty → zakładka **stoi** (`2348 2351 3`); bieg zwykły →
   `Odebrano 3`, `2351 2351 0`, `no active members` od razu. **18.09
   pierwszy bieg z `cron`:** blok 28 linii, `Odebrano 3`, 2 × `(2325, 3)`,
   zgodnie z przewidywaniem. **Trzy odczyty domknięte 20.09:** zakładka
   `2354 2354 0`, pliki spółek po 775, `COUNT(*)` 2325 — wszystkie trzy jak
   przewidzieliśmy.
4. **Sprzątanie kodu** — ✅ 11.09 na EC2. Do tego:
   - podsumowanie Producenta, ✅ trzy ścieżki: awaria brokera 11.09
     lokalnie, „nic nowego" 12.09 na EC2, dzień giełdowy 14.09 na EC2;
   - spisy wymagań dla dwóch maszyn, ✅ 11.09;
   - `CRON_TZ`, ✅ 13–14.09.
5. **Wynik Golda do S3 i Atheny** — ✅ **17.09**. Notatka
   `notatki/plany/Notatka-2026-09-15-wynik-golda-do-s3.md` zatwierdzona (pięć
   decyzji: nadpisywać, CSV, przełącznik tylko na EC2, tabele ręcznie SQL,
   bez kolumny z godziną). Przełącznik w `gold.py` napisany przez Gracjana.
   Tabele w Athenie założone ręcznie 16.09. **17.09:** kod na EC2
   (`git pull` do `070b478`), `GOLD_DO_S3=1` w `crontab` z `REPLACE`
   14:59:47 UTC i `RELOAD` 15:00:01 UTC, bieg z `cron` o 18:10 polskiego
   wypisał 2 × `S3: wysłano`, a `COUNT(*)` na `gold_dane_dzienne` dał
   **2322** zamiast 2316. **To ta liczba jest dowodem** — plik policzony
   przez `cron` sam przeszedł do S3 i Athena go czyta.
   **Niespełniony tylko warunek (c):** awaria nadal cicha.
6. **Wyłączenie lokalnego Harmonogramu, `silver/` i `gold/` poza gitem** — 🟨 **21.09
   wdrożone na laptopie i EC2, sprawdzian 22.09 o 18:10.** Notatka
   `notatki/plany/Notatka-2026-09-21-jedno-miejsce-liczenia.md` zatwierdzona: cztery
   decyzje zgodnie z rekomendacją (`.gitkeep`, wyłączenie a nie usunięcie zadania,
   `pipeline.bat` zostaje, historia gita nietknięta), piąta (termin): laptop od razu, EC2
   po potwierdzeniu 18:30 (tego samego wieczoru). Laptop: `.gitignore` z wyjątkiem
   `.gitkeep`, `git rm --cached`, commit `6af7b48` (`6 files changed, 4 insertions(+),
   4656 deletions(-)`, zgodnie z przewidywaniem), zadanie `GPW Pulse - pipeline` w stanie
   `Disabled`. Próba na klonie testowym zgodna (bez rytuału `pull` się przerywa, po
   rytuale kasuje pliki, foldery z `.gitkeep` zostają). EC2: rytuał i `pull` do `6af7b48`,
   sześć przewidywań zgodnych, w `silver/` i `gold/` sam `.gitkeep`. **Brakuje:** biegu
   z `cron` o 18:10 22.09 na odtworzonych folderach; przepięcia wykresów, `ranking.py`,
   `test_plikow.py` i Power BI (czytają lokalne pliki, stojące od 20.09); zmiany zasady
   14 po sprawdzianie.
7. **Test prawdziwej drogi** — ⬜ następny w kolejce; miał iść na końcu, gdy kształt
   łańcucha jest ostateczny, czyli po sprawdzianie punktu 6.
8. **Sygnał awarii** — ✅ **21.09, z zastrzeżeniami**, wzięty przed 6 i 7 decyzją Gracjana
   18.09. Notatka zatwierdzona, `control.py` i 11 testów, 19.09 kod na EC2 i testy 2–3
   z prawdziwym stróżem, 21.09 linia `30 18` w `crontab` (16:53 polskiego), test ciszy
   (mail `DOWN` 19.09 19:00:00 +0200) i pierwszy bieg z `cron` o 18:30:02 zgodny
   z przewidywaniem (start w linii 663, `wc -l` 691, `Kontrola: OK`, stróż `#3 OK`,
   `down → up`). Warunki (a)–(d) spełnione jednym biegiem, (e) niniejszy opis.
   **Zastrzeżenia:** to jeden bieg, nie tydzień; głośna awaria pokazana na dwóch testach
   wymuszonych, nie na prawdziwej awarii potoku; sygnał nie łapie złych danych przy
   udanym biegu, braku świecy w dzień giełdowy (wygląda jak sobota) ani lokalnych rzeczy;
   strefę sprawdzi dopiero 25.10; zależy od jednej osoby po stronie stróża. Skutek dla
   reszty listy: każde ✅ wyżej miało niespełniony warunek (c) — od 21.09 awaria w zakresie
   sygnału jest głośna (mail). Stan szczegółowo niżej, w „Sygnał awarii — stan 21.09
   wieczorem".
9. **Pełne miesiące w rankingu** — ✅ 12.09 lokalnie, 14.09 na EC2, wzięte
   poza kolejnością.
10. **Dokumentacja** — ⬜ w tle: README od nowa, dziesięć wpisów dziennika
    bez „Czego się nauczyłem", plany do posprzątania.

### Sygnał awarii — stan 21.09 wieczorem

Notatka: `notatki/plany/Notatka-2026-09-18-sygnal-awarii.md`, **zatwierdzona w całości**,
wyniki testów dopisane 21.09. Dwa słowa, żeby się nie mylić: **skrypt kontrolny** to nasz
skrypt na EC2, który ocenia dzisiejszy blok; **stróż** to usługa poza EC2 (healthchecks.io),
która czeka na zgłoszenie i pisze e-mail, gdy nie przyjdzie albo przyjdzie z awarią.

- **Decyzje:** stróż zewnętrzny, plan darmowy (nie SNS — sama SNS nie złapie martwego EC2 ani
  niedziałającego `cron`); „dowód sukcesu" zamiast szukania złych słów: `stan: zapisane` przy
  każdej spółce z `config.ticker`, `Odebrano`, 2 × `S3: wysłano`, zero `Traceback`; Producent
  pisze błędy do `errors.txt` (koniec osobnego `errors.log`); adres zgłoszenia jako `STROZ_URL`
  w `crontab`, **nigdy w gicie**; skrypt kontrolny o 18:30 polskiego, zapas 30 minut, strefa
  `Europe/Warsaw` w stróżu (nie UTC — inaczej 25.10 fałszywy alarm).
- **U stróża:** konto założone przez Gracjana. Zadanie `GPW - bieg dzienny` (Cron `30 18 * * *`,
  `Europe/Warsaw`, Grace 30 min, e-mail na Interię włączony dla zadania) — ustawienia
  potwierdzone 19.09 zrzutami. **Historia zdarzeń (zrzut 21.09):** 19.09 14:17 `new → down`
  i `down → up` (dwa testy z EC2: awaria, potem OK), **19.09 19:00 `up → down` (cisza; test 4
  z notatki zaliczony, strefa polska)**, 21.09 18:30 `down → up` (`#3 OK`, `GET` z
  `13.63.105.190`). Stróż pisze tylko przy zmianie stanu (dwa dni ciszy dały jeden mail). Mail
  `UP` 21.09: „downtime lasted 1 day, 23 hours", `Status Changed to Up at … 18:30:02 +0200`.
  Hipoteza z 19.09 o ok. 15-minutowym opóźnieniu maili z Interii — niepotwierdzona (godziny
  przyjścia maili z 21.09 nie zapisano). Konto bez logowania przez rok jest kasowane. Obsługa
  stróża to jedna osoba — sami piszą, że możliwe są przerwy wielodniowe. Adres zgłoszenia
  pojawił się 19.09 w rozmowie (odczyt `control.py`, zrzut ekranu) — ryzyko małe; przy
  podejrzeniu wycieku nowe zadanie z nowym adresem. Zrzuty z 21.09 były przycięte bez pola
  z adresem.
- **Kod:** `kod/control.py` — `sprawdz_blok(blok, spolki, dzis)` zwraca listę problemów,
  `wytnij_blok(tekst)` wycina blok od ostatniej linii startu i odsiewa linie zaczynające się
  od `Kontrola:`, część główna (patrz niżej); `kod/test_control.py` — 11 testów na prawdziwym
  bloku z 18.09 (`kod/dane_testowe/blok_2026-09-18.txt`), `11 passed` (wynik wklejony 19.09).
  **Wyjaśnienie testów zrobione 19.09**, dwa razy: tabela 8 + 3 testów, potem kod linia po
  linii i każdy test z przebiegiem; Gracjan: „wszystko już rozumiem". Nazwa `control.py`, nie
  `kontrola.py` z notatki — wybór Gracjana.
- **Dwie pułapki znalezione 18.09, obie w notatce:**
  - komunikaty skryptu kontrolnego zawierają szukane słowa, więc drugi bieg tego samego dnia
    widziałby własną linię i uznał awarię za komplet — stąd odsiew i test
    `test_powtorna_kontrola`. **Linia wyniku skryptu musi zaczynać się od `Kontrola:`**;
  - polskie litery w treści zgłoszenia: EC2 ma `urllib3==1.26.20`, który oddaje tekst do
    `http.client`, a ten koduje latin-1 → `UnicodeEncodeError`. Laptop (`urllib3==2.7.0`)
    koduje UTF-8, więc test na laptopie tego nie pokaże. Treść wysyłać jako
    `.encode("utf-8")`. **Sprawdzone na EC2 19.09** (2351 bajtów co do bajta, litery bez
    krzaków w treści wpisu i w mailu) — ryzyko zamknięte.
- **19.09, commit `b28e3de`** (wpis `notatki/dziennik/2026-09-19.md` napisany 21.09
  z transkryptu sesji): część główna `control.py` — czyta `errors.txt` (albo plik z
  `KONTROLA_LOG`), datę bierze z `KONTROLA_DATA` albo z dzisiejszej daty maszyny, adres
  stróża z `STROZ_URL`; wypisuje `Kontrola: OK` albo `Kontrola: AWARIA - …`; przy komplecie
  `get`, przy awarii `post …/fail` z treścią w UTF-8; odpowiedź inna niż 200 albo wyjątek →
  linia `Kontrola: …` i kod wyjścia 1; bez `STROZ_URL` druga linia `Kontrola: brak adresu
  stróża`. `data_ingestion.py`: `basicConfig` bez `filename`, więc błędy `ERROR` idą na
  stderr, czyli do `errors.txt`; `flush=True` przy linii startu, bo bez niego `ERROR`
  lądował **przed** linią startu, poza blokiem (zwykły `print` do pliku czeka w buforze,
  `stderr` nie) — pokazane na żywo na laptopie. Sprawdzone 19.09: lokalnie `11 passed`
  i obie gałęzie wysyłki z fałszywym adresem; na EC2 (pull do `b28e3de`) testy 2 i 3
  z notatki: data 18.09 → `Kontrola: OK`, data 19.09 → `Kontrola: AWARIA - …`, oba
  kod 0; stróż: `#1 Failure` (POST, 2351 bajtów = 57 + 2294, policzone przed odczytem)
  i `#2 OK` (GET); trzy maile na Interii (test z przycisku, DOWN, UP).
- **21.09 — wgranie i pierwszy bieg z `cron`:** `crontab` wgrany o **14:53:03 UTC (16:53
  polskiego)** z pliku `~/crontab-nowy-0919.txt` (kontrole przed: żywy `crontab` = kopia,
  5 / 7 linii, `diff` z zamaskowanym adresem cztery linie, `wc -c` linii z adresem 67,
  `date` 14:52:55 UTC, przed oknem 17:55). Bieg o 18:00 i skrypt kontrolny o 18:30:02:
  start w linii **663** (`16:00:02` UTC), blok 28 linii, `Kontrola: OK` w linii **691**,
  stróż `#3 OK` (18:30, `GET` z `13.63.105.190`, `down → up`), mail `UP`. Wszystkie
  przewidywania zapisane przed odczytem.
- **Blok w `errors.txt`:** 29 linii w dzień giełdowy, 27 bez nowych wiadomości —
  **potwierdzone 21.09** dla dnia giełdowego.
- **Czego sygnał świadomie nie łapie:** złych danych przy udanym biegu (Athena zwraca pół
  tabeli, Yahoo poprawia ceny wstecz, cena z trwającej sesji); braku świecy o 18:00 w dzień
  giełdowy (wygląda jak sobota, sam się naprawia dzień później); lokalnych rzeczy
  (kompakcja z laptopa). Gdy EC2 leży albo `cron` nie ruszył, alarm idzie po 19:00 od
  stróża, nie od skryptu.
- **Zostaje:** 25.10 pierwszy prawdziwy sprawdzian strefy u stróża; obserwacja przez
  kolejne dni (jeden bieg to za mało na „działa"); godzina przyjścia maili (hipoteza
  o opóźnieniu z Interii).

### Wciąż otwarte (najkrócej, pełne opisy w przeglądzie)

- Producent uruchomiony przed 17:00 zapisuje cenę z trwającej sesji jako
  zamknięcie.
- Okno na kurs zamknięcia u Yahoo ma najwyżej kwadrans zapasu (11.09:
  o 17:45 brak świecy, o 18:00 jest).
- Testy sprawdzają rzeczy obok potoku.
- Nikt nie dowie się o awarii — **zamknięte 21.09 w zakresie sygnału** (patrz „Sygnał awarii"). Log
  podwójny naprawiony w kodzie 19.09: Producent pisze błędy na stderr do
  `errors.txt`, `errors.log` przestał rosnąć (laptop: 6519 bajtów przed
  i po; EC2: 8 linii, potwierdzone 21.09).
- Korekty cen Yahoo nie docierają do S3.
- **Nowe 21.09:** wykresy (`wykresy.py`, `ranking.py`), `test_plikow.py` i Power BI
  czytają lokalne `gold/` i `silver/`, które stoją od 20.09 (Harmonogram wyłączony) —
  pokażą stare dane bez błędu. Do przepięcia na Athenę; osobna decyzja i notatka.
- Nierówne okna `range=3y` dla nowej spółki (13.09).
- README obiecuje więcej, niż jest.
- **Trzy sprawy z 14.09 — wszystkie zamknięte 17.09:**
  - `consumer.close()` — ✅ dopisane, sprawdzone (`no active members` od
    razu po biegu). **Zostaje ograniczenie:** `close()` stoi za
    `put_object`, więc przy awarii się nie wykonuje. Pełne rozwiązanie
    wymaga `finally` — odłożone świadomie, nie gubi danych;
  - zakładka przed zapisem — ✅ z podejrzenia zrobił się fakt potwierdzony
    w kodzie i na żywo, potem naprawiony (patrz punkt 3 kolejki);
  - CBF — ✅ porównane z BiznesRadarem: 14.09 `201.00`, 15.09 `197.40`,
    16.09 `195.30`, **co do grosza zgodnie z Yahoo**. **17.09 `204.00`
    potwierdzone 18.09 w oficjalnym archiwum GPW** (gpw.pl, Archiwum
    notowań), razem z SNT 344,80 i XTB 147,24. BiznesRadar miał w archiwum
    203,80 — to jego błąd (jego własny nagłówek wskazywał 204,00). **Od
    18.09 porównujemy z archiwum GPW, nie z BiznesRadarem.**
- **Nowe 17.09:**
  - **rozjazd nazw kolumn**, zamierzony: plik CSV w S3 ma w nagłówku
    `pierwsza_cena` i `ostatnia_cena`, a tabela `gold_ranking_spolek`
    `pierwotna_cena` i `aktualna_cena`. Nic nie psuje (nagłówek pomijany,
    dopasowanie po kolejności), ale trzeba o tym wiedzieć. Zrównanie nazw
    wymagałoby zmiany w `gold.py`, czyli wdrożenia na EC2;
  - Cyber_Folks połączył się z Shoperem, 15.09 weszło ponad 3,2 mln akcji
    serii F. Przy takich zdarzeniach kursy historyczne bywają przeliczane
    wstecz — to zaostrza znaną wadę „korekty cen nie docierają do S3".
- **Poza kolejnością, do decyzji Gracjana:**
  - Python 3.10 na EC2, jedyna sprawa, która pogarsza się sama, bo `boto3`
    porzucił 3.9 w kwietniu 2026;
  - `pd.read_sql` przez SQLAlchemy;
  - ostrzeżenie `value_deserializer`;
  - słowa „niedobór pamięci" w komentarzu `compaction.py` (prawdziwy powód
    to brak biblioteki);
  - plan B dla źródła danych;
  - **(15.09) kompakcja, wykresy (`wykresy.py`, `ranking.py`) i Power BI nie
    mają miejsca w kolejności napraw.** Propozycja Claude'a: kompakcja na EC2
    po sygnale awarii i Pythonie 3.10 (w `cron` byłaby comiesięcznym
    kasowaniem, którego nikt nie ogląda); wykresy i Power BI przepiąć na
    Athenę zaraz po wyłączeniu Harmonogramu, bo inaczej pokażą stare dane
    bez błędu **(od 21.09 to się już dzieje: Harmonogram wyłączony)**. Silvera do S3
    nie potrzeba: `gold/dane_dzienne.csv` ma
    wszystkie jego kolumny. Niezdecydowane.

### Test „zakładki nie ma" — wynik z 14.09, potwierdzony na EC2 15.09

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
- **15.09 na EC2:** 2 × `(2316, 3)`, `Odebrano 3`, zakładka 2345. Brakuje
  tylko sygnału awarii.
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
- **15.09:** blok po nowym Goldzie „+1 linia”. Będzie +4: Gold jako osobny
  program wypisze też 2 linie ostrzeżenia `boto3`.
- **15.09:** `echo %GOLD_DO_S3%` (składnia cmd) podane do PowerShella, gdzie
  zawsze wypisuje sam napis i nic nie sprawdza.
- **15.09:** `git status` „5 linii” po teście wysyłki. Było 6, bo Claude
  chwilę wcześniej sam zmienił notatkę z 14.09.
- **17.09:** liczenie godziny z głowy zamiast sprawdzenia zegara. Claude
  napisał „jest 17:56", gdy było 17:37 — i wcześniej też szacował czas na
  podstawie postępu rozmowy. Gracjan sprostował. **Wniosek: przed każdą
  wypowiedzią o godzinie uruchomić `date`.**
- **17.09:** przewidziane „`3 insertions`" przy `git commit`, a wyszło 321.
  Liczba 3 dotyczyła samego `kafka_consumer.py`; `git commit` sumuje
  wszystkie pliki w commicie, a w tym był też plik notatki (318 linii),
  którego długość Claude znał. **Wniosek: przy `git commit` podawać sumę,
  przy `git diff plik` — liczbę dla pliku.**
- **17.09:** w notatce zapisane, że jeden bieg testowy dowiedzie zarówno
  nieruszonej zakładki, jak i działania `close()`. Niewykonalne — przy
  awarii zapisu program pada przed `close()`. Poprawione w notatce po
  napisaniu kodu, rozdzielone na dwa testy.
- **17.09:** „aktualna cena 191,2 zł" z wyszukiwarki podana jako możliwy
  punkt odniesienia dla dzisiejszego biegu. Arytmetyka się nie domykała
  (spadek 3,34% od 195,30 dałby 188,8), więc wartość była niewiarygodna od
  początku i nie powinna trafić do rozmowy jako poszlaka.
- **18.09:** „AWS nie łapie czwartku i piątku" — za szeroko. Nie łapie
  **sama SNS**; AWS ma CloudWatch, który umie alarmować przy ciszy.
  Sprostowane na pytanie Gracjana, wariant dopisany do notatki.
- **18.09:** dwa podobne słowa na dwie różne rzeczy („strażnik" i „stróż")
  w jednej notatce. Zmienione na „skrypt kontrolny" i „stróż".
- **18.09:** kroki do sprawdzenia biegu podane jako „są w wiadomości sprzed
  trzech", a kroki do kodu jako długa lista z tabelą w środku jednego kroku.
  Gracjan dwa razy prosił o przepisanie. Stąd dopisek w zasadzie 3.
- **18.09:** niejasna uwaga o komunikacie przy braku `Odebrano` („wypisze
  całą listę spółek") — Gracjan zrozumiał ją jako prośbę o komunikat na
  każdą spółkę i dopisał pętlę. Chodziło o komunikat o Konsumencie.
- **18.09:** jako wzór testów wskazany `test_bieg_nie_z_dzis` — jedyny test
  z inną datą. Gracjan przepisał datę `2026-09-19` do sześciu testów.
- **18.09:** od 13.09 w CLAUDE.md i przeglądzie stało „26.10 pierwszy bieg
  po zmianie czasu". Czas zmienia się w nocy z 24 na 25.10, więc pierwszy
  bieg z `17:00` UTC to niedziela 25.10 (sprawdzone strefą czasową Windows).
  Poprawione w obu miejscach.
- **20.09:** przewidywanie rozmiaru pliku Golda w S3 (157886 − 2326 = 155560)
  policzone przed komendą, ale wpisane do wiadomości dopiero po niej.
  Sprawdzenie było dobre, zapis „przed" nie. **Wniosek: liczbę napisać
  w wiadomości, dopiero potem puszczać komendę.**
- **21.09:** na starcie sesji podałem stan sprzed 19.09 jako aktualny (EC2 na
  `033107f`, zadanie u stróża niepotwierdzone, ceny z 18.09 otwarte, testy
  niewyjaśnione, „nie wiemy, czy część główna była uruchamiana"), bo dziennika
  z 19.09 nie było, a CLAUDE.md kończył się na 20.09. Transkrypt sesji z 19.09
  pokazał, że kod jest na EC2, ustawienia stróża potwierdzone, ceny sprawdzone,
  testy wyjaśnione, a część główna przetestowana. **Wniosek: dziennik
  i CLAUDE.md pisać w dniu sesji, także gdy sesja urwie się w połowie; brak
  wpisu z dnia to sygnał, że stan trzeba sprawdzić w transkrypcie
  (`list_events` na sesji), a nie zakładać, że nic się nie zdarzyło.**
- **19.09 (z transkryptu):** Claude kazał sprawdzać Gmaila, a maile idą na
  Interię — adres wziął z danych sesji, nie z ustawień stróża. Pierwsze
  przewidywanie testu z fałszywym adresem: jedna linia zamiast dwóch (zmienne
  `$env:` zostają w oknie PowerShella). Sprostowane w sesji.
- **21.09 (wieczór):** `git add` — przewidziano „brak wyniku", a wypisał ostrzeżenie
  o końcach linii (`LF` na `CRLF`); wcześniej o nim wspominano tylko przy commicie.
  Niegroźne.
- **21.09:** kolejność linii w wynikach przewidziana błędnie: `git rm --cached` wypisuje
  alfabetycznie, `git status --short` daje nieśledzone `??` na końcu. Treść zgodna.
  **Wniosek: przewidywać liczby i słowa, nie układ.**
- **21.09:** zakres godziny dla `date` na EC2 (15:00–15:15 UTC), a wyszło 14:52:55, bo
  Gracjan szedł szybciej niż zakładano; odczyt `RELOAD` ustawiony bez odczekania,
  więc pierwszy odczyt nie mógł go jeszcze zawierać (wpis potrzebuje kilku–
  kilkunastu sekund).
- **21.09:** wpis z 19.09 napisany najpierw w pierwszej osobie. Dziennik ma narrację
  bezosobową, pierwsza osoba tylko w „Czego się nauczyłem". Przepisany.

### Priorytet Gracjana (08.09)

Czysty, działający łańcuch `data_ingestion → Kafka → S3/Athena → silver →
gold` → wynik na stronie. Wykresy, README pod pracodawcę, Power BI —
dopiero potem.

### Na następną sesję

**Sprawdzian punktu 6 (wtorek 22.09, bieg o 18:10)** i dalej według listy. 21.09 zrobiono:
sygnał awarii w `cron` (pierwszy bieg 18:30), wyłączenie Harmonogramu, `silver/` i `gold/`
poza gitem (laptop i EC2), dokumentację i notatkę o nawiasach (Gracjan czyta ją przed
sesją: `notatki/plany/Notatka-2026-09-21-nawiasy-w-pythonie.md`).

1. **Sprawdzian 22.09 — przewidywania zapisane 21.09** (założenie: wtorek 22.09 to dzień
   giełdowy i Yahoo ma świecę o 18:00; pełne kroki podać przed biegiem):
   - linia startu **692** (`16:00:0X` UTC), po 18:32 `wc -l` **720**, ostatnia linia
     `Kontrola: OK`;
   - blok jak 21.09, ale 2 × `(2331, 3)`, `Odebrano 3`, 2 × `S3: wysłano`, bez `Traceback`
     (folder istnieje);
   - zakładka **2360**, pliki spółek **777** (razem 2331), Athena 777 na spółkę, `do` =
     `2026-09-22 17:00:00`;
   - S3 `gold/`: `dane_dzienne.csv` ok. **155990–156010 B** (155778 + 3 × ok. 73),
     `ranking.csv` ok. 355–365 B;
   - EC2 po biegu: `ls -a silver gold` — w `silver` `.gitkeep` i `clean_data.csv`, w `gold`
     `.gitkeep`, `dane_dzienne.csv`, `ranking.csv`; `git status --short` **pusty** (pliki
     ignorowane);
   - stróż `Up`, ostatnie zgłoszenie ok. 18:30, łącznie 4; lokalny `silver\clean_data.csv`
     dalej `20.09.2026 20:22:04`.
2. **Po sprawdzianie:** zmienić zasadę 14 w tym pliku (rytuał `git checkout -- silver/ gold/`
   przestaje być potrzebny, bo pliki są ignorowane, a `git status --short` na EC2 ma być
   pusty) i dać ✅ przy punkcie 6.
3. **Test prawdziwej drogi** (następny w kolejce) albo **przepięcie wykresów, `ranking.py`,
   `test_plikow.py` i Power BI na Athenę** — do wyboru Gracjana; oba czekają na sprawdzian
   punktu 6.
4. **Notatka o nawiasach** — pytania Gracjana i ćwiczenia z odpowiedziami na początku sesji.
5. **Terminy:** 1.10 kompakcja z laptopa (wypisze o 3 pliki więcej z powodu testu B);
   **25.10** (niedziela) pierwszy bieg po zmianie czasu — `17:00:0X` w linii startu i to
   będzie poprawne, a u stróża pierwszy prawdziwy sprawdzian strefy.

**EC2 jest na `6af7b48` od 21.09 ok. 19:03** (dziewięć plików, zgodnie z przewidywaniem;
`git status --short` pusty). Od tego czasu w `kod/` nic się nie zmieniło.

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
    **wgrany 21.09 o 14:53:03 UTC (16:53 polskiego)** i od tego dnia jest żywym
    `crontab` (siedem linii). Powrót sprzed sygnału awarii: `crontab
    ~/crontab-kopia-0919.txt`.

## Gdzie co jest

Kod, dane i notatki razem w folderze projektu: `kod/`, `companies/`
(pamięć Producenta, **poza gitem**, każda maszyna ma własną), `bronze/`
(poza gitem), `silver/`, `gold/` (**od 21.09 poza gitem**, w folderach tylko `.gitkeep`;
dawniej w gicie, do czasu, gdy wynik trafi
do S3), `wykresy/`, `notatki/`, `aws/` (klucz SSH, poza gitem). Skrypt
kontrolny (od 18.09): `kod/control.py`, testy `kod/test_control.py`, wzór
prawdziwego bloku logu `kod/dane_testowe/blok_2026-09-18.txt`. Testy
uruchamiane z folderu projektu: `pytest kod/test_control.py -v`. Nauka
Pythona (osobny projekt): `DE/Python_l/`.

**Co z `notatki/` jest w gicie, sprawdzone 11.09.** `notatki/plany/`
i `notatki/Slownik.md` **są śledzone**. Poza gitem, przez `.gitignore`, są
`notatki/dziennik/` i `notatki/.obsidian/`. Znaczy to, że **wszystkie wpisy
dziennika (32 pliki na 15.09), czyli cały zapis nauki z tego projektu,
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
