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

## Stan projektu — uczciwie (18.09 wieczorem)

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
  **Od 17.09 na EC2:** `enable_auto_commit=False` w konstruktorze
  i `consumer.close()` w ostatniej linii. Zakładka przesuwa się **tylko** po
  udanym zapisie do S3 — wcześniej biblioteka zapisywała ją sama co 5 s,
  w trakcie pętli, czyli przed zapisem. Dowody, testy i ograniczenia:
  `notatki/plany/Notatka-2026-09-17-zakladka-przed-zapisem.md`.
  **Uwaga:** `close()` stoi za `put_object`, więc przy awarii zapisu się nie
  wykonuje i broker przez kilkanaście sekund widzi martwego członka grupy.
  To blokuje `--reset-offsets`, który wymaga grupy nieaktywnej.
  **18.09 pierwszy bieg z `cron` na nowym Konsumencie:** `Odebrano 3
  wiadomości`, blok zgodny co do linii. Zakładki tego dnia nie odczytaliśmy.
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
- **Lokalny Harmonogram Windows** liczy Silver+Gold równolegle o 18:10 jako
  „zapas" (`kod/pipeline.bat`, pełne ścieżki do `.venv\Scripts\python.exe`).
  Od 15.09 z nowym `gold.py`, bez przełącznika, więc nic nie wysyła do S3.

**Normalny blok jednego biegu w `errors.txt`, stan od 17.09:**
- w dzień giełdowy **28 linii**: Producent 4, ostrzeżenie `kafka-python` 2,
  `boto3` 2, `Odebrano` 1, `pandas` 2, Silver 1, Gold 12, ostrzeżenie
  `boto3` w Goldzie 2 (osobny program), 2 × `S3: wysłano`;
- bez nowych wiadomości **26 linii**, bo Konsument tworzy klienta S3,
  a z nim ostrzeżenie `boto3`, tylko wtedy, gdy ma co zapisać.
- Zmiany w Konsumencie z 17.09 **nie dodają ani nie ujmują linii**. Gdyby
  blok się zmienił, znaczyłoby to, że zmieniło się coś jeszcze.

Stan 18.09 po biegu: blok 28 linii od linii 583 (`16:00:02` UTC), więc
`errors.txt` ma 610 linii — wynika z bloku, `wc -l` nie uruchomiony. Silver
i Gold po `(2325, 3)`: trzy powtórki z testu B (17.09) odsiane, dokładnie
jak przewidzieliśmy. **Nieodczytane 18.09:** zakładka (przewidywana
`2354 2354 0`), pliki spółek (775), `COUNT(*)` w Athenie (2325). Ranking:
CBF 202,80, SNT 352,60, XTB 150,34. `errors.log` 8 (stan z 17.09). W `live/`
nadal trzy powtórki z testu B — kompakcja 1.10 wypisze o trzy pliki więcej.
W S3 `gold/` pliki z biegu `cron` na EC2, więc EC2 i Athena liczą to samo.

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
   zgodnie z przewidywaniem. **Zakładka, `wc -l` i `COUNT(*)` nieodczytane**
   — warunek (a) potwierdzony w logu, liczby do domknięcia.
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
6. **Wyłączenie lokalnego Harmonogramu, `silver/` i `gold/` poza gitem** —
   ⬜.
7. **Test prawdziwej drogi** — ⬜.
8. **Sygnał awarii** — 🟨 **18.09 w toku**, wzięty przed 6 i 7 decyzją
   Gracjana. Dotyczy wszystkiego: **każde ✅ wyżej ma niespełniony warunek
   (c)**, bo awarię widać tylko w logu, którego nikt nie czyta. Stan
   szczegółowo niżej, w „Sygnał awarii — stan 18.09".
9. **Pełne miesiące w rankingu** — ✅ 12.09 lokalnie, 14.09 na EC2, wzięte
   poza kolejnością.
10. **Dokumentacja** — ⬜ w tle: README od nowa, dziesięć wpisów dziennika
    bez „Czego się nauczyłem", plany do posprzątania.

### Sygnał awarii — stan 18.09

Notatka: `notatki/plany/Notatka-2026-09-18-sygnal-awarii.md`, **zatwierdzona
w całości**. Dwa słowa, żeby się nie mylić: **skrypt kontrolny** to nasz
skrypt na EC2, który ocenia dzisiejszy blok; **stróż** to usługa poza EC2
(healthchecks.io), która czeka na zgłoszenie i pisze e-mail, gdy nie
przyjdzie albo przyjdzie z awarią.

- **Decyzje:** stróż zewnętrzny, plan darmowy (nie SNS — sama SNS nie
  złapie martwego EC2 ani niedziałającego `cron`); „dowód sukcesu" zamiast
  szukania złych słów: `stan: zapisane` przy każdej spółce z
  `config.ticker`, `Odebrano`, 2 × `S3: wysłano`, zero `Traceback`;
  Producent pisze błędy do `errors.txt` (koniec osobnego `errors.log`);
  adres zgłoszenia jako `STROZ_URL` w `crontab`, **nigdy w gicie**; skrypt
  kontrolny o 18:30 polskiego, zapas 30 minut, strefa `Europe/Warsaw`
  w stróżu (nie UTC — inaczej 25.10 fałszywy alarm).
- **U stróża:** konto założone przez Gracjana. Zadanie `GPW - bieg dzienny`
  (Cron `30 18 * * *`, `Europe/Warsaw`, Grace 30 min) — **zapisu nie
  potwierdziliśmy w rozmowie**. Zadanie w stanie *New* nie alarmuje
  (sprawdzone w kodzie stróża). **Od pierwszego zgłoszenia stróż czeka
  codziennie o 18:30** — wdrożenie na EC2 za jednym posiedzeniem albo
  zadanie w *Paused*. Konto bez logowania przez rok jest kasowane.
  Obsługa stróża to jedna osoba — sami piszą, że możliwe są przerwy
  wielodniowe.
