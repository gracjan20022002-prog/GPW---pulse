# Notatka 22.09 — test prawdziwej drogi

**Stan: zatwierdzona 22.09.** To siódma naprawa z kolejki z przeglądu
z 08.09, następna po sprawdzianie punktu 6 (potwierdzonym dziś: `silver/`
i `gold/` odtwarzają się z samego `.gitkeep`). Cztery decyzje niżej —
zatwierdzone: (1) `gold_dane_dzienne`, (2) heurystyka pon–pt, (3) na start
ręcznie z laptopa, potem przeniesienie na EC2, (4) dwa fakty z przeglądu
i zgodność liczby dni między spółkami, od razu. Kod pisze Gracjan.

**23.09: kod napisany i sprawdzony na laptopie.** `kod/path.py` (funkcja
`sprawdz_daty` + część `__main__` z Atheną, data z `DROGA_DATA` albo dziś)
i `kod/test_path.py` (6 testów, `6 passed`). Bieg na prawdziwej tabeli:
`2334`, `Dane: OK`. Alarm na żywych danych przy udawanym dniu: 24.09 → trzy
braki, 22.09 → trzy wpisy z przyszłości. Wszystko zgodne z przewidywaniami
zapisanymi przed biegiem. Otwarte kwestie z „Czego nie sprawdziłem":
- typ kolumny `data` nie ma znaczenia, bo `pd.to_datetime` obsłużył to, co
  oddała Athena;
- zapytanie z laptopa działa (czasu nie mierzyliśmy).

Instrukcja krok po kroku: [[Notatka-2026-09-23-jak-napisac-testy-drogi]].

## Sedno w trzech zdaniach

Dzisiejsze testy w `test_plikow.py` sprawdzają rzeczy obok drogi danych:
`test_dzialania` czyta `companies/*.txt` (to pamięć Producenta, nie źródło),
`test_powtorek` czyta lokalny `silver/clean_data.csv` (od 21.09 to plik
zamrożony na laptopie, bo Harmonogram jest wyłączony). Prawdziwa droga danych
to Athena → Silver → Gold, i nic automatycznie nie sprawdza dwóch konkretnych
rzeczy z przeglądu: że dziś **brakuje** wpisu dla jednej ze spółek, albo że
w danych jest wpis z **przyszłości**. Proponuję test, który łączy się
z Athena tak jak `silver.py`, i pyta o te dwa fakty wprost.

## Przykład na innych danych: zeszyt sprzedaży lodziarni

Lodziarnia sprzedaje trzy smaki. Co wieczór ktoś wpisuje do wspólnego
zeszytu (to jest tabela w Athenie), ile sprzedano każdego smaku. Test
prawdziwej drogi to nie sprawdzanie notatnika sprzedawcy w kieszeni
(to jest `companies/*.txt`) — to zajrzenie do zeszytu i zadanie dwóch pytań.

**Pytanie 1: czy każdy smak ma dziś wpis?**

Zeszyt (dziś jest 2026-09-22):

| smak | data | sprzedano |
|---|---|---|
| wanilia | 2026-09-22 | 41 |
| czekolada | 2026-09-22 | 55 |
| pistacjowy | 2026-09-19 | 12 |

Wynik testu: `BRAK: pistacjowy nie ma wpisu z 2026-09-22 (ostatni: 2026-09-19)`.

**Pytanie 2: czy jest wpis z przyszłości?**

Zeszyt:

| smak | data | sprzedano |
|---|---|---|
| wanilia | 2026-09-22 | 41 |
| czekolada | 2026-09-23 | 12 |

Wynik testu: `BŁĄD: czekolada ma wpis z 2026-09-23, a dziś jest 2026-09-22`.

Oba wyniki to zwykła lista tekstów — dokładnie to, co dziś robi
`sprawdz_blok` w `control.py` (zwraca listę problemów zamiast od razu
wysyłać cokolwiek).

## Przykład → projekt

| Lodziarnia | Projekt |
|---|---|
| trzy smaki | trzy spółki z `config.ticker` |
| wspólny zeszyt | tabela w Athenie (`gold_dane_dzienne` albo `live`) |
| „czy każdy smak ma dziś wpis" | czy każda spółka ma wiersz z dzisiejszą datą |
| „czy jest wpis z przyszłości" | czy `MAX(data)` w tabeli jest później niż dziś |
| sprawdzenie zeszytu wieczorem | uruchomienie testu po biegu `cron` (na razie ręcznie) |
| notatnik sprzedawcy w kieszeni | `companies/*.txt` — to sprawdza dzisiejszy `test_dzialania`, nie jest to zeszyt |

## Stan dziś (sprawdzone 22.09)

- `kod/test_plikow.py` ma dwa testy: `test_dzialania` (parametryzowany po
  `ticker`, czyta `companies/{tick}.txt`, sprawdza format wiersza i próg
  ≥700 wierszy) i `test_powtorek` (czyta lokalny `silver/clean_data.csv`,
  liczy duplikaty `dzien`+`spolka`). Żaden nie łączy się z Athena.
