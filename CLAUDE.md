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
`merge`, `drop_duplicates`, `to_parquet`, od 03.10 `read_sql` z `pyathena` i `sort_values`
z `ascending=False` w wykresach), `matplotlib` podstawy, Power BI
podstawy, `pytest` podstawy, strefy czasowe (`ZoneInfo`, `.astimezone`, `time(17, 55)`,
od 05.10) i flaga z `continue` w pętli (06.10), `kafka-python` (Producent/Konsument, `group_id`,
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
    ustalonej z Gracjanem.

16. **Przegląd całości** (cały kod + wszystkie notatki od początku) po
    zamknięciu każdego większego kawałka i zawsze na prośbę Gracjana —
    wynik do pliku przeglądu, nie do pamięci.

## Stan projektu — uczciwie (06.10 wieczorem)

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
**Od 26.09 (EC2 na `fc6e262`) skrypt kontrolny o 18:30 sprawdza log i dane:** poza blokiem
w `errors.txt` pyta Athenę (`SELECT spolka, data FROM gold_dane_dzienne` przez
`pobierz_dane()` z `kod/path.py`) i dokłada problemy z `sprawdz_daty` (brak dzisiejszej
świecy w dzień pon–pt, wpis z przyszłości, różna liczba dni między spółkami, spółka bez
wierszy) do tej samej listy. Jedno zgłoszenie do stróża. `crontab` bez zmian. Pierwszy bieg
z `cron` na nowym kodzie: 26.09 o 18:30, **sprawdzony tego samego wieczoru**: blok 30 linii,
`Kontrola: Dane 2340 wierszy`, `Kontrola: OK`.
**Od 03.10 (`RELOAD` 09:45:01 UTC) wszystkie trzy biegi idą na Pythonie 3.14.6** z
`~/GPW---pulse/venv314/bin/python` (pandas 3.0.5, `urllib3` 2.7.0). Tylko ścieżka w trzech
liniach `crontab` się zmieniła; nadal siedem linii. Stary `venv` (3.9.25) stoi nietknięty jako
powrót: `crontab ~/crontab-kopia-1003.txt`. Pierwszy bieg (sobota 03.10) zgodny co do linii,
pierwszy dzień giełdowy (pon. 05.10) też, a zgłoszenie awarii do stróża na 3.14 sprawdzone
06.10 (#21, 1836 B). Od #17 stróż widzi `python-requests/2.34.2` (wcześniej `2.32.5`).

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
  ręcznie przez `compaction.py`, **wyłącznie z laptopa**. **Pierwszy bieg z prawdziwym
  kasowaniem: 03.10** — `Usunięto 66 plików`, `bronze` do `2026-09-30 17:00:00`
  (783 wiersze na spółkę), w `live/` zostały pliki z października. Następny: na początku
  listopada, nie między 17:55 a 18:35.
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
  sam `.gitkeep`; pliki `.csv` **wróciły z pierwszym biegiem o 18:10 — sprawdzian
  22.09 potwierdzony w całości**, `git status --short` po biegu dalej pusty.
  Lokalne pliki na laptopie stoją od 20.09 20:22:04 (Harmonogram wyłączony, to
  zamierzone). Notatka:
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
- **Od 26.09** (nowy `control.py` na EC2) skrypt kontrolny dokłada 3 linie: 2 linie
  ostrzeżenia `pandas` (stderr, więc **nad** liniami `Kontrola:`) i `Kontrola: Dane N
  wierszy` (przedostatnia). Blok: **32 linie** w dzień giełdowy, **30** w weekend/święto.
  Przy awarii Atheny zamiast 4 linii kontroli będzie ok. 30: 2 ostrzeżenia, 25 linii od
  `pyathena` (`Failed to execute query.` + `Traceback`, policzone 26.09) i 3 linie wyniku
  (pandas 2.3.3 opakowuje błąd, dwie z tych linii nie zaczynają się od `Kontrola:`).
  **Potwierdzone 26.09 (sobota): blok w liniach 808–837, 30 linii.** Blok dnia giełdowego
  (32) pierwszy raz 28.09.
- **Od 03.10 (Python 3.14) blok ma 28 linii w obu rodzajach dni.** Znikają ostrzeżenia
  `boto3` o Pythonie 3.9: 2 linie w Goldzie (zawsze, bo `GOLD_DO_S3=1` tworzy klienta S3)
  i 2 w Konsumencie (tylko w dzień giełdowy, gdy ma co zapisać). Weekend 30 − 2 = 28, dzień
  giełdowy 32 − 4 = 28. Ostrzeżenie powstaje przy **tworzeniu klienta S3**, nie przy imporcie,
  dlatego ręczny Gold bez `GOLD_DO_S3` nie pokazywał go nawet na 3.9. **Potwierdzone 03.10
  (sobota): 1028–1055.** Dzień giełdowy na 3.14 potwierdzony 05.10 (1084–1111) i 06.10 (1112–1139). Przy awarii Atheny na
  pandas 3.0.5 wynik kontroli powinien zająć 1 linię zamiast 3 (tak było na laptopie 25.09),
  a `Traceback` od `pyathena` na 3.14 jest dłuższy niż 25 linii — **na EC2 niesprawdzone**.

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

**Stan 22.09 wieczorem** (dzień giełdowy, sprawdzian punktu 6 — folderów
`silver/`/`gold/` odtworzonych z samego `.gitkeep`): `errors.txt` **720**
linii; start biegu w linii **692** (`16:00:02` UTC, odczyt na EC2 ok. 19:04
polskiego); blok 29 linii (692–720), `Kontrola: OK` w linii 720; Silver
i Gold po `(2331, 3)`; zakładka `2360 2360 0`, `no active members`; pliki
spółek po 777 (razem 2331); `COUNT(*)` na `gold_dane_dzienne`: 777 dni na
spółkę na wszystkich trzech, `do` = `2026-09-22 17:00:00`; S3 `gold/`
z 16:10:07 UTC: `dane_dzienne.csv` 155997 B, `ranking.csv` 364 B.
`errors.log` 8, bez zmian. Zero linii `Traceback`, `Error`, `ERROR`,
`nietknięte`. `ls -a silver gold` na EC2: w `silver` `.gitkeep`
i `clean_data.csv`, w `gold` `.gitkeep`, `dane_dzienne.csv`,
`ranking.csv`; `git status --short` **pusty**. Stróż: `#4 OK`, 22.09 18:30,
`Up`, łącznie cztery zgłoszenia. Wszystkie piętnaście przewidywań zapisanych
21.09 trafione co do liczby — patrz „Kolejność napraw", punkt 6.

**Stan 23.09 wieczorem** (dzień giełdowy). **Codziennej kontroli na EC2 nie było**
(log, zakładka, stróż, S3 nieodczytane). Jedyny odczyt to test prawdziwej drogi z laptopa
ok. 19:20 polskiego: `gold_dane_dzienne` ma **2334** wiersze, po 778 dni na spółkę,
każda z wpisem z 23.09, bez dni z przyszłości (`Dane: OK`). Pośrednio znaczy to, że bieg
o 18:00/18:10 dopisał świece. Przewidywania na kontrolę z 23.09, gdyby ją robić z logu:
start w linii 721, `wc -l` 749, 2 × `(2334, 3)`, zakładka 2363, pliki spółek po 778.
**Potwierdzone 25.09:** linia startu 23.09 to 721.

**Stan 25.09 wieczorem** (piątek, dzień giełdowy; 24.09 bez kontroli, sprawdzony razem
z 25.09). Odczyt na EC2 o 17:54:35 UTC. Linie startu **721, 750, 779**, wszystkie
`16:00:02` UTC. `wc -l` **807**. Bloki 24.09 i 25.09 po 29 linii: `(2337, 3)` i `(2340, 3)`,
2 × `S3: wysłano`, `Kontrola: OK`. Zero linii `Traceback|Error|ERROR|nietknięte`. Pliki
spółek po **780** (razem 2340). `errors.log` 8. Zakładka `2369 2369 0`, `no active members`.
S3 `gold/` z 16:10:07 UTC: `dane_dzienne.csv` **156615 B** (w przewidzianym zakresie
156550–156750), `ranking.csv` **338 B** (przewidziane „ok. 360”, szacunek bez wyliczenia).
`silver`/`gold` z `.gitkeep` i `.csv`, `git status --short` pusty, EC2 na `6af7b48`. Athena:
780 dni na spółkę, `od` 2023-08-14, `do` 2026-09-25 17:00:00, przeczytane 152,94 kB. Stróż:
#5–#7 `OK` o 18:30 (23–25.09), bez zmiany stanu od 21.09 `down → up`. Ranking 25.09:
CBF 204,60, SNT 353,00, XTB 151,50 (niesprawdzone w archiwum GPW). ~~Przewidywania na
następny dzień giełdowy (pon. 28.09): start w linii 808, `wc -l` 836~~ — **błąd, sprostowany
26.09:** 808 to start sobotniego bloku, bo liczba pomijała weekend. Nieaktualne też dlatego,
że kod z etapu B trafił na EC2 26.09. Aktualne przewidywania: tabela w „Stan 26.09” niżej.

**Stan 26.09** (sobota; po południu wdrożenie, wieczorem kontrola pierwszego biegu z `cron`).
**Etap B punktu 7 (test prawdziwej drogi na EC2) zamknięty.** `date` na EC2 13:55:17 UTC,
`git status --short` pusty, `git pull` `6af7b48..fc6e262` (`13 files changed, 3258
insertions(+), 178 deletions(-)`, zgodnie z przewidywaniem), po nim `git status --short` pusty.
Ręczne biegi `control.py` w oknie SSH, bez `>>` (log **807** linii przed i po):
- **E1** `KONTROLA_DATA=2026-09-25` → 2 linie ostrzeżenia `pandas`, `Kontrola: Dane 2340
  wierszy`, `Kontrola: OK`, `Kontrola: brak adresu stróża`. Import `path.py` działa na
  Pythonie 3.9, rola EC2 czyta `gold_dane_dzienne`.
- **E2** `KONTROLA_DATA=2026-09-28` → `AWARIA` z 4 problemami (brak pomiaru z 28.09 + 3 × `brak
  wpisu z: 2026-09-28`), co do słowa.
- **E3** zmyślone `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY` → `Failed to execute query.`
  i `Traceback` od `pyathena` (razem 25 linii), potem wynik w **3 liniach**: `Kontrola: AWARIA -
  Athena: Błąd - Execution failed on sql: SELECT …`, `An error occurred
  (UnrecognizedClientException) …`, `unable to rollback`. Pandas 2.3.3 na EC2 opakowuje błąd
  (laptop, pandas 3.0.5: jedna linia). Przewidziane przed biegiem, sprawdzone w kodzie pandas.
- **E4** adres stróża z `crontab -l` przez `$( )` (`${#STROZ_URL}` = 56): E2 → u stróża **#8
  `Failure`**, `POST`, 16:04, **2450 B** (= 154 linia `AWARIA` + 2 + 2294 blok z 25.09),
  `up → down`; E1 → **#9 `OK`**, `GET`, 16:04, `down → up`. `unset`, potem `${#STROZ_URL}` = 0.
  **Maile `DOWN` i `UP` przyszły na Interię o 16:19**, 15 minut po zmianie stanu u stróża
  (hipoteza z 19.09 potwierdzona).

**Przewidywania do 02.10** (zapisane 26.09 ok. 16:15, przed biegami; blok **30** linii
w weekend, **32** w dzień giełdowy; brak świąt w tym okresie, z pamięci):

| Dzień | Start | `wc -l` po biegu | `Kontrola: Dane` | Zakładka | Pliki spółek | Stróż (tylko biegi `cron`) |
|---|---|---|---|---|---|---|
| sob. 26.09 | 808 | 837 | 2340 | 2369 | 780 | #10 |
| niedz. 27.09 | 838 | 867 | 2340 | 2369 | 780 | #11 |
| pon. 28.09 | 868 | 899 | 2343 | 2372 | 781 | #12 |
| wt. 29.09 | 900 | 931 | 2346 | 2375 | 782 | #13 |
| śr. 30.09 | 932 | 963 | 2349 | 2378 | 783 | #14 |
| czw. 1.10 | 964 | 995 | 2352 | 2381 | 784 | #15 |
| pt. 2.10 | 996 | 1027 | 2355 | 2384 | 785 | #16 |

Do tego w sobotę 26.09 i niedzielę 27.09: 3 × `nowych dni: 0, wysłane: 0, stan: zapisane`,
`Odebrano 0`, 2 × `(2340, 3)`, 2 × `S3: wysłano`, S3 `gold/` **156615 B** i **338 B** (wejście
bez zmian). Każdy ręczny bieg `control.py` ze `STROZ_URL` przesuwa numery u stróża.

**Wieczorna kontrola 26.09** (`date` na EC2 17:00:43 UTC): wiersz sobotni tabeli trafiony
w całości. Linie startu 779 i **808** (`16:00:02` UTC), `wc -l` **837**, blok 30 linii:
3 × `nowych dni: 0, wysłane: 0, stan: zapisane`, `Odebrano 0 wiadomości`, 2 × `(2340, 3)`,
2 × `S3: wysłano`, na końcu 2 linie ostrzeżenia z `kod/path.py:32`, **`Kontrola: Dane 2340
wierszy`**, **`Kontrola: OK`** — ostrzeżenie nad liniami `Kontrola:`, jak wynikało z bufora.
Zero `Traceback|Error|ERROR|nietknięte`. Pliki spółek 780 × 3 (2340), `errors.log` 8, zakładka
`2369 2369 0`, `no active members`. S3 `gold/` 16:10:06 UTC: **156615 B** i **338 B**.
`silver`/`gold` z `.gitkeep` i `.csv`, `git status --short` pusty. Stróż: według Gracjana
„wszystko OK” (zrzutu nie było, więc numer #10 nieodczytany przez Claude'a).

**Stan 03.10** (sobota, sesja 10:35–12:32; kontrola wieczornego biegu dopiero 04.10). Dziennik
`notatki/dziennik/2026-10-03.md`.
- **Biegi 27.09–02.10 sprawdzone wstecz:** cała tabela „Przewidywania do 02.10” wyżej trafiona
  (starty 808…996, `wc -l` 1027, blok 28.09 868–899 = 32 linie z `Dane 2343` i `OK`, pliki
  785 × 3, zakładka `2384 2384 0`, S3 157673 B / 350 B z 02.10 16:10:07 UTC, stróż #10–#16
  `OK` bez zmiany stanu, na Interii żadnego `DOWN`). Zastrzeżenie „tylko sobota” z punktu 7
  zdjęte: „brak dzisiejszej świecy” przeszedł pięć dni giełdowych.
- **Kompakcja zrobiona** (laptop, `python kod/compaction.py`): przewidziane z samego `Total
  Objects: 72` „usunięte 66” → `stara ilosc: 761, nowa_ilosc: 783` × 3, `Usunięto 66 plików`.
  `bronze` do `2026-09-30 17:00:00` (783 wiersze na spółkę), w `live/` 6 plików z 01–02.10,
  Athena `bronze UNION ALL live` 785 dni × 3 przed i po.
- **Python 3.14 na EC2** (notatka `notatki/plany/Notatka-2026-10-03-python-na-ec2.md`,
  zatwierdzona; decyzja 5 wbrew rekomendacji: przepięcie w sobotę). Laptop: nowy
  `requirements-ec2.txt` (18 paczek przez `-c requirements-lokalny.txt`), `venv314/` w
  `.gitignore`, commit `4aca12d`. EC2: `pull` do `4aca12d`, `dnf install python3.14` (3.14.6;
  systemowy `python3` dalej 3.9.25), `venv314` z gotowych paczek, `diff` z `pip freeze` pusty.
  Silver+Gold w obu `venv` → **3 × `diff -q` puste, pliki identyczne co do bajtu**. Ręczne biegi
  na `venv314`: `control.py` `Dane 2355`/`OK`, Producent 3 × `zapisane`, Konsument `Odebrano 0`.
  `crontab`: kopia `~/crontab-kopia-1003.txt`, nowy `~/crontab-nowy-1003.txt` (`sed
  's#/venv/bin/python#/venv314/bin/python#g'`), `diff` `5,7c5,7`, `RELOAD` **09:45:01 UTC**.
- **Wykresy na Athenie** (notatka `Notatka-2026-10-03-wykresy-na-athene.md`, pięć decyzji (a);
  instrukcja `Notatka-2026-10-03-jak-przepiac-wykresy.md`): `wykresy.py` i `ranking.py` czytają
  `gold_dane_dzienne` / `gold_ranking_spolek`, sortują, w tytule `(stan na: RRRR-MM-DD)`;
  `test_plikow.py` usunięty; `pytest kod/ -v` → `18 passed`; awaria ze zmyślonymi kluczami głośna,
  obrazek nienadpisany. Commit `96f191b`. Power BI odłożony.
- **Pierwszy bieg `cron` na 3.14 (sob. 03.10), odczyt 04.10 o 13:20 UTC — zgodny w całości:**
  starty 996 i **1028** (`16:00:03` UTC), `wc -l` **1055**, blok **28 linii** bez ani jednej
  `PythonDeprecationWarning` (dowód, że szedł `venv314`), 3 × `nowych dni: 0 … zapisane`,
  `Odebrano 0`, 2 × `(2355, 3)`, Gold `117`/`111`, 2 × `S3: wysłano`, `Kontrola: Dane 2355
  wierszy`, `Kontrola: OK`, zero błędów, pliki 785 × 3, `errors.log` 8, zakładka `2384 2384 0`,
  S3 157673 B / 350 B z 16:10:07 UTC, `git status --short` pusty, stróż `Up` (numeru #17 nie
  odczytaliśmy), Interia bez maili.
- **Na 3.14 sprawdzone później:** wysyłka przez Kafkę i zapis Konsumenta do S3 (05.10) oraz
  zgłoszenie `/fail` do stróża z `urllib3` 2.7.0 (06.10) — „Stan 05–06.10” niżej.

**Przewidywania od 04.10** (zapisane 04.10 ok. 15:30; blok **28 linii w obu rodzajach dni**;
w październiku brak świąt; Gold `117`/`111` do końca października):

| Dzień | Start | `wc -l` po biegu | `Odebrano` | `Kontrola: Dane` | Zakładka | Pliki spółek | Stróż |
|---|---|---|---|---|---|---|---|
| niedz. 04.10 | 1056 | 1083 | 0 | 2355 | 2384 | 785 | #18 |
| pon. 05.10 | 1084 | 1111 | 3 | 2358 | 2387 | 786 | #19 |
| wt. 06.10 | 1112 | 1139 | 3 | 2361 | 2390 | 787 | #20 |
| śr. 07.10 | 1140 | 1167 | 3 | 2364 | 2393 | 788 | #23 |
| czw. 08.10 | 1168 | 1195 | 3 | 2367 | 2396 | 789 | #24 |
| pt. 09.10 | 1196 | 1223 | 3 | 2370 | 2399 | 790 | #25 |
| sob. 10.10 | 1224 | 1251 | 0 | 2370 | 2399 | 790 | #26 |
| niedz. 11.10 | 1252 | 1279 | 0 | 2370 | 2399 | 790 | #27 |

Wiersze 04–06.10 trafione w całości (stróż #18–#20). **Numery u stróża od 07.10 poprawione
06.10 o +2**, bo ręczny test dał #21 i #22; każdy ręczny `control.py` ze `STROZ_URL` je przesuwa.
S3 `dane_dzienne.csv`: 158096 B na 2361 wierszy (06.10), ok. +218 B na dzień giełdowy (2358 →
2361: 157891 → 158096 B); `ranking.csv` 330–370 B. Wdrożenie warunku 07.10 bloku nie zmienia:
o 18:00 nic się nie pomija, więc dopisku nie ma, blok dalej 28 linii.

**Stan 05–06.10** (dzienniki `2026-10-05.md` i `2026-10-06.md`):
- **05.10 (poniedziałek), pierwszy dzień giełdowy na Pythonie 3.14:** kontrola o 17:01 UTC, wiersze
  04 i 05.10 tabeli trafione w całości (1084–1111, `Odebrano 3`, `Dane 2358`, zakładka 2387, pliki
  786 × 3, S3 157891 B / 362 B), bez `PythonDeprecationWarning`. Kafka → S3 działa na nowym
  Pythonie; niedzielny bieg potwierdził, że odpięcie `IAMFullAccess` nie ruszyło EC2. Wieczorem
  porcja 1 warunku: `kod/session.py` (9 linii) i `kod/test_session.py` (10 testów), `10 passed`.
  Nazwy po angielsku (wybór Gracjana), instrukcja przepisana z `sesja` na `session`.
- **06.10 (wtorek):** porcja 2 — pięć zmian w `kod/data_ingestion.py` (84 → 92 linie, linie 6,
  27, 30, 59–61, 83–84), `pytest kod/ -v` → `28 passed in 2.16s`; bieg z
  `KAFKA_BOOTSTRAP=localhost:9999` o 16:45:35 → 4 × `ERROR` po 30 s, 3 × `nowych dni: 24, wysłane:
  0, stan: nietknięte, dziś pominięte (przed 17:55)`, pamięć nietknięta. **Pierwszy dowód na
  prawdziwych danych z Yahoo; na EC2 jeszcze stary kod** (warunek (d) 07.10). Kontrola biegu
  06.10 (17:07 UTC): 1112–1139, wszystko z tabeli, S3 158096 B / 349 B, stróż #20. Test `/fail`
  na 3.14 o 19:12 (ręczne `control.py` bez `>>`): `KONTROLA_DATA=2026-10-07` → `AWARIA` z 4
  problemami, u stróża **#21 `Failure`, `POST`, 1836 B** (przewidziane przed biegiem: 154 + 2 +
  1680; blok na EC2 `wc -c` 1681), `up → down`; `KONTROLA_DATA=2026-10-06` → **#22 `OK`**, `down →
  up`. **Nieodczytane w sesji:** maile `DOWN`/`UP` (ok. 19:27) i polskie litery w treści #21.
  Ranking 06.10: CBF 203,00, SNT 343,80, XTB 136,12.

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

### Codzienna kontrola po biegu (ułożona 20.09, przeliczona 21.09, 26.09 i 03.10)

Kiedy: po 18:32 polskiego, bo skrypt kontrolny kończy o 18:30, a Silver i Gold o
18:10. Godziny w logu są w UTC (patrz UWAGA wyżej). Przewidywania zapisać **przed**
puszczeniem komend. „Dzień giełdowy" to dzień z nowymi świecami, „weekend/święto" to
dzień bez. **Od 03.10 (Python 3.14) blok ma 28 linii w obu rodzajach dni**, więc zawsze
`tail -n 28`. Wcześniej: 32/30 (26.09–02.10), 29/27 (21–25.09). **Przy kontroli kilku dni
naraz** w krokach 5–7 brać wszystkie linie startu (`grep -n "=== Data pomiaru"
companies/errors.txt | tail -n N`, N = liczba dni) i porównać z tabelą „Przewidywania od
04.10” w „Stan 03.10”. Przy podawaniu kroków Gracjanowi kroki 1–2 są krokami
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
    z dzisiejszą datą i godziną `16:10` (UTC, bo z EC2). Rozmiar `dane_dzienne.csv`: 158096 B
    na 2361 wierszy (06.10), rośnie o ok. 73 B na wiersz (ok. +218 B na dzień giełdowy);
    `ranking.csv` 330–370 B. **Lokalnego pliku do porównania rozmiaru nie ma od 21.09**
    (Harmonogram wyłączony).
14. **[przeglądarka]** stróż: `Up`, ostatnie zgłoszenie ok. 18:30 (`Europe/Warsaw`), typ `GET`
    z `13.63.105.190`, `python-requests/2.34.2`, liczba zgłoszeń +1 na dzień (21.09: 3; 26.09
    po testach E4: 9; 06.10 `cron` #20, po teście `/fail` #22). Zrzuty przycinać bez pola z adresem zgłoszenia. Na Interii: żadnego
    `DOWN` (mail przychodzi ok. 15 minut po zmianie stanu).
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
6. **Wyłączenie lokalnego Harmonogramu, `silver/` i `gold/` poza gitem** — ✅ **21.09
   wdrożone, 22.09 sprawdzian zamknięty.** Notatka
   `notatki/plany/Notatka-2026-09-21-jedno-miejsce-liczenia.md` zatwierdzona: cztery
   decyzje zgodnie z rekomendacją (`.gitkeep`, wyłączenie a nie usunięcie zadania,
   `pipeline.bat` zostaje, historia gita nietknięta), piąta (termin): laptop od razu, EC2
   po potwierdzeniu 18:30 (tego samego wieczoru). Laptop: `.gitignore` z wyjątkiem
   `.gitkeep`, `git rm --cached`, commit `6af7b48` (`6 files changed, 4 insertions(+),
   4656 deletions(-)`, zgodnie z przewidywaniem), zadanie `GPW Pulse - pipeline` w stanie
   `Disabled`. Próba na klonie testowym zgodna (bez rytuału `pull` się przerywa, po
   rytuale kasuje pliki, foldery z `.gitkeep` zostają). EC2: rytuał i `pull` do `6af7b48`,
   sześć przewidywań zgodnych, w `silver/` i `gold/` sam `.gitkeep`. **22.09:** pierwszy
   bieg `cron` (18:00/18:10/18:30) na odtworzonych folderach — piętnaście przewidywań,
   piętnaście trafień (linia startu 692, `wc -l` 720, `(2331,3)`, zakładka 2360, Athena
   777/spółkę, S3 155997 B/364 B, stróż `Up`, `git status --short` pusty). Warunek (a)–(e)
   definicji „zrobione" spełniony. **Zostaje, świadomie poza tym punktem:** przepięcie
   wykresów, `ranking.py`, `test_plikow.py` i Power BI na Athenę (czytają lokalne pliki na
   laptopie, stojące od 20.09) — **03.10 zrobione poza Power BI**: wykresy na Athenie,
   `test_plikow.py` usunięty (`96f191b`); Power BI świadomie odłożony.
7. **Test prawdziwej drogi** — ✅ **26.09, z zastrzeżeniami.** 25.09 wpięty do `control.py`
   na laptopie (etap A, commit `8b8f585`); 26.09 na EC2 (etap B, `fc6e262`), biegi E1–E4
   zgodne, mail `DOWN` o 16:19; pierwszy bieg z `cron` o 18:30 (etap C) zgodny co do linii
   (szczegóły i zastrzeżenia na końcu punktu).
   `notatki/plany/Notatka-2026-09-22-test-prawdziwej-drogi.md`: sedno — dzisiejsze testy
   (`test_dzialania`, `test_powtorek`) sprawdzają rzeczy obok drogi danych, nic nie łączy
   się z Athena i nie sprawdza „dziś brakuje spółki" ani „jest dzień z przyszłości".
   Kształt wzorem `control.py` (czysta funkcja zwraca listę problemów, osobna warstwa
   łączy się z Athena). Cztery decyzje zatwierdzone: (1) tabela `gold_dane_dzienne`
   (koniec całej drogi, nie `live`); (2) dzień giełdowy wykrywany heurystyką
   poniedziałek–piątek, nie listą świąt GPW — oceniona pracochłonność 20–30 minut,
   świadomie przyjęty koszt: kilkanaście fałszywych alarmów rocznie w święta; (3) na start
   uruchamiane ręcznie z laptopa, wpięcie do `control.py`/EC2 to osobna, późniejsza
   decyzja; (4) sprawdza oba fakty z przeglądu **i** zgodność liczby dni między trzema
   spółkami, od razu.
   **23.09 kod napisany przez Gracjana i sprawdzony na laptopie.** `kod/path.py`:
   `sprawdz_daty(df, spolki, dzis)` (trzy sprawdzenia, kolumna `dzien` przez
   `.dt.date`) + `__main__` czytający `SELECT spolka, data FROM gold_dane_dzienne`
   z datą z `$env:DROGA_DATA` albo `date.today()`, wypisuje `len(df)` i `Dane: OK` /
   `Dane: Problem - …`. `kod/test_path.py`: 6 testów na zmyślonych danych
   z `ticker`, **`6 passed`**. Bieg na Athenie: `2334`, `Dane: OK`. Alarm na żywych
   danych przy udawanym dniu: 24.09 → trzy braki, 22.09 → trzy wpisy z przyszłości,
   bez zmiennej → `OK` — trzy trafienia co do słowa. Instrukcja:
   `notatki/plany/Notatka-2026-09-23-jak-napisac-testy-drogi.md`. Spełnione (a), (b),
   (e); **niespełnione (c) i (d)**, bo test chodzi ręcznie z laptopa.
   **24.09 notatka projektowa** `notatki/plany/Notatka-2026-09-24-droga-na-ec2.md`, **25.09
   zatwierdzona w całości**, osiem decyzji w wariancie (a):
   - wpięcie do `control.py`, jedna lista problemów i jedno zgłoszenie do stróża (osobna
     linia `cron` z tym samym stróżem kasowałaby awarię późniejszym `OK`);
   - problem z danymi = awaria u stróża;
   - błąd Atheny → problem na liście (wewnętrzny `try`);
   - wspólna `pobierz_dane()` w `path.py`;
   - jedna `KONTROLA_DATA`;
   - czwarte sprawdzenie „spółka z `ticker` bez ani jednego wiersza”, zawsze (luka: pusta
     tabela w weekend dawała `[]`);
   - linia `Kontrola: Dane N wierszy`;
   - ostrzeżenie `pandas` zostaje.

   Instrukcja przed kodem: `notatki/plany/Notatka-2026-09-25-jak-wpiac-droge-do-kontroli.md`.
   **25.09 kod Gracjana:** `path.py` z czwartym sprawdzeniem i `pobierz_dane()`,
   `test_path.py` z 7. testem (`test_brak_spolki_w_sobote`), `control.py` z importem obu
   funkcji, `dzis = date.fromisoformat(KONTROLA_DATA)` przed wewnętrznym `try` (linie 43–49:
   `pobierz_dane()`, `print(f"Kontrola: Dane {len(dane)} wierszy")`, `blad = blad +
   sprawdz_daty(...)`, `except` → `Athena: Błąd - {e}`). Wyniki:
   - `7 passed`;
   - `python kod/path.py` → `2340`, `Dane: OK`;
   - `18 passed in 0.61s` na obu plikach;
   - bieg na bloku z 18.09 → `Kontrola: Dane 2340 wierszy` + `AWARIA` z 3 × wpis z przyszłości,
     co do słowa;
   - zmyślone klucze AWS → jeden problem `Athena: Błąd - An error occurred
     (UnrecognizedClientException) … token … invalid.`, bez linii `Dane`.

   **Nieprzewidziane:** `pyathena` przy błędzie wypisuje na stderr `Failed to execute query.`
   i pełny `Traceback` (ok. 40 linii na 3.14, na 3.9 mniej, nie sprawdzone). Na EC2 trafi to
   do `errors.txt`. **Decyzja Gracjana: zostawić.** Koszt: ręczny bieg `control.py` tego
   samego dnia po powrocie Atheny dalej da `AWARIA` (w bloku jest `Traceback`), a stróż wróci
   na `Up` przy następnym biegu. Commit `8b8f585` (`5 files changed, 752 insertions(+),
   5 deletions(-)`, zgodnie z przewidywaniem), wypchnięty.
   **26.09 etap B zamknięty** (sobota, `pull` ok. 13:56 UTC, przed oknem 17:55): `fc6e262`,
   `13 files changed, 3258 insertions(+), 178 deletions(-)`, `git status --short` pusty przed
   i po. E1 → `Dane 2340`, `OK`; E2 → 4 problemy; E3 → `Athena: Błąd - Execution failed on
   sql …` w 3 liniach (pandas 2.3.3) + 25 linii od `pyathena` (tyle na Pythonie 3.9, co
   domyka „nie sprawdzone” wyżej); E4 → stróż #8 `Failure` 2450 B i #9 `OK`, obie zmiany
   stanu. Wszystko przewidziane przed komendami, wszystko trafione. Pełne wyniki: notatka
   z 24.09, „Wyniki etapu B”, i „Stan 26.09” wyżej. Liczby w „Codziennej kontroli” zmienione
   na 32/30. Stan warunków: (a) ✅, (b) ✅, (c) ✅ `Failure` u stróża i mail `DOWN` na Interii
   o 16:19 (`UP` też 16:19), (d) ✅ pierwszy bieg z `cron` 26.09 o 18:30 sprawdzony tego
   samego wieczoru (blok 808–837, `Kontrola: Dane 2340 wierszy`, `Kontrola: OK`, wszystkie
   liczby z tabeli trafione), (e) ✅ ten opis.
   **Zastrzeżenia:** ~~jeden bieg i to w sobotę~~ — **zdjęte 03.10:** siedem biegów 26.09–02.10
   zgodnych z tabelą, w tym pięć dni giełdowych z „brakuje dzisiejszej świecy” (28.09: blok 32,
   `Dane 2343`). Zostają: w święta w dzień roboczy fałszywy alarm (pierwszy 11.11); nie łapie
   złej ceny przy dobrej dacie ani ubytku dni u wszystkich spółek po równo.
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
10. **Dokumentacja** — ✅ **04.10.** (1) README od nowa (`aaf39b4`): opis potoku z diagramem
    Mermaid, jak projekt pilnuje sam siebie, stan uczciwie z ograniczeniami z decyzji 04.10,
    lekcje z błędów; stary README w `notatki/plany/Historia-projektu.md`. Gracjan: „póki co
    jest ok”, poprawi go przed zakończeniem projektu. (2) Dziesięć wpisów dziennika (21.07,
    10.08, 12.08, 13.08, 17.08, 19.08, 20.08, 21.08, 24.08, 25.08) z „Czego się nauczyłem”
    napisanym z treści wpisów, z dopiskiem, że uzupełnione 04.10 przez Claude'a (dziennik poza
    gitem). Wpisy 22.07–06.08 mają własne sekcje „Nauczone”/„Napotkane błędy i nauka” — bez
    zmian. (3) Plany: w `Plan-ogolny`, `Plan-01`…`Plan-06`, `Codzienna-rutyna`,
    `Stare-repo-co-to-bylo` blok „Status (04.10.2026): dokument historyczny” z tym, co dziś
    obowiązuje (w Plan-04 tabela części A–D, w Plan-06 tabela wątków 1–10); pięć odsyłaczy
    `[[project-…]]` do prywatnych notatek Claude'a (Plan-05, Plan-06) zamienione na tekst.
    Treści planów nie przepisywano — to historia. **Lista napraw z 08.09 zamknięta.**

**Poza listą, zrobione 03.10** (szczegóły w „Stan 03.10”):
- **Kompakcja** z prawdziwym kasowaniem — ✅ `Usunięto 66 plików`, Athena 785 × 3 przed i po.
- **Python 3.14 na EC2** (dawna wada „Python 3.9 na EC2”) — ✅ **06.10**: sobota 03.10 zgodna
  co do linii, dzień giełdowy 05.10 (Kafka → S3) zgodny, zgłoszenie `/fail` 06.10 (#21, 1836 B,
  `python-requests/2.34.2`) zgodne co do bajtu. Zastrzeżenie: maili z testu 06.10 nie
  odczytano w sesji. Stary `venv` do skasowania najwcześniej ok. 17.10.
- **Wykresy na Athenie, `test_plikow.py` usunięty** — ✅ (a)–(d), (e) czeka na README (opis
  `test_plikow.py`, Power BI z danymi do 20.09).

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
  `13.63.105.190`), 22–25.09 #4–#7 `OK` o 18:30, **26.09 16:04 test E4 z nowym
  `control.py`: #8 `Failure` (`POST`, 2450 B, `up → down`) i #9 `OK` (`GET`, `down → up`)**.
  Stróż pisze tylko przy zmianie stanu (dwa dni ciszy dały jeden mail). Mail
  `UP` 21.09: „downtime lasted 1 day, 23 hours", `Status Changed to Up at … 18:30:02 +0200`.
  **Opóźnienie maili: 15 minut, potwierdzone 26.09** (hipoteza z 19.09): zmiany stanu
  o 16:04, maile `DOWN` i `UP` na Interii o 16:19. Nie wiadomo, czy czeka stróż, czy Interia.
  Na co dzień: awaria zgłoszona o 18:30 → mail ok. 18:45; cisza (stróż 19:00) → mail ok. 19:15. Konto bez logowania przez rok jest kasowane. Obsługa
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

**Decyzja Gracjana 04.10 o znanych wadach — wszystko zgodnie z rekomendacją Claude'a:**
- **Naprawić przed stroną (N):** warunek w Producencie przeciw cenie z trwającej sesji
  (czerwona wada, groźna przy ręcznych biegach w dzień roboczy przed 17:00 — notatka, kod,
  wdrożenie na EC2) — **06.10 kod i testy na laptopie zrobione** (`28 passed`, bieg z martwym
  brokerem o 16:45 z dopiskiem przy trzech spółkach), wdrożenie na EC2 07.10; odpięcie `IAMFullAccess` od użytkownika `gpw-tracker-admin` — **✅ 04.10
  ok. 16:20** (Gracjan, konsola jako root): przed — „Last Accessed” dla IAM „19 days ago” (15.09,
  sprawdzanie roli EC2), polityki przy IAM „AWSGlueConsoleFullAccess and 1 more”; po — przy IAM
  samo `AWSGlueConsoleFullAccess` (ta polityka daje część IAM: odczyt ról, przekazanie roli
  Glue), usług 20 → 19; z laptopa `get-caller-identity` bez zmian, `aws s3 ls` 157673/350 B,
  `python kod/path.py` → `2355`, `Dane: OK`, `aws iam list-attached-user-policies` →
  `AccessDenied` („no identity-based policy allows”). Zrzutu zakładki Permissions (3 polityki)
  nie było. EC2 bez wpływu (rola `gpw_tracker_ec2_role`) — potwierdzi bieg 04.10. Powrót:
  Permissions → Add permissions → Attach policies directly → `IAMFullAccess`. Możliwe dalsze
  zawężenie (czy `AWSGlueConsoleFullAccess` jest potrzebne) — osobna decyzja, później. ~~Komentarz „niedobór
  pamięci” w `compaction.py`~~ — **sprawdzone 04.10 po decyzji: nic do naprawy**, w `kod/` nie
  ma takiego słowa, a linia 1 `compaction.py` od 11.09 (`4b535d8`) podaje prawdziwy powód
  (brak `pyarrow` na EC2). Pozycja na liście „do decyzji” była nieaktualna od 11.09.
- **Zostają jako ograniczenia opisane w README (O):** kwadrans zapasu u Yahoo (od 26.09 głośny
  i sam się naprawia); korekty Yahoo wstecz (razem z nimi uśpiony przypadkowy wybór ceny
  w Silverze — naprawiać kiedyś razem); `close()` bez `finally`; ostrzeżenia SQLAlchemy
  i `value_deserializer`; brak planu B dla źródła; nowa spółka (partycja w Athenie + okno
  `range=3y`) — warunek „przed dodaniem spółki”; rozjazd nazw kolumn w rankingu; granice
  kontroli (zła cena przy dobrej dacie, ubytek u wszystkich, fałszywy alarm w święta);
  kompakcja ręczna raz w miesiącu.
- **Później (P):** aktualizacja Amazon Linux — po 17.10, osobna notatka.
- Power BI — odłożony decyzją z 03.10 (README: dane do 20.09).

- Producent uruchomiony przed 17:00 zapisuje cenę z trwającej sesji jako
  zamknięcie.
- Okno na kurs zamknięcia u Yahoo ma najwyżej kwadrans zapasu (11.09:
  o 17:45 brak świecy, o 18:00 jest).
- Testy sprawdzają rzeczy obok potoku — **od 23.09 jest test prawdziwej drogi**
  (`kod/path.py`), od 25.09 wpięty w `control.py`, **od 26.09 na EC2 i w `cron`** (`fc6e262`,
  biegi ręczne E1–E4 i pierwszy bieg z `cron` zgodne — kolejność napraw, punkt 7).
  `test_plikow.py` **usunięty 03.10** (oba jego testy dublowały silniejsze sprawdzenia).
- Nikt nie dowie się o awarii — **zamknięte 21.09 w zakresie sygnału** (patrz „Sygnał awarii"). Log
  podwójny naprawiony w kodzie 19.09: Producent pisze błędy na stderr do
  `errors.txt`, `errors.log` przestał rosnąć (laptop: 6519 bajtów przed
  i po; EC2: 8 linii, potwierdzone 21.09).
- Korekty cen Yahoo nie docierają do S3.
- **Nowe 21.09:** wykresy (`wykresy.py`, `ranking.py`), `test_plikow.py` i Power BI
  czytają lokalne `gold/` i `silver/`, które stoją od 20.09 (Harmonogram wyłączony) —
  pokażą stare dane bez błędu. **03.10: wykresy przepięte na Athenę (z datą ostatniej świecy
  w tytule), `test_plikow.py` usunięty. Zostaje Power BI** — dalej pokazuje dane do 20.09,
  świadomie odłożony (łącznik Athena wymaga sterownika ODBC na laptopie).
- **Nowe 03.10:** `dnf` na EC2 ostrzega o nowszym Amazon Linux (do `2023.12.20260930`, system
  na `2023.12.20260817`) — aktualizacja systemu, osobna decyzja, nie w tym samym tygodniu co
  zmiana Pythona ani 25.10. Stary `venv` (3.9, ok. 0,2 GB) do skasowania najwcześniej ok.
  17.10. Daty na osi X w `wykres3spolek.png` nachodzą na siebie (kosmetyka, było i przed
  zmianą).
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
  - ~~Python 3.10 na EC2~~ — **03.10 Python 3.14 na EC2** (3.10 w Amazon Linux 2023 nie ma),
    czeka na pierwszy dzień giełdowy 05.10;
  - `pd.read_sql` przez SQLAlchemy;
  - ostrzeżenie `value_deserializer`;
  - ~~słowa „niedobór pamięci" w komentarzu `compaction.py`~~ — nieaktualne od 11.09
    (sprawdzone 04.10: komentarz w linii 1 podaje brak `pyarrow`);
  - plan B dla źródła danych;
  - **(15.09) kompakcja, wykresy (`wykresy.py`, `ranking.py`) i Power BI nie
    mają miejsca w kolejności napraw.** Propozycja Claude'a: kompakcja na EC2
    po sygnale awarii i Pythonie 3.10 (w `cron` byłaby comiesięcznym
    kasowaniem, którego nikt nie ogląda); wykresy i Power BI przepiąć na
    Athenę zaraz po wyłączeniu Harmonogramu, bo inaczej pokażą stare dane
    bez błędu **(od 21.09 to się już dzieje: Harmonogram wyłączony)**. Silvera do S3
    nie potrzeba: `gold/dane_dzienne.csv` ma
    wszystkie jego kolumny. **03.10: kompakcja zrobiona ręcznie z laptopa (dalej poza
    `cron`), wykresy przepięte, Power BI odłożony.**

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
- **23.09:** zasady do funkcji i testów podawane po kawałku, dopiero przy ocenie
  wklejonego kodu (`test_` w nazwie, `ticker` zamiast `df["spolka"]`, `[1:]`, liczenie
  problemów ze wszystkich sprawdzeń). Gracjan to wytknął. Stąd dopisek w zasadzie 3
  i notatka „wszystko w jednym miejscu".
- **23.09:** o 16:45 zapowiedziany test alarmu przed 18:10, bez rezerwy na funkcję, testy
  i część z Atheną. Nie zdążyliśmy. Zastąpiony udawanym dniem przez `DROGA_DATA`.
- **23.09:** pierwsze przykłady testów z `* 3` i nazwami wpisanymi na sztywno, a
  `len(...)`, `[0]` i `[1:]` dopiero później, więc Gracjan przepisywał tabele.
- **24.09:** sesja zakończona bez wpisu w dzienniku. To ta sama sytuacja co przed 21.09.
  Dopisany 25.09 z transkryptu.
- **25.09:** komendy wpisane w tekst kroków zamiast w osobne okienka. Gracjan poprosił
  o powrót do okienek (zasada 4).
- **25.09:** `ranking.csv` „ok. 360 B” bez wyliczenia, wyszło 338.
- **25.09:** „`pytest` poniżej sekundy” po zmianie pliku, wyszło 1,62 s. Dowodem braku
  połączenia z Atheną jest brak `warnings summary`, a nie czas.
- **25.09:** bieg ze zmyślonymi kluczami: tekst przewidziany jako `Execution failed on sql …`,
  a przyszedł sam komunikat `botocore`. Nieprzewidziany `Traceback` od `pyathena` na stderr.
- **25.09:** pułapka `in` na kolumnie pandas dopisana do tabeli błędów dopiero po pytaniu
  Gracjana o warunek. Pierwsza wersja warunku Gracjana brzmiała `t not in spolki`.
- **25.09 (znalezione 26.09):** przewidywanie na poniedziałek 28.09 „start w linii 808,
  `wc -l` 836” pominęło weekend — 808 to start sobotniego bloku. **Wniosek: przy
  przewidywaniu na dzień odległy o kilka biegów liczyć każdy bieg po kolei, także weekend.**
- **26.09:** `export`, `unset` i `${#…}` przedstawione jako nowe, a są w słowniku od 19.09
  (używane wtedy z `read -s` przy tym samym adresie). Nowe były tylko `$( )` i `cut -d= -f2-`.
  Słownika nie sprawdziłem przed wiadomością.
- **03.10:**
  - `python3.1?` „łapie 3.11–3.13”, a złapał też 3.14 (`?` to dowolny jeden znak);
  - commit `4aca12d`: przewidziane `127/13`, wyszło `128/14`, bo edytor dopisał koniec ostatniej
    linii `.gitignore`;
  - `venv314` „250–450 MB”, wyszło 205 MB;
  - 2 linie `boto3` w ręcznym Goldzie na starym `venv`: nie było ich, bo ostrzeżenie wychodzi
    przy tworzeniu klienta S3 (`GOLD_DO_S3=1`), nie przy imporcie;
  - `wykresy.py` „24 linie”, ma 27;
  - instrukcja bez ostrzeżenia przed nazwą `max` (dopisana zasada 13 w instrukcji);
  - porcja z testem awarii bez kroku włączającego `venv` i bez wyraźnego przejścia z EC2 na
    laptop (`pytest` z Pythona systemowego), potem „włącz venv” obok „venv nieistotne”. Stąd
    krok PRZEŁĄCZENIE w zasadzie 4;
  - sesja przerwana o 12:32 przed wieczorną kontrolą: dziennik był już zapisany jako szkic,
    więc 04.10 start poszedł z dobrego stanu. CLAUDE.md i słownik czekały do 04.10.
- **03.10 (znalezione 04.10):** przewidywanie na pon. 05.10 „start 1056, `wc -l` 1083”
  pominęło niedzielny bieg (to liczby niedzieli). **Drugi raz ten sam błąd co 25.09.**
  **Wniosek: przewidywania na kolejne dni zawsze jako tabela z wierszem na każdy dzień
  kalendarza** (jak „Przewidywania od 04.10”), nigdy jedną liczbą na „następny dzień
  giełdowy”.
- **04.10:**
  - w tabeli znanych wad zarekomendowałem „naprawić” komentarz „niedobór pamięci”
    w `compaction.py`, biorąc pozycję z listy w CLAUDE.md bez zajrzenia do kodu. Komentarz był
    poprawny od 11.09. Gracjan przyjął rekomendację, więc decyzja stała na nieaktualnej
    przesłance. **Wniosek: przed rekomendacją naprawy otworzyć plik, którego dotyczy;**
  - napisałem, że `Codzienna-rutyna` nie istnieje — istnieje (`notatki/plany/`), nie
    sprawdziłem przed wiadomością;
  - przy liczeniu zmian do commita użyłem `git add -N` (zmiana indeksu) i cofnąłem —
    Claude czyta stan gita, ale go nie zmienia (zasada 5);
  - README zapowiedziany na 150–200 linii, wyszło 254;
  - przy IAM nie przewidziałem, że `AWSGlueConsoleFullAccess` sama daje część IAM (wiersz IAM
    po odpięciu `IAMFullAccess` został, z jedną polityką).
- **06.10:**
  - po zmianach w `data_ingestion.py` nie sprawdziłem pliku i nie opisałem nowych linii z własnej
    inicjatywy; Gracjan musiał poprosić („miałeś to robić za każdym razem”). Dopisane do
    zasady 3;
  - w rozmowie formy rodzajowe zwracające się do Gracjana („sama”, „pominęła”), bez żadnej
    podstawy;
  - instrukcja z 04.10 (Część 8, krok 4): ręczny bieg na EC2 „przed 17:55” bez zastrzeżenia,
    że po 17:00 Yahoo może nie mieć świecy (przy kroku 2 zastrzeżenie było). Poprawione na
    „przed 16:50”.

### Priorytet Gracjana (08.09)

Czysty, działający łańcuch `data_ingestion → Kafka → S3/Athena → silver →
gold` → wynik na stronie. Wykresy, README pod pracodawcę, Power BI —
dopiero potem.

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
w niej instalacja Plotly w `.venv` i dopisanie do `requirements-lokalny.txt`.

### Na następną sesję

Stan 06.10 (wtorek, koniec sesji ok. 19:35). Warunek w Producencie: **kod i testy zrobione na
laptopie 06.10** (`kod/session.py`, `kod/test_session.py`, pięć zmian w `kod/data_ingestion.py`,
`28 passed`, bieg z martwym brokerem o 16:45 z dopiskiem przy trzech spółkach). Komendy commita
podane na koniec sesji 06.10 — na starcie sprawdzić, czy commit jest i czy wypchnięty. Instrukcja
(jedyne odniesienie): `notatki/plany/Notatka-2026-10-04-jak-napisac-warunek-sesji.md` (Część 8
poprawiona 06.10). **Przed każdym kawałkiem kodu: notatka projektowa (zasada 10) i pełna
notatka-instrukcja (zasada 3); po każdej zmianie Gracjana — opis każdej nowej linii (zasada 3).**

**Plan Gracjana z 06.10:** śr. 07.10 — wdrożenie na EC2 i przegląd całości; od czw. 08.10 —
strona, od notatki projektowej.

0. **Na starcie:** czy przyszły maile `DOWN` i `UP` z testu 06.10 (u stróża 19:12, na Interii
   przewidziane ok. 19:27); czy treść #21 u stróża ma polskie litery bez krzaków; `git log -1`
   i `git status --short` na laptopie (commit z 06.10 jest, drzewo czyste).
1. **Śr. 07.10 — wdrożenie, ręczna część przed 16:50** (Część 8 instrukcji, każdy krok
   z przewidywaniem zapisanym przed komendą):
   - z laptopa przed `pull`: `git diff --stat 4aca12d HEAD` — liczba plików do przewidywania
     (EC2 nie ściągał też `96f191b`, `aaf39b4`, `93a5731`, `0f3f882`);
   - EC2: `git status --short` pusty → `git pull` (`4aca12d..` commit z 06.10) → `git status
     --short` pusty, `kod/session.py` jest;
   - ręczny Producent bez `>>`, w trakcie sesji (9:00–16:50):
     `KAFKA_BOOTSTRAP=localhost:9094 venv314/bin/python kod/data_ingestion.py` → 3 × `nowych dni:
     0, wysłane: 0, stan: zapisane, dziś pominięte (przed 17:55)`; potem `LOG-END-OFFSET` dalej
     **2390** (nic nie poszło do Kafki), pliki spółek dalej 787, ostatni wiersz `2026-10-06`.
     Bez dopisku (Yahoo bez świecy) — dowód słabszy, nie błąd. `nowych dni: 1` / `wysłane: 1` —
     warunek nie działa: stop i rozmowa. **Nie w oknie 17:55–18:35;**
   - kontrola po 18:32: start **1140**, `wc -l` **1167**, blok 28, 3 × `nowych dni: 1, wysłane:
     1, stan: zapisane` **bez dopisku** (18:00 > 17:55), `Odebrano 3`, 2 × `(2364, 3)`, `Kontrola:
     Dane 2364 wierszy`, `OK`, zakładka 2393, pliki 788 × 3, S3 ok. 158260–158360 B, stróż #23.
     Zgodność = warunek (d): dzień pominięty po południu przyszedł o 18:00;
   - powrót przy kłopocie: `git revert` na laptopie, `git push`, `git pull` na EC2 — bez ręcznych
     zmian plików na EC2.
2. **Śr. 07.10 — przegląd całości** (zasada 16; lista napraw zamknięta 04.10, przeglądu po niej
   nie było): cały kod + wszystkie notatki od początku, wynik do nowego pliku w `notatki/plany/`.
   Nowe wady → kolejność napraw ustalona z Gracjanem, przed stroną (zasada 15).
3. **Od czw. 08.10 — strona:** notatka projektowa według „Strona — decyzje 06.10” wyżej.
4. **README po zgodnej kontroli 07.10:** ograniczenie „Ręczne uruchomienie Producenta … przed
   17:00” zamienić na opis warunku; wiersz w tabeli `Przeglad-2026-09-08-co-nie-gra.md`.
5. **Stary `venv` na EC2** — do skasowania najwcześniej ok. 17.10, osobna decyzja po dwóch
   tygodniach spokoju (decyzja 6 z notatki o Pythonie). Razem z nim `~/porownanie-1003/`.
6. **Power BI na Athenę** — odłożony 03.10 (sterownik ODBC na laptopie, osobna notatka); na
   stronę nie idzie (decyzja 06.10). Do tego czasu README mówi, że raport pokazuje dane do 20.09.
7. **Aktualizacja Amazon Linux** (ostrzeżenie `dnf` 03.10) — osobna decyzja; nie w tygodniu
   zmiany Pythona ani w tygodniu 25.10. Ewentualne zawężenie `AWSGlueConsoleFullAccess` — też
   osobna decyzja.
8. **Terminy:**
   - **25.10** (niedziela) pierwszy bieg po zmianie czasu — `17:00:0X` w linii startu i to
     będzie poprawne, a u stróża pierwszy prawdziwy sprawdzian strefy;
   - **26.10** (poniedziałek) pierwszy dzień giełdowy zimą — w bloku `nowych dni: 1` bez
     dopisku (strefa w warunku liczy się dobrze także zimą; Część 8, krok 6 instrukcji);
   - **01.11** Gold zmieni linię `Pełna liczba …` z `117`/`111` (doliczyć nowy miesiąc
     i październik jako pełny — przeliczyć przed biegiem, nie z pamięci);
   - **początek listopada** kompakcja za październik (z laptopa, nie między 17:55 a 18:35);
   - **11.11** (środa) pierwszy fałszywy alarm kontroli w święto (mail `DOWN`, 12.11 `UP`);
   - **19.02.2027** koniec darmowego planu AWS (albo wcześniej, gdy skończy się kredyt: 04.10
     zostało **83,44 USD** ze 100, „140 days remaining”; EC2 chodzi 24/7). Przed tą datą
     decyzja: płatny plan, wyłączenie albo zmiana architektury.

**EC2 jest na `4aca12d` od 03.10 ok. 09:2x UTC** (`pull` `fc6e262..4aca12d`, 7 plików;
`git status --short` pusty 04.10 i 06.10). Commitów od `96f191b` (wykresy, usunięty
`test_plikow.py`) EC2 nie ściągał — przyjdą z `pull` 07.10. Poprzednio: `fc6e262` od 26.09,
`6af7b48` od 21.09.

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

**Co z `notatki/` jest w gicie, sprawdzone 11.09.** `notatki/plany/`
i `notatki/Slownik.md` **są śledzone**. Poza gitem, przez `.gitignore`, są
`notatki/dziennik/` i `notatki/.obsidian/`. Znaczy to, że **wszystkie wpisy
dziennika (32 pliki na 15.09), czyli cały zapis nauki z tego projektu,
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
