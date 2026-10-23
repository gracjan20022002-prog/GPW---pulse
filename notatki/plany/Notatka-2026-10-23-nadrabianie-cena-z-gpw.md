# Notatka projektowa: nadrabianie wstrzymanych dni ceną z archiwum GPW (23.10.2026)

> **Status (23.10.2026, wieczorem): temat odłożony — decyzja Gracjana.** Tryb `NADROB=gpw` nie powstaje.
> Zostaje wstrzymanie z alarmem i `NADROB=1` po porównaniu cen z dopisku z archiwum GPW; jeśli się nie
> zgadzają — czekanie na poprawkę Yahoo. Powód: zdarzenie od 12.09 nie wystąpiło, złe ceny wcześniejszych
> dni to jeden epizod (05–13.10), od 14.10 Yahoo zgadza się z GPW, a tryb kosztowałby dwie funkcje,
> 15 testów i nowy plik na EC2. Zostaje zasada na czas luki (do CLAUDE.md). Instrukcja
> `Notatka-2026-10-23-jak-napisac-nadrabianie-z-gpw.md` zostaje jako gotowiec, gdyby temat wrócił.

*Notatka przed kodem (zasada 10), z decyzji 1 i 2 przeglądu z 23.10. **Zatwierdzona przez Gracjana
23.10 ze wszystkimi rekomendacjami D1–D6 (wariant a).** Numery linii i komendy pojawią się dopiero
w krokach (notatka-instrukcja, zasada 3).*

## Sedno w trzech zdaniach

1. Od 20.10 dzień, który nie przyszedł o 18:00, jest wstrzymany, a dziś jedyna droga, żeby go wysłać,
   to `NADROB=1` z ceną z Yahoo — tą samą, która bywa zła tygodniami.
2. Nowy tryb `NADROB=gpw` wyśle wstrzymane dni z cenami, które przepiszesz ręcznie z archiwum GPW do
   małego pliku na EC2; dzień bez ceny w pliku zostaje wstrzymany, a plik z literówką zatrzymuje bieg,
   zanim cokolwiek pójdzie do Kafki.
3. Linia wyniku pokaże, co poszło (daty i ceny), więc luka zamyka się tego samego wieczoru, w którym
   ktoś sprawdzi GPW, i widać to w logu.

## Przykład na innych danych: stacja pogodowa

Stacja ma dwa wstrzymane dni pomiaru w Krakowie (20 i 21.10). Czujnik podaje za nie wartości, którym
nie ufamy. Operator przepisuje z archiwum IMGW to, co zna, do pliku:

**Wejście — plik:**
```
# data stacja temperatura (z archiwum IMGW)
2026-10-21 KRK 12,1
2026-10-19 KRK 9,0
2026-10-21 GDA 8,7
```

**Wejście — stan programu:** wstrzymane KRK: 20.10 i 21.10; czujnik: 20.10 → 10,4, 21.10 → 11,0.

**Wyjście (uruchomione 23.10):**
```
KRK: nadrobione z IMGW: 1 (2026-10-21 12.1), wstrzymane: 1 (2026-10-20), z pliku pominięte: 1 (2026-10-19 — nie był wstrzymany)
```

21.10 poszedł z wartością z pliku, 20.10 został wstrzymany (brak w pliku), 19.10 pominięty, bo nie
był wstrzymany (mógł już pójść wcześniej — wysłanie go drugi raz dałoby dwie wartości jednego dnia).
Przecinek w `12,1` przyjęty jak kropka.

**Wyjście przy literówce** (`121` zamiast `12,1`), uruchomione 23.10, kod wyjścia 1, nic nie wysłane:
```
KRK 2026-10-21: 121.0 różni się od czujnika (11.0) o ponad 25%
```

| Przykład | Projekt |
|---|---|
| plik operatora | `companies/ceny_gpw.txt` na EC2 (poza gitem, jak pamięć Producenta) |
| linia `2026-10-21 KRK 12,1` | `2026-10-21 CBF.WA 193,90` (zamknięcie z archiwum GPW, szósta kolumna) |
| wstrzymane dni stacji | wstrzymane dni spółki (`podziel_daty`, gdy dzień nie jest dzisiejszy) |
| wartość z czujnika | cena z odpowiedzi Yahoo za ten dzień |
| próg 25% | ten sam próg: chroni przed literówką, nie przed złą ceną Yahoo |
| `nadrobione z IMGW: …` | dopisek `nadrobione z GPW: N (data cena, …)` w linii wyniku spółki |
| `wstrzymane: …` dla dnia bez wpisu | ten sam dopisek co dziś → kontrola daje `AWARIA` do skutku |

