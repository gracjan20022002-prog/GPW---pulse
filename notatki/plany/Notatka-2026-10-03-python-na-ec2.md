# Notatka 03.10.2026 — nowy Python na EC2

Status: **zatwierdzona przez Gracjana 03.10** — decyzje 1, 2, 3, 4, 6 zgodnie z rekomendacją,
decyzja 5 inaczej: **przepięcie dziś, w sobotę 03.10** (szczegóły na końcu). Kodu projektu ta
zmiana nie rusza, zmienia środowisko, w którym kod chodzi na EC2.

## Sedno w trzech zdaniach

1. EC2 chodzi na Pythonie 3.9, a `boto3` (biblioteka do S3 i Atheny) od kwietnia 2026 nie
   wydaje już dla niego poprawek — to jedyna wada w projekcie, która sama się pogarsza.
2. Stawiamy **obok** starego `venv` drugi, na nowym Pythonie, sprawdzamy go ręcznie na tych
   samych danych i dopiero potem przepinamy trzy linie `crontab` na nowy.
3. Stary `venv` zostaje nietknięty jako droga powrotu: cofnięcie to jedna komenda `crontab`
   z kopii.

## Fakty z 03.10 (odczyt Gracjana na EC2)

| Co | Wynik |
|---|---|
| System | Amazon Linux 2023 (`2023.12.20260817`), wsparcie do 2029-06-30 |
| Python systemowy | 3.9.25 — **zostaje**, używa go sam system (np. `dnf`) |
| Do zainstalowania z `dnf` | `python3.11`, `python3.12`, `python3.13`, `python3.14` (3.14.6) |
| Dysk | 2,8 GB wolne z 8 GB |
| Pamięć | 913 MB, wolne ok. 360 MB; swap 2 GB, zajęte 417 MB |
| Laptop | Python 3.14.2, pandas 3.0.5, `urllib3` 2.7.0 |
| EC2 dziś | Python 3.9.25, pandas 2.3.3, `urllib3` 1.26.20 |

Pythona 3.10 w Amazon Linux 2023 **nie ma** — stąd wybór między 3.11 a 3.14.

## Przykład na innych danych: nowy piekarnik w cukierni

Cukiernia piecze codziennie o 18:00 według planu na drzwiach: „piekarnik A, sernik”.
Piekarnik A jest stary, producent przestał wysyłać części.

1. Stawiamy piekarnik B **obok** A. A dalej piecze według planu.
2. Rano pieczemy ten sam sernik w A i w B i porównujemy.

   | Piekarnik | Wejście | Wyjście (waga) |
   |---|---|---|
   | A | ten sam przepis, te same składniki | 812 g |
   | B | ten sam przepis, te same składniki | 812 g |

3. Zgodne → na drzwiach zmieniamy „piekarnik A” na „piekarnik B”. Wieczorem piecze B.
4. A stoi podłączony jeszcze dwa tygodnie. Gdyby B zawiódł — z powrotem kartka „A”.

| Przykład | Projekt |
|---|---|
| piekarnik A | `~/GPW---pulse/venv` (Python 3.9) |
| piekarnik B | nowy `venv` na nowym Pythonie |
| sernik z rana w obu | ręczny bieg `silver.py` + `gold.py` (bez `GOLD_DO_S3`, więc bez S3) w obu i porównanie plików |
| kartka na drzwiach | trzy linie w `crontab` z pełną ścieżką do Pythona |
| powrót do kartki „A” | `crontab ~/crontab-kopia-…txt` |

## Co może pójść źle

- **Instalacja paczek zabraknie pamięci** (360 MB wolne): instalować tylko gotowe paczki
  (`--only-binary`), bez kompilacji. Jeśli padnie — stary `venv` nietknięty, nic się nie dzieje.
- **Ruszony Python systemowy** (np. podmiana `python3`) psuje `dnf`: nowy Python tylko jako
  `python3.X`, nigdy w miejsce `python3`.