- Jedyne dziś sprawdzenie treści danych w Athenie to ręczny krok 12
  „codziennej kontroli" — zapytanie SQL wklejane w konsoli przeglądarki,
  nieautomatyczne, niepowiązane z sygnałem awarii.
- Sygnał awarii (`control.py`) świadomie tego nie łapie — czyta tylko tekst
  `errors.txt`, nie zagląda do danych. To udokumentowane ograniczenie
  z 21.09, nie coś nowego.
- Wzorzec już zatwierdzony i działający: `sprawdz_blok(blok, spolki, dzis)`
  w `control.py` — czysta funkcja, dostaje dane, zwraca listę problemów;
  osobno testowana (`test_control.py`, 11 testów na prawdziwym bloku z
  18.09), osobno wywoływana z prawdziwym światem (zgłoszenie do stróża).
- Dzisiejszy sprawdzian pokazał `gold_dane_dzienne`: 777 wierszy = 777 dni
  na każdą z trzech spółek, `MAX(data)` = 2026-09-22 dla wszystkich —
  czyli gdyby taki test istniał dziś, przeszedłby czysto. Dobry dzień na
  pierwsze uruchomienie, gdy kod powstanie.

## Kształt, jaki proponuję (wzorem `control.py`)

Dwie warstwy, nie jedna:

1. **Czysta funkcja** — dostaje gotową tabelę (DataFrame z kolumnami
   `spolka`, `data`) i listę spółek, zwraca listę tekstów-problemów.
   Zero połączenia z siecią — dzięki temu testowalna na zmyślonych danych,
   jak w przykładzie z lodziarnią wyżej. Sprawdza trzy rzeczy (zatwierdzone
   w decyzjach niżej):
   - dzisiejsza data obecna dla każdej spółki — **tylko gdy dziś to
     poniedziałek–piątek** (heurystyka z decyzji 2);
   - brak wiersza z datą późniejszą niż dziś — sprawdzane zawsze, niezależnie
     od dnia tygodnia;
   - ta sama liczba dni (`COUNT(DISTINCT data)`) dla wszystkich trzech
     spółek — sprawdzane zawsze, to nie zależy od tego, czy dziś jest sesja.
2. **Cienka warstwa** — łączy się z Athena (`pyathena`, jak w `silver.py`),
   pobiera tabelę, woła funkcję z (1), wypisuje wynik.

## Co może pójść źle

- **Weekend i święto.** W dzień bez sesji żadna spółka nie ma dzisiejszego
  wpisu — test naiwnie krzyczałby „brak" codziennie, nie tylko w dni
  giełdowe. Test nie ma skąd wiedzieć, czy dziś jest sesja.
- **Athena w trakcie pracy.** 04.09 zwróciła 405 zamiast 2283 wierszy bez
  żadnego błędu (crawler akurat pracował). Test złapałby to jako „brakuje
  wszystkich spółek" — głośno, ale z mylącym powodem.
- **Uruchomienie za wcześnie.** Przed 18:10 dane z dzisiaj jeszcze nie
  doszły — test zawsze pokaże „brak", niezależnie od tego, czy coś jest
  nie tak. Ta sama pułapka co przy ręcznej kontroli.
- **Nowa spółka pierwszego dnia** — nie dotyczy dziś (trzy stałe spółki),
  ale gdyby doszła czwarta, jej historia zaczyna się od zera; test o to
  akurat nie pyta (pyta tylko o dziś), więc nie jest to realne ryzyko.
- Koszt zapytań Athena rośnie z liczbą uruchomień — dziś nieistotne
  (pojedyncze zapytanie dziennie), do pamięci, gdyby ktoś chciał podpiąć
  to częściej.

## Decyzje — Twoje

