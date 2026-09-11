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
Gracjana; do 08.09 dwie linie 16:00 i 16:02; **sprawdzone biegiem
10.09**) i o 16:10 UTC `silver.py && gold.py`.
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
dowie się o awarii, a **log jest podwójny i czytamy tylko jedną połowę**
(`logging.error` → `errors.log`, `print` i `Traceback` → `errors.txt`;
nowe, 10.09); **ranking „najbardziej zmiennego miesiąca" nie jest po
prostu błędny, on miga z dnia na dzień** (XTB: 08.09 `2026-09`, 10.09
`2025-01`, 11.09 znowu `2026-09` — niedokończony miesiąc przeskakuje
pełny i wraca; ograniczenie „pierwszy tydzień" było za łagodne, 11.09
to dziewiąty dzień notowań); **okno na kurs zamknięcia ma najwyżej
kwadrans zapasu** (11.09 o 17:45 Yahoo nie miało jeszcze dzisiejszej
świecy, o 18:00 miało — nowe, zmierzone); README obiecuje więcej, niż
jest; dziesięć wpisów dziennika bez „Czego się nauczyłem".

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
**Test „zakładki nie ma" NIE przed 14.09.** Producent i Konsument
w jednej linii `crontab` (każdy skrypt ze swoim `>> errors.txt 2>&1`);
kopia sprzed edycji `~/crontab-kopia-0909.txt` na EC2. Kod Pythona 09.09
bez zmian.

**10.09, sprawdzone:** (1) **jedna linia `crontab` zamknięta** — bieg
`cron` trafił wszystkie cztery liczby przewidziane 09.09: ścieżka i trzy
adresy Yahoo **przed** `Odebrano 3 wiadomości`, `(2307, 3)` dwa razy,
769 wierszy w plikach spółek, grupa 2336/2336 przy LAG 0; niezależnie
potwierdzone z Windowsa (lokalny Silver o 18:10 wyciągnął z Atheny 2307
wierszy z dzisiejszą datą). (2) **krok 4, sprzątanie kodu, zrobiony
i sprawdzony lokalnie**, commit `fe47920`: `timeout=(10, 30)`
w `requests.get` (sprawdzone obiema drogami — `0.001` daje trzy wpisy
o błędzie w odstępie 30 ms i pliki nietknięte, wartość docelowa daje trzy
adresy Yahoo i zero wpisów); martwy kod i cztery pliki-śmieci usunięte
(`kod` w gicie 12 → 10 plików, `pipeline.bat` **zostaje**, uruchamia go
Harmonogram Windows); bucket/region/baza/adres Atheny do `config.py`
jako `BUCKET`, `REGION`, `BAZA`, `WYNIKI_ATHENY` (bucket z sześciu miejsc
do jednego; dowód: `git diff` na `silver/` i `gold/` pusty, plik
identyczny co do bajta); sześć z dziewięciu `print`-ów z Golda, jeden
z testów, martwy import `ticker` z Konsumenta. **Na EC2 dopiero po
`git pull` 11.09.** (3) `errors.log` na EC2 przeczytany pierwszy raz:
osiem linii, wszystkie z 31.08, z ręcznych biegów bez `KAFKA_BOOTSTRAP`,
ze starą wersją mylącego komunikatu — cisza od 31.08 jest prawdziwa.
(4) grunt pod `CRON_TZ` sprawdzony czterema odczytami (cronie 1.5.7,
napis `CRON_TZ` w `/usr/sbin/crond`, strefa UTC, `Europe/Warsaw` obecna).

**Odłożone świadomie 10.09:** podsumowanie w Producencie zamiast jego
dwóch `print`-ów (nie da się sprawdzić bez żywego brokera, a wysyłka
zepsułaby sprawdzenie linii `crontab`); trzy ostrzeżenia bibliotek
i `requirements.txt` (osobne decyzje, nie sprzątanie).