- **Kod na laptopie:** `kod/control.py` — `sprawdz_blok(blok, spolki, dzis)`
  zwraca listę problemów, `wytnij_blok(tekst)` wycina blok od ostatniej
  linii startu i odsiewa linie zaczynające się od `Kontrola:`;
  `kod/test_control.py` — 11 testów na prawdziwym bloku z 18.09
  (`kod/dane_testowe/blok_2026-09-18.txt`), według Gracjana wszystkie
  przechodzą (wynik ośmiu pierwszych wklejony, `8 passed`). Nazwa
  `control.py`, nie `kontrola.py` z notatki — wybór Gracjana.
- **Dwie pułapki znalezione 18.09, obie w notatce:**
  - komunikaty skryptu kontrolnego zawierają szukane słowa, więc drugi bieg
    tego samego dnia widziałby własną linię i uznał awarię za komplet —
    stąd odsiew i test `test_powtorna_kontrola`. **Linia wyniku skryptu
    musi zaczynać się od `Kontrola:`**;
  - polskie litery w treści zgłoszenia: EC2 ma `urllib3==1.26.20`, który
    oddaje tekst do `http.client`, a ten koduje latin-1 →
    `UnicodeEncodeError`. Laptop (`urllib3==2.7.0`) koduje UTF-8, więc test
    na laptopie tego nie pokaże. Treść wysyłać jako `.encode("utf-8")`.
- **Brakuje:** części głównej `control.py` pod `if __name__ == "__main__":`
  (odczyt `errors.txt`, propozycja: ścieżka z `KONTROLA_LOG` do testów na
  kopii logu; linia `Kontrola: …`; `get` przy komplecie, `post …/fail`
  z powodem i blokiem przy awarii; bez `STROZ_URL` nic nie wysyła); jednej
  zmiany w `data_ingestion.py` (`basicConfig` bez `filename`); wdrożenia na
  EC2; testów 2–5 z notatki; biegu z `cron` o 18:30.
- **Blok w `errors.txt` po wdrożeniu:** 29 linii w dzień giełdowy, 27 bez
  nowych wiadomości.

### Wciąż otwarte (najkrócej, pełne opisy w przeglądzie)

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
    bez błędu. Silvera do S3 nie potrzeba: `gold/dane_dzienne.csv` ma
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

### Priorytet Gracjana (08.09)

Czysty, działający łańcuch `data_ingestion → Kafka → S3/Athena → silver →
gold` → wynik na stronie. Wykresy, README pod pracodawcę, Power BI —
dopiero potem.

### Na następną sesję

**Temat w toku: sygnał awarii.** Gracjan poprosił, żeby następną sesję
zacząć od **spokojnego wyjaśnienia każdego z 11 testów** w
`kod/test_control.py` — jak działa i dlaczego tak wygląda. Dalej, jeśli
Gracjan zechce, według listy.

1. **Wyjaśnienie testów**, test po teście, z wejściem i wyjściem.
2. **Domknięcie biegu z 18.09** — trzy odczyty, których 18.09 nie było:
   `wc -l` na `companies/*.txt`, zakładka, `COUNT(*)` w Athenie. Przed 18:00
   19.09 przewidywania jak 18.09: `errors.txt` 610, pliki spółek po 775,
   zakładka `2354 2354 0`, `COUNT(*)` 2325. **Po biegu w sobotę 19.09**
   (bez nowych danych, bez skryptu kontrolnego): linia startu **611**
   z `16:00:0X` UTC, blok **26 linii**, `errors.txt` **636**, 3 ×
   `nowych dni: 0, wysłane: 0, stan: zapisane`, `Odebrano 0 wiadomości`,
   2 × `(2325, 3)`, 2 × `S3: wysłano`, zakładka dalej `2354 2354 0`, pliki
   spółek po 775, `COUNT(*)` 2325.
3. **Czy zadanie u stróża jest zapisane** w stanie *New*.
4. **Ceny z 18.09 w archiwum GPW** (gpw.pl, Archiwum notowań, data
   18-09-2026): nasz ranking ma CBF 202,80, SNT 352,60, XTB 150,34. O 17:51
   18.09 archiwum jeszcze ich nie miało.
5. **Część główna `control.py`**, potem zmiana logu w Producencie, commit
   i push, wdrożenie na EC2 z testami 2–4 z notatki — **jednym
   posiedzeniem**, z zapasem przed 18:30, bo od pierwszego zgłoszenia stróż
   czeka codziennie. Po wdrożeniu blok 29 / 27 linii.
6. **Terminy:** 1.10 kompakcja z laptopa (wypisze o 3 pliki więcej z powodu
   testu B); **25.10** (niedziela) pierwszy bieg po zmianie czasu —
   `17:00:0X` w linii startu i to będzie poprawne; po wdrożeniu też pierwszy
   sprawdzian strefy u stróża.

**EC2 stoi na `033107f`.** Laptop i GitHub są po 18.09 dalej, ale to dane,
dokumentacja i jeszcze nieużywany `control.py` — EC2 na razie nic z tego nie
potrzebuje. Przy `git pull` — rytuał z zasady 14.

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
  - `~/crontab-nowy-0917.txt` to plik wgrany 17.09 (pięć linii).

## Gdzie co jest

Kod, dane i notatki razem w folderze projektu: `kod/`, `companies/`
(pamięć Producenta, **poza gitem**, każda maszyna ma własną), `bronze/`
(poza gitem), `silver/`, `gold/` (w gicie — do zmiany, gdy wynik trafi
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