- **pandas 3 liczy inaczej niż pandas 2.3** → inny `gold/`. Poszlaka, że nie: laptop (pandas 3)
  do 20.09 dawał plik tej samej wielkości co EC2 (po odjęciu końców linii). Rozmiar to nie
  treść — dlatego porównanie plików przed przepięciem.
- **Literówka w `crontab`** → stoją wszystkie biegi: kopia przed zmianą, `diff` = dokładnie
  3 linie, stróż złapie ciszę o 19:00.
- **Kafka (`kafka-python`) na nowym Pythonie** — na EC2 niesprawdzone przed pierwszym biegiem
  `cron`. Danych to nie zgubi: Producent zapisuje pamięć po potwierdzeniu brokera, Konsument
  przesuwa zakładkę po zapisie do S3. Najgorzej: dzień później, po powrocie do starego `venv`.
- **Zmiana w trakcie okna 17:55–18:35** — nie robić.
- **Blok w logu zmieni długość** (znikną ostrzeżenia `boto3`, błąd Atheny w 1 linii zamiast 3):
  nowe liczby policzone w krokach, przed pierwszym biegiem.
- **Za miesiąc:** dwa `venv` na dysku (ok. 0,4 GB więcej); stary skasować po dwóch tygodniach
  spokoju (osobna decyzja). Notatki i CLAUDE.md mówią „3.9” — poprawić w dniu przepięcia.
- **25.10 zmiana czasu** — nie łączyć z przepięciem w jednym tygodniu, żeby przy rozjeździe
  było wiadomo, co go spowodowało.

## Jak sprawdzimy

Przed przepięciem: import wszystkich paczek, `pip freeze` = plik `requirements-ec2.txt`
(pusty `diff`), te same pliki `silver/` i `gold/` z obu `venv`, ręczny `control.py` daje `OK`.
Po przepięciu: pierwszy bieg `cron` w **dzień giełdowy**, blok policzony przed biegiem,
stróż `OK`, a wieczorem pełna codzienna kontrola.

## Decyzje do podjęcia (rekomendacja Claude'a pierwsza)

1. **Wersja:** (a) **3.14** — ta sama co laptop, więc test na laptopie mówi to samo co EC2
   (lekcja z 26.09: inny pandas dał inny tekst błędu); poprawki do ok. 2030 *(z pamięci, nie
   sprawdzone)*; (b) 3.12 — ostrożniej, ale trzecie zestawienie wersji, którego nikt nie
   sprawdzał; (c) 3.11 — poprawki do ok. 2027, czyli ten sam problem za rok.
2. **Gdzie nowy `venv`:** (a) **`~/GPW---pulse/venv314`** + wpis w `.gitignore`; (b) poza repo,
   `~/venv314` — bez zmiany `.gitignore`, ale inna ścieżka niż wszędzie w notatkach.
3. **Wersje paczek:** (a) **nowy `requirements-ec2.txt` przygotowany na laptopie** z wersjami
   z laptopa, w gicie, na EC2 instalowany z pliku; (b) instalacja na EC2 „najnowszych” i spisanie
   po fakcie.
4. **Sprawdzenie przed przepięciem:** (a) **ręczny Silver+Gold w obu `venv` i porównanie
   plików**; (b) tylko import paczek.
5. **Dzień przepięcia:** (a) **rano w dzień giełdowy**, nie w tygodniu 25.10; (b) weekend —
   pierwszy bieg bez nowych świec sprawdza mniej.
6. **Stary `venv`:** (a) **zostaje dwa tygodnie**, potem osobna decyzja o skasowaniu;
   (b) kasować od razu po pierwszym udanym biegu.

## Decyzje Gracjana 03.10

