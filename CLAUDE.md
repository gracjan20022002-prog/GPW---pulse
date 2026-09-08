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
`13.63.105.190`, 24/7) `cron` uruchamia codziennie o 16:00/16:02/16:10 UTC
`data_ingestion.py` (Yahoo → Kafka, pamięć `companies/*.txt` zapisywana
dopiero po potwierdzeniu brokera — od 08.09), `kafka_consumer.py`
(Kafka → S3 `live/`), `silver.py && gold.py` (Athena `bronze UNION live` →
CSV na dysku EC2). `bronze` w S3 jest Parquetem do końca poprzedniego
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
'earliest'` — retencja na EC2 domyślna (7 dni), grupa `gpw_consumer`
z zakładką 2330/2330, LAG 0.

**Priorytet Gracjana (08.09):** czysty, działający łańcuch
`data_ingestion → Kafka → S3/Athena → silver → gold` → wynik na stronie.
Wykresy, README pod pracodawcę, Power BI — dopiero potem.

**Następna sesja (09.09), ustalone z Gracjanem:**
1. Sprawdzić `errors.txt` na EC2 po 18:12 poprzedniego dnia — `Odebrano 3
   wiadomości`, plik spółki 768 wierszy (zwykła ścieżka `'earliest'`).
2. **Test ścieżki „zakładki nie ma"** (Gracjan prosił, żeby o tym
   pamiętać): `kafka-consumer-groups.sh --delete --group gpw_consumer`,
   ręczny bieg Konsumenta z jawnym `KAFKA_BOOTSTRAP=localhost:9094`,
   ponowne `--describe`. Z `'earliest'` ma odczytać wiadomości
   z ostatniego tygodnia (> 0); zostawi po jednym dodatkowym pliku na
   spółkę w `live` — dedup je odrzuci, kompakcja skasuje 1.10.
3. **Krok 3(b): Producent i Konsument w jednej linii `crontab`** zamiast
   16:00 i 16:02. Decyzja Gracjana: `;` (Konsument rusza zawsze) czy `&&`
   (nie rusza po awarii Producenta) — to nie to samo co `silver && gold`.
   Notatka projektowa przed edycją, `crontab -l` po niej.
4. Dalej kroki 4–10 z przeglądu, po kolei.

Kopie z 08.09: pamięć Producenta `~/pamiec-kopia-0809/` (Windows),
poprzedni `bronze` w `bronze/poprzedni/` (poza gitem).

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