**11.09, sprawdzone:** (1) **krok 4 zamknięty na EC2** — `git checkout --
silver/ gold/`, `git pull` (sześć commitów, EC2 stało na `eba2eef`),
i wieczorny bieg `cron` trafił **wszystkie sześć liczb policzonych przed
biegiem**: `errors.txt` 417 → 440, blok jednego biegu 49 → 23 linie, sam
blok Golda 37 → 11, pliki spółek 770, `errors.log` dalej 8, grupa
2339/2339 przy LAG 0; w bloku ani `dtype:`, ani wierszy 748–752, ani
samotnej liczby `38`. Potwierdzenie niezależne z Windowsa: lokalny
`clean_data.csv` 2311 linii i ranking identyczny co do ostatniej cyfry,
mimo trzynastu różnic w pakietach i dwóch wersji Pythona. (2)
**podsumowanie w Producencie napisane i sprawdzone lokalnie** — linia
startu z datą i godziną zamiast ścieżki, potem linia na spółkę z liczbą
nowych dni, liczbą wysłanych i stanem pamięci; test z martwym brokerem
(`127.0.0.1:9092`) dał `nowych dni 7, wysłane 0, stan nietknięte` trzy
razy, pliki nietknięte przy 762 wierszach, `errors.log` +4 (trzy z tych
linii pisze biblioteka `kafka`, nie nasz kod). **Na EC2 nie trafiło** —
kod jest w gicie, EC2 dostanie go dopiero przy `git pull`. Notatka:
`notatki/plany/Notatka-2026-09-11-podsumowanie-w-producencie.md`.
(3) **spisy wymagań rozdzielone na dwie maszyny** — `requirements.txt`
przez `git mv` na `requirements-lokalny.txt` (32 paczki, Python 3.14.2),
nowy `requirements-ec2.txt` (19 paczek, Python 3.9.25), oba czystym
`pip freeze` bez komentarzy, żeby porównanie działało jedną komendą.
Czternastu paczek na EC2 brakuje i **wszystkie mają wyjaśnienie**:
siedem ciągnie `matplotlib`, cztery `pytest`, plus te dwa narzędzia
i `pyarrow`; jedyna nadwyżka `pytz` to zależność pandas 2. Nic nie
brakuje przypadkiem. Notatka:
`notatki/plany/Notatka-2026-09-11-wymagania-dwie-maszyny.md`.
(4) `compaction.py` ma komentarz „wyłącznie lokalnie"; README poprawiony
w zdaniu, które twierdziło, że bez `pyarrow` projekt nie ruszy.

**Trzy pomyłki Claude'a 11.09, wszystkie sprostowane przez przeczytanie
repozytorium:** zapowiedział trzy commity przy `git pull`, było sześć
(nie sprawdził wcześniej, na czym stoi EC2); powiedział, że decyzja
o `pyarrow` nie jest nigdzie zapisana, a jest w trzech miejscach
(dziennik 04.09, Plan-06, przegląd 2.8); powiedział, że wada rankingu
jest znana tylko z opisu, a przegląd 2.6 opisuje ją jako zaobserwowaną.

**Priorytet Gracjana (08.09):** czysty, działający łańcuch
`data_ingestion → Kafka → S3/Athena → silver → gold` → wynik na stronie.
Wykresy, README pod pracodawcę, Power BI — dopiero potem.

**Następna sesja (12.09), ustalone z Gracjanem 11.09:**
1. **Zaczynamy od naprawy rankingu miesięcznego** — decyzja Gracjana
   z 11.09, **poza kolejnością** z przeglądu (to punkt 9 z dziesięciu).
   Powód: 11.09 zobaczyliśmy, że wada nie jest stała, tylko **miga** —
   XTB pokazał `2026-09`, potem `2025-01`, potem znowu `2026-09` w ciągu
   czterech dni. Liczba zmieniająca się bez powodu widocznego dla
   czytelnika jest gorsza niż liczba stale zła, bo zabiera zaufanie także
   do sąsiednich liczb. Rzecz siedzi w `kod/gold.py`, w grupowaniu po
   spółce i miesiącu z odchyleniem standardowym. **Najpierw notatka
   projektowa**: co znaczy „pełny miesiąc", co zrobić z miesiącem
   bieżącym, co gdy spółka ma dziurę w danych, jak to sprawdzimy. Potem
   kod pisany przez Gracjana.
2. **Podsumowanie w Producencie na EC2.** Kod jest w gicie od 11.09
   i sprawdzony lokalnie z martwym brokerem. Brakuje testu na żywym
   brokerze, a jedyna bezpieczna droga to zwykły bieg `cron` — ręczne
   uruchomienie z laptopa wysłałoby osiem dni razy trzy spółki, bo
   lokalna pamięć kończy się na 1 września. Oczekiwane w `errors.txt`:
   linia startu z datą i godziną (na EC2 pokaże **czas uniwersalny**,
   czyli `16:00`, nie `18:00`), potem `nowych dni 1, wysłane 1, stan
   zapisane` trzy razy; długość bloku bez zmian, cztery linie za cztery.
   **Można to sprawdzić tym samym biegiem co ranking**, bo obie zmiany
   dotykają różnych linii logu i odchylenie da się przypisać. Liczby dla
   obu policzyć **przed** biegiem.