1. Wersja **3.14**. 2. **`~/GPW---pulse/venv314`** + `.gitignore`. 3. **`requirements-ec2.txt`
z laptopa**, w gicie. 4. **Silver+Gold w obu `venv` i porównanie plików.** 6. **Stary `venv`
zostaje dwa tygodnie.**

5. **Przepięcie dziś, w sobotę 03.10, przed 17:55** — wbrew rekomendacji „dzień giełdowy”.
Skutki i jak je łagodzimy:
- dzisiejszy bieg nie wyśle ani nie odbierze żadnej wiadomości, więc droga Kafka → S3 na
  nowym Pythonie (Konsument z zapisem do S3) pierwszy raz naprawdę w **poniedziałek 05.10**;
  dziś sprawdzimy tylko połączenie z brokerem (ręczny bieg Producenta i Konsumenta, 0 wiadomości);
- dzisiejszy bieg jest pierwszym i na nowym `bronze` (kompakcja rano), i na nowym Pythonie.
  Żeby rozdzielić przyczyny: **przed** przepięciem ręczny Silver na starym `venv` czyta już nowy
  `bronze` — `(2355, 3)` tam to dowód kompakcji niezależny od Pythona.

## Wyniki 03.10 (wszystko przewidziane przed komendami)

- **Laptop:** `requirements-ec2.txt` z 5 paczek przez `-c requirements-lokalny.txt` — 18 linii,
  bez `pytz` i bez `pyarrow`; commit `4aca12d` (`128/14` zamiast przewidzianych `127/13` —
  edytor dopisał brakujący koniec ostatniej linii `.gitignore`), wypchnięty.
- **EC2, instalacja (09:2x–09:35 UTC):** `pull` `fc6e262..4aca12d` (7 plików, 376/76);
  `dnf install python3.14` (4 paczki, 47 MB); `python3.14` 3.14.6, `python3` dalej 3.9.25;
  `venv314` z 18 gotowymi paczkami (`manylinux`, bez kompilacji), `diff` z `pip freeze` pusty,
  import `3.0.5 1.43.75`, `git status` pusty, `venv314` 205 MB (przewidziane 250–450 — pudło),
  wolne 2,5 GB. `dnf` ostrzega o nowszym Amazon Linux (2023.12.20260930) — osobna sprawa.
- **Porównanie:** Silver na starym `venv` `(2355, 3)` — dowód kompakcji niezależny od Pythona;
  Gold w obu `117` / `111`; **3 × `diff -q` puste — pliki z 3.9/pandas 2.3.3 i 3.14/pandas 3.0.5
  identyczne co do bajtu.** Pomyłka: przewidziane 2 linie `boto3` w ręcznym Goldzie — ostrzeżenie
  wychodzi przy tworzeniu klienta S3 (`GOLD_DO_S3=1`), nie przy imporcie.
- **Ręczne biegi na `venv314`:** `control.py` (02.10) → `Dane 2355`, `OK`; Producent 3 × `nowych
  dni: 0 … zapisane`; Konsument `Odebrano 0`; zakładka `2384 2384 0`; log 1027 nietknięty.
- **`crontab`:** kopia `~/crontab-kopia-1003.txt`, nowy `~/crontab-nowy-1003.txt` (oba `chmod 600`,
  7 linii), `diff` `5,7c5,7`, stary Python 0 razy, wgrany, `RELOAD` **09:45:01 UTC** (11:45 polskiego).
  Powrót: `crontab ~/crontab-kopia-1003.txt`.

**Jeszcze nie „zrobione”:** (b)/(d) pierwszy bieg `cron` dziś wieczorem (start 1028, blok 28,
`wc -l` 1055, `Dane 2355`, stróż #17) i **pierwszy dzień giełdowy pon. 05.10** (start 1056,
`wc -l` 1083, `Odebrano 3`, `Dane 2358`) — dopiero on sprawdzi wysyłkę przez Kafkę i zapis
Konsumenta do S3 na 3.14. Stary `venv` do skasowania najwcześniej ok. 17.10.