## Jak to wpina się w Producenta (bez numerów linii)

- `NADROB` dostaje trzecią wartość: brak = zwykły bieg; `1` = jak dziś, wszystkie wstrzymane dni z cenami
  Yahoo (dla nowej spółki i starej historii, po sprawdzeniu, że Yahoo zgadza się z GPW); `gpw` = nowy
  tryb z tej notatki.
- W trybie `gpw` Producent na starcie czyta `companies/ceny_gpw.txt`. Zły wiersz albo brak pliku =
  komunikat i koniec, zanim połączy się z Yahoo.
- Dla każdej spółki: dzisiejsza świeca idzie jak zawsze (cena Yahoo); każdy wstrzymany dzień, który ma
  wpis w pliku, idzie z ceną z pliku; wstrzymany dzień bez wpisu zostaje wstrzymany (nie idzie ani do
  Kafki, ani do pamięci).
- Pamięć zapisuje się jak dziś, tylko po potwierdzeniu brokera; wysłany dzień trafia do pamięci, więc
  następnego wieczoru nie jest już „nowy”. (Następny bieg nadpisze w pamięci jego cenę ceną Yahoo — to
  bez znaczenia, bo pamięć mówi tylko, które dni poszły.)
- Linia wyniku: w trybach `1` i `gpw` dopisek z wysłanymi zaległymi dniami i cenami (do 5 ostatnich,
  jak przy wstrzymanych) — to decyzja 2 z przeglądu.
- Wiadomość w Kafce taka sama jak dziś, więc Konsument, Silver, Gold i kontrola się nie zmieniają.
  W S3 cena z GPW (np. `193.9`) zamiast liczby Yahoo z szumem.
- Odczyt pliku i wybór dni jako małe funkcje w `kod/session.py`, z testami bez Kafki i Yahoo, jak
  `podziel_daty`. W `data_ingestion.py` tylko wywołanie i wysyłka.

## Co może pójść źle i co wtedy

- **Literówka w cenie** (`1939`, `19,39`) — próg 25% wobec ceny Yahoo z tego dnia zatrzymuje bieg przed
  wysyłką. Literówki mniejszej niż 25% próg nie złapie — dlatego linia wyniku pokazuje wysłaną cenę.
- **Przecinek zamiast kropki** (archiwum GPW pisze `193,90`) — przyjmowane oba.
- **Zły symbol** (`CBF` zamiast `CBF.WA`) albo **zły wiersz archiwum** (CBF to `CYBERFLKS`, SNT to
  `SYNEKTIK`) — wpis dla nieznanej spółki zatrzymuje bieg; zły wiersz archiwum zwykle łapie próg.
- **Data, która nie jest wstrzymana** (już wysłana albo dzień bez sesji) — pomijana i wypisana, nigdy
  nie wysłana drugi raz.
- **Wpis w pliku zostanie na EC2** — przy następnym `NADROB=gpw` dni już wysłane są pomijane, więc bez
  szkody; plik zostaje jako ślad, co wpisano.
- **Broker nie odpowiada w czasie nadrabiania** — pamięć nietknięta, dni dalej wstrzymane, można powtórzyć.
- **Bieg w oknie 17:55–18:35** — zasada jak dziś: nadrabianie nigdy w tym oknie (najlepiej po 18:50,
  gdy archiwum GPW ma dzień, albo rano).
- **`NADROB=gpw` w `crontab`** — nigdy; zmienna tylko przed ręczną komendą, jak `NADROB=1`.
- **Część spółek ma lukę, część nie** — każda spółka liczona osobno.
- **Przy nadrobionym dniu Gold liczy po luce zmianę dwudniową** (przegląd, 1.1 punkt 3) — po nadrobieniu
  i następnym biegu Gold przelicza wszystko od nowa, więc znika samo.

## Jak sprawdzimy

- Testy funkcji odczytu i wyboru (na zmyślonych danych, wynik przewidziany przed uruchomieniem): plik
  poprawny, przecinek, komentarz i pusta linia, zły wiersz, nieznana spółka, dzień niewstrzymany, dzień
  bez wpisu, literówka ponad progiem.
- Bieg Producenta na laptopie z udawanym Yahoo i Kafką, jak 16.10 (kopia, bez EC2).
- Na EC2 pierwszy bieg zwykłego `cron` po wdrożeniu: blok 28 linii jak dziś (nowy kod nie zmienia
  zwykłego biegu).