3. **`CRON_TZ` — Gracjan prosił 10.09, żeby zrobić to w jednej
   z najbliższych sesji.** Grunt sprawdzony (cronie 1.5.7, napis
   `CRON_TZ` obecny w `/usr/sbin/crond`, strefa systemu UTC,
   `Europe/Warsaw` obecna). **PUŁAPKA: samo dopisanie
   `CRON_TZ=Europe/Warsaw` przesuwa bieg dwie godziny wstecz**, bo cron
   przeczyta obecne `0 16` i `10 16` jako szesnastą **polską** —
   Producent pobierałby cenę godzinę przed zamknięciem GPW i zapisywał ją
   jako kurs zamknięcia. Strefa i godziny (`16` → `18`) muszą pójść
   **jednym ruchem**. Nie w dniu, w którym inny bieg ma coś potwierdzać.
   Rytuał jak 09.09: `crontab -l > ~/crontab-kopia-RRMM.txt`, praca na
   drugiej kopii, `diff`, `crontab plik`; nigdy `crontab -e`. Korzyść
   uboczna: bez tego po zmianie czasu EC2 przesunie się na 17:00,
   a Harmonogram Windows zostanie na 18:10, i maszyny rozjadą się
   o godzinę. **Waga podniesiona 11.09:** zmierzyliśmy, że okno na kurs
   zamknięcia ma najwyżej kwadrans zapasu (o 17:45 Yahoo nie miało
   jeszcze świecy za ten dzień, o 18:00 miało), więc przesunięcie biegu
   w którąkolwiek stronę jest groźniejsze, niż się wydawało.
4. **Test ścieżki „zakładki nie ma" — NIE przed 14.09** (Gracjan prosił,
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
5. **Zostało sześć kroków z dziesięciu** w kolejności napraw
   z przeglądu: 5 wynik Golda do S3 i Atheny, 6 wyłączenie lokalnego
   Harmonogramu i `silver/` `gold/` poza gitem, 7 test prawdziwej drogi,
   8 sygnał awarii, 9 pełne miesiące w rankingu (bierzemy jako pierwsze,
   poza kolejnością), 10 dokumentacja. Kroki 1–4 zamknięte i sprawdzone
   na EC2, krok 4 dnia 11.09.
6. **Poza kolejnością, otwarte decyzje:** Python 3.10 na EC2 — jedyna
   z tych spraw, która pogarsza się sama z upływem czasu, bo `boto3`
   porzucił Pythona 3.9 w kwietniu 2026; przejście `pd.read_sql` na
   SQLAlchemy; ostrzeżenie `value_deserializer` w Konsumencie (najmniej
   pilne); poprawka słów „niedobór pamięci" w komentarzu
   `compaction.py` — prawdziwym powodem jest brak biblioteki, nie brak
   pamięci.
7. **1 października: pierwsza kompakcja z prawdziwym kasowaniem,
   wyłącznie z laptopa.** Na EC2 nie ma `pyarrow` i jest to decyzja
   z 04.09, nie usterka: `silver.py` nie otwiera plików z S3, tylko pyta
   Atenę, a ona czyta Parquet po swojej stronie.

Kopie: pamięć Producenta `~/pamiec-kopia-0809/` (Windows), poprzedni
`bronze` w `bronze/poprzedni/` (poza gitem), `crontab` sprzed 09.09
`~/crontab-kopia-0909.txt` (EC2).

## Gdzie co jest

Kod, dane i notatki razem w folderze projektu: `kod/`, `companies/`
(pamięć Producenta, **poza gitem**, każda maszyna ma własną), `bronze/`
(poza gitem), `silver/`, `gold/` (w gicie — do zmiany, gdy wynik trafi
do S3), `wykresy/`, `notatki/`, `aws/` (klucz SSH, poza gitem). Nauka
Pythona (osobny projekt): `DE/Python_l/`.

**Co z `notatki/` jest w gicie, sprawdzone 11.09** — poprzedni opis w tym
miejscu był nieprawdziwy. `notatki/plany/` i `notatki/Slownik.md`
**są śledzone**. Poza gitem, przez `.gitignore`, są `notatki/dziennik/`
i `notatki/.obsidian/`. Znaczy to, że **dwadzieścia jeden wpisów
dziennika, czyli cały zapis nauki z tego projektu, istnieje wyłącznie na
laptopie i w OneDrive, ani jeden nie jest w repozytorium**. Decyzja, czy
ma tak zostać, należy do Gracjana i nie była dotąd nigdzie uzasadniona.

Spisy wymagań od 11.09: `requirements-lokalny.txt` (laptop, 32 paczki,
Python 3.14.2) i `requirements-ec2.txt` (EC2, 19 paczek, Python 3.9.25).
Pliku o nazwie `requirements.txt` **celowo nie ma** — to konwencja,
z której ktoś odruchowo zainstalowałby zły zestaw.

Połączenie z EC2: z folderu `aws\aws ec2 key`:
`ssh -i "gpw-tracker-key.pem" ec2-user@13.63.105.190`. Repo na EC2:
`~/GPW---pulse`, `venv` bez kropki: `~/GPW---pulse/venv/bin/python`.
Log `cron`: `~/GPW---pulse/companies/errors.txt`.
