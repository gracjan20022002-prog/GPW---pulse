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
    zatwierdza, potem kod.

11. **Sprawdzać, nie zakładać.** Przed stwierdzeniem o plikach, danych,
    gicie — czytać i liczyć. Przewidywany wynik pisany **przed**
    uruchomieniem. Gdy Claude nie sprawdził — mówi „nie sprawdziłem".

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

## Stan projektu — uczciwie

Repo: `GPW - pulse`, GitHub `github.com/gracjan20022002-prog/GPW---pulse`.

**Co działa dziś, sprawdzone:** na EC2 (`t3.micro`, Elastic IP
`13.63.105.190`, 24/7) `cron` uruchamia codziennie o 16:00 UTC w jednej
linii `data_ingestion.py ; kafka_consumer.py` (od 09.09, `;` — decyzja
Gracjana; do 08.09 dwie linie 16:00 i 16:02; **pierwszy bieg nowej linii
10.09, do sprawdzenia**) i o 16:10 UTC `silver.py && gold.py`.
`data_ingestion.py`: Yahoo → Kafka, pamięć `companies/*.txt` zapisywana
dopiero po potwierdzeniu brokera (od 08.09); `kafka_consumer.py`: Kafka →
S3 `live/`; Silver+Gold: Athena `bronze UNION live` → CSV na dysku EC2.
Pełny tekst `crontab` w dzienniku 09.09. `bronze` w S3 jest Parquetem do końca poprzedniego
miesiąca, przepisywanym ręcznie przez `compaction.py` (pierwszy bieg
z prawdziwym kasowaniem: 1 października). Lokalny Harmonogram Windows
liczy Silver+Gold równolegle o 18:10 jako „zapas".

**Co nie działa albo zagraża danym:** pełna lista z wagami, liniami
i uzasadnieniem w
[`notatki/plany/Przeglad-2026-09-08-co-nie-gra.md`](notatki/plany/Przeglad-2026-09-08-co-nie-gra.md)
— **to jest źródło prawdy o stanie projektu**, nie README. Kolejność
napraw z Części 5 tego pliku **zatwierdzona przez Gracjana 08.09**.
Wciąż otwarte (najkrócej): wynik Golda kończy na dysku EC2 i nic go nie
czyta; Producent zapisuje cenę z trwającej sesji jako zamknięcie, gdy
uruchomić go przed 17:00; testy sprawdzają rzeczy obok potoku; nikt nie
dowie się o awarii; ranking „najbardziej zmiennego miesiąca" jest błędny
w pierwszym tygodniu miesiąca; martwy kod i konfiguracja na sztywno;
README obiecuje więcej, niż jest; dziesięć wpisów dziennika bez „Czego
się nauczyłem".

**Naprawione 08.09, sprawdzone:** (1) Producent zapisuje pamięć
„wysłane" dopiero po potwierdzeniu każdej wiadomości przez brokera
(`send(...).get(timeout=10)`, flaga per spółka) — test lokalny z martwym
brokerem + prawdziwy bieg `cron` na EC2; (2) kompakcja pobiera obecny
`bronze` z S3 do `bronze/poprzedni/` i przerywa `assert`-em przed
jakimkolwiek zapisem, gdy liczba wierszy spółki zmalała — obie ścieżki
sprawdzone biegiem (761 vs 740); (3) Konsument `auto_offset_reset=
'earliest'` — zwykła ścieżka sprawdzona 09.09 przez `cron` (2333/2333,
LAG 0).

**09.09, sprawdzone:** zwykła ścieżka Konsumenta z `'earliest'` przez
`cron` — liczby przewidziane przed biegiem (`Odebrano 3`, 768 wierszy,
`(2304, 3)`, 2333/2333) wszystkie trafione. **Fakt poprawiający wpis
z 08.09:** zalew z 01.09 **wciąż leży w topicu** — `earliest` = 22,
`latest` = 2330, offsety 22–2326 w zamkniętym segmencie `...0022.log`
(ostatnia wiadomość 07.09 16:00 UTC); broker skasuje go około 14.09
16:00 UTC. Kafka kasuje całymi segmentami, wiadomość żyje 7–14 dni.
**Test „zakładki nie ma" NIE przed 14.09.** **09.09, wdrożone,
sprawdzenie 10.09:** Producent i Konsument w jednej linii `crontab`
(każdy skrypt ze swoim `>> errors.txt 2>&1`); kopia sprzed edycji
`~/crontab-kopia-0909.txt` na EC2. Kod Pythona 09.09 bez zmian.