1. **Którą tabelę pytać.** (a) `gold_dane_dzienne` — to koniec całej drogi
   (Athena → Silver → Gold), jedno miejsce sprawdza wszystko po drodze —
   **rekomendacja**. (b) `live` — bliżej surowego wejścia, bliżej dosłownego
   brzmienia z przeglądu („w `live` jest dzień z przyszłości"), ale nie
   sprawdza, czy Silver/Gold czegoś nie popsuły po drodze.
   **Wybrano: (a) `gold_dane_dzienne`.**
2. **Skąd wiedzieć, że dziś jest dzień giełdowy** (żeby nie fałszywie
   krzyczeć w weekend). (a) nie zgadywać wcale — test tylko donosi fakt
   („dziś brakuje X"), a Ty go uruchamiasz i oceniasz, wiedząc, jaki to
   dzień — **rekomendacja na start**, bo nic nie zgaduje i jest prosta.
   (b) heurystyka pon–pt bez świąt — będzie fałszywie alarmować w święta
   (Wielkanoc, święta państwowe). (c) lista sesyjnych dni GPW do
   utrzymania — dokładne, ale kolejna rzecz do aktualizowania co roku.

   **Wybrano: (b) heurystyka pon–pt.** Ocena pracochłonności: sama
   heurystyka to jedna linia (`data.weekday() < 5` — Python liczy
   poniedziałek jako 0, niedzielę jako 6), plus parę testów na zmyślonych
   datach (piątek, sobota, niedziela, poniedziałek) wzorem tych z
   lodziarnią wyżej. Razem z grubsza **20–30 minut** — wzorzec (funkcja +
   testy na sztucznych danych) już znasz z `control.py`, więc to
   powtórzenie, nie nowa umiejętność. Zdecydowanie mniej niż opcja (c):
   lista świąt wymaga albo nowej zależności (biblioteki do świąt), albo
   ręcznego liczenia świąt ruchomych (Wielkanoc, Boże Ciało zależą od daty
   Wielkanocy) — to osobne, większe zadanie, nie coś na pół godziny. Koszt
   wybranej opcji: kilkanaście razy w roku (święta państwowe w dni robocze,
   plus 24.12 i 31.12, które GPW też ma wolne) test fałszywie powie „brak
   dzisiejszej daty" — to świadomie przyjęty szum, nie usterka; oceniasz go
   Ty, czytając wynik, tak jak dziś oceniasz ręcznie w kroku 7 kontroli.
3. **Gdzie na razie uruchamiać.** (a) ręcznie, z laptopa, osobnym małym
   skryptem/testem — **rekomendacja**, bo oddziela „napisanie testu" od
   „wpięcie w automat" na EC2. (b) od razu dopisane do `control.py`
   na EC2, jako część sygnału awarii — większy krok, łączy dwie osobne
   sprawy z listy napraw.
   **Wybrano: (a) na start ręcznie z laptopa. (b) później, osobną decyzją,
   gdy test się oswoi.**
4. **Co dokładnie zgłasza.** (a) tylko dwa fakty z przeglądu — brakująca
   dzisiejsza data dla którejś spółki i jakakolwiek data z przyszłości —
   **rekomendacja**, trzyma się dokładnie wady 2.9 z przeglądu.
   (b) też zgodność liczby dni między trzema spółkami — to już sprawdzamy
   ręcznie w kroku 12 kontroli; można dodać później, osobną decyzją.
   **Wybrano: oba, od razu — (a) i (b) razem, bez odkładania.**

## Jak sprawdzimy

Przewidywania w wiadomości przed każdą komendą (kroki po zatwierdzeniu).
Test samej funkcji (warstwa 1) na zmyślonych danych jak w przykładzie
z lodziarnią wyżej, po jednym przypadku na każdą z trzech rzeczy, które
sprawdza (brak dzisiejszej daty, data z przyszłości, różna liczba dni
między spółkami), plus dwa przypadki na heurystykę dnia tygodnia (dziś to
wtorek → sprawdzać brak; dziś to sobota → nie sprawdzać braku), plus jeden
przypadek bez żadnego problemu (ma zwrócić pustą listę). Test warstwy 2
(połączenie z Athena) na dzisiejszych, prawdziwych danych — ma wypisać
„brak problemów", bo sprawdzian z dzisiaj pokazał komplet (777/777/777,
wszystkie `do` = 2026-09-22, ta sama liczba dni na wszystkich trzech).

## Co to zepsuje za miesiąc

- Zmiana nazw kolumn w `gold_dane_dzienne` (znany rozjazd z 17.09 między
  nagłówkiem CSV a tabelą) wymagałaby dopasowania zapytania testu.
- Jeśli kiedyś test trafi do `cron` na EC2, dochodzi do listy rzeczy
  zależnych od roli IAM (już ma dostęp do Athena od 03.09) i do kosztu
  Athena liczonego per uruchomienie zamiast raz dziennie.
- Lista trzech spółek w `config.ticker` i tak jest już wspólna dla tego
  testu i dla `test_dzialania` — nowa spółka obejmie oba automatycznie.

## Czego nie sprawdziłem

- Dokładny typ kolumny `data` w `gold_dane_dzienne` w Athenie (czy string,
  czy timestamp) — wpłynie na dokładne porównanie z dzisiejszą datą.
- Czy istnieje gdziekolwiek w projekcie lista dni sesyjnych GPW — nie
  przeszukałem całego repo, tylko `notatki/` i `kod/test_plikow.py`.
- Czas i koszt pojedynczego zapytania do `gold_dane_dzienne` z laptopa
  (widzieliśmy dotąd zapytania tylko z poziomu EC2, w logach `silver.py`).

## Powiązane notatki

- [[Przeglad-2026-09-08-co-nie-gra]] — sekcja 2.9, źródło wady; kolejność
  napraw, punkt 7
- [[Notatka-2026-09-18-sygnal-awarii]] — wzorzec „funkcja zwraca listę
  problemów", `control.py`/`test_control.py`
- [[Notatka-2026-09-21-jedno-miejsce-liczenia]] — dlaczego lokalny
  `silver/clean_data.csv` już nie nadaje się jako źródło dla testów