- Pierwsze prawdziwe nadrabianie na EC2: liczby przed (dopisek z wczoraj, ceny z GPW), po (linia wyniku
  z cenami, `Odebrano` następnego wieczoru, cena w Athenie co do grosza z GPW, kontrola `OK`, stróż `UP`).

## Zasada na czas luki (z decyzji 1)

Od pierwszego maila `DOWN` aż do `UP`: codziennie kontrola po 18:32, kroki 7 i 8 (ostatni blok i `grep`
błędów), bo stróż nie przyśle drugiego maila (sprawdzone 23.10). Do dopisania w CLAUDE.md przy kontroli.

## Co to zmieni za miesiąc

Nic w zwykłych biegach. README: opis nadrabiania (dwa tryby) i poprawione zdania o samonaprawie.
Strona (notatka z 23.10) dostanie po nadrobieniu ceny z GPW, więc zgodne z archiwum co do grosza.

## Decyzje do podjęcia (rekomendacja pierwsza)

- **D1. Jak włączyć:** (a) nowa wartość `NADROB=gpw`, a `NADROB=1` bez zmian · (b) plik nadpisuje Yahoo
  przy `NADROB=1`, dni bez wpisu idą z ceną Yahoo — łatwo zapomnieć o wpisie i wysłać złą cenę ·
  (c) plik używany zawsze, gdy istnieje.
- **D2. Format pliku:** (a) `data spółka cena`, rozdzielone spacją, cena z przecinkiem albo kropką,
  linie z `#` i puste pomijane · (b) CSV z nagłówkiem.
- **D3. Sprawdzenie ceny:** (a) cena większa od zera i najwyżej 25% różnicy od ceny Yahoo z tego dnia,
  inaczej bieg staje przed wysyłką · (b) bez progu, tylko wypisanie obu cen.
- **D4. Po nadrabianiu:** (a) tylko ręczny Producent; Konsument, Silver, Gold i kontrola same
  w najbliższym biegu `cron` (stróż `UP` po najbliższej kontroli o 18:30) · (b) od razu ręcznie także
  Konsument, Silver i Gold.
- **D5. Gdzie kod:** (a) odczyt pliku i wybór dni w `kod/session.py` z testami, w `data_ingestion.py`
  wywołanie i wysyłka · (b) wszystko w `data_ingestion.py` (bez testów, jak reszta Producenta).
- **D6. Próba przed pierwszym prawdziwym użyciem:** (a) testy i bieg na laptopie z udawanym Yahoo
  i Kafką; na EC2 gotowe kroki czekają na pierwszą lukę · (b) próba na EC2 z udawanym „dziś”
  (`PRODUCENT_DATA`) — wysłałaby prawdziwy dzień ręcznie wpisaną ceną.

## Rozważone 23.10: nadrabianie automatyczne

Pytanie Gracjana: czy wstrzymany dzień może następnego wieczoru pójść sam, „jakby był dzisiejszy”.
Nie wprost — następnego wieczoru ten dzień nie jest już ostatnią świecą u Yahoo, więc jego cena
w odpowiedzi bywa zła (to błąd, przed którym chroni naprawa 1). Da się natomiast złapać cenę, póki dzień
jest dzisiejszy:
- **A. zapas ceny:** przy awarii brokera Producent zapisuje datę i cenę złapane o 18:00, następnego
  wieczoru wysyła dzień z tą ceną. Pokrywa awarie Kafki; nowy plik stanu na EC2.
- **B. drugi bieg tego samego wieczoru** (np. 19:00): pokrywa spóźnione Yahoo; zmiana w `crontab`
  i w kontroli (nowy blok w logu, ponowny Silver i Gold).
- EC2 lub `cron` nie ruszył, Yahoo nie odpowiadało cały wieczór — tylko ręcznie, `NADROB=gpw`.

**Decyzja Gracjana 23.10 (wariant 1):** jutro (24.10) tylko `NADROB=gpw` z tej notatki; B później,
osobną notatką projektową; A odłożone.

## Kolejność pracy po zatwierdzeniu

1. Notatka-instrukcja (zasada 3): co robi każda nowa funkcja, przykład uruchomiony, nowe pojęcia,
   pułapki, kolejność porcji.
2. Porcja 1: funkcje w `session.py` i testy (piszesz Ty).
3. Porcja 2: wpięcie w `data_ingestion.py`, bieg na laptopie.
4. Porcja 3: wdrożenie na EC2 (`git pull`, zwykły bieg `cron`), README i CLAUDE.md.