**Priorytet Gracjana (08.09):** czysty, działający łańcuch
`data_ingestion → Kafka → S3/Athena → silver → gold` → wynik na stronie.
Wykresy, README pod pracodawcę, Power BI — dopiero potem.

**Następna sesja (10.09), ustalone z Gracjanem:**
1. **Po 18:12 sprawdzić pierwszy bieg nowej linii `crontab`** (liczby
   policzone 09.09): w `errors.txt` ścieżka i trzy adresy Yahoo od
   Producenta **przed** `Odebrano 3 wiadomości` (dowód, że przekierowanie
   łapie oba skrypty), `(2307, 3)` dwa razy, pliki spółek 769 wierszy,
   `--describe` 2336/2336, LAG 0. Komendy: `grep -n "data_ingestion.py\|
   yahoo\|Odebrano\|^(" ~/GPW---pulse/companies/errors.txt | tail -n 7`,
   `wc -l ~/GPW---pulse/companies/*.WA.txt`, `--describe`. Dopiero wtedy
   krok „jedna linia `crontab`" jest zrobiony — zaktualizować tabelę
   w przeglądzie. Gdyby coś nie grało: `crontab ~/crontab-kopia-0909.txt`
   przywraca stan sprzed edycji.
2. **Test ścieżki „zakładki nie ma" — NIE przed 14.09** (Gracjan prosił,
   żeby o teście pamiętać; 09.09 odłożony, bo zalew z 01.09 wciąż leży
   w topicu i `'earliest'` wlałby go drugi raz). Termin do wyboru
   Gracjana: 14.09 po 18:15 albo 15.09 przed 18:00 (Claude proponował
   15.09). Najpierw `~/kafka_2.13-4.3.1/bin/kafka-get-offsets.sh
   --bootstrap-server localhost:9094 --topic gpw_tracker --time earliest`
   ma pokazać `2327`; jeśli mniej — nie kasować grupy. Potem notatka
   projektowa, `--describe`, `--delete --group gpw_consumer`, ręczny bieg
   Konsumenta z `KAFKA_BOOTSTRAP=localhost:9094`, `--describe`, `aws s3
   ls` na `live/` z lokalnego PowerShella. Oczekiwane `Odebrano N`,
   N = `latest` − 2327; po jednym dodatkowym pliku na spółkę w `live`
   (powtórki tych samych wiadomości — Silver odsieje, kompakcja skasuje
   1.10).
3. **Krok 4 z przeglądu: sprzątanie kodu i konfiguracji** — najpierw
   notatka projektowa z listą do zatwierdzenia: martwy kod i `print`-y
   (Producent, Silver, Gold, testy), bucket/region/baza do `config.py`,
   `timeout` w `requests.get` (nowe, 09.09), `CRON_TZ`, pliki-śmieci,
   trzy ostrzeżenia bibliotek w logu. Gracjan wybiera zakres, potem
   edycje.
4. Dalej kroki 5–10 z przeglądu, po kolei.

Kopie: pamięć Producenta `~/pamiec-kopia-0809/` (Windows), poprzedni
`bronze` w `bronze/poprzedni/` (poza gitem), `crontab` sprzed 09.09
`~/crontab-kopia-0909.txt` (EC2).

## Gdzie co jest

Kod, dane i notatki razem w folderze projektu: `kod/`, `companies/`
(pamięć Producenta, **poza gitem**, każda maszyna ma własną), `bronze/`
(poza gitem), `silver/`, `gold/` (w gicie — do zmiany, gdy wynik trafi
do S3), `wykresy/`, `notatki/` (plany, słownik, dziennik i `.obsidian`
poza gitem), `aws/` (klucz SSH, poza gitem). Nauka Pythona (osobny
projekt): `DE/Python_l/`.

Połączenie z EC2: z folderu `aws\aws ec2 key`:
`ssh -i "gpw-tracker-key.pem" ec2-user@13.63.105.190`. Repo na EC2:
`~/GPW---pulse`, `venv` bez kropki: `~/GPW---pulse/venv/bin/python`.
Log `cron`: `~/GPW---pulse/companies/errors.txt`.
