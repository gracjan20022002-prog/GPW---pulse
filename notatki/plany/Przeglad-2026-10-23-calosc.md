# Przegląd całości 23.10.2026 — po naprawach 1 i 2

Data: 2026-10-23 (piątek), ok. 17:05–17:10 (godziny z laptopa). Przegląd według zasady 16: naprawy 1 i 2 z przeglądu
z 08.10 wdrożone na EC2 20.10, a przeglądu po nich nie było. Decyzja Gracjana 23.10 (D6 w notatce
o danych na stronę): przegląd przed kodem skryptu, który da dane stronie.

## Sedno

Łańcuch danych chodzi bez awarii: każdy bieg od 10.10 zgodny z przewidywaniem co do liczby, 117 cen
w S3 zgodnych z archiwum GPW. W kodzie nie znalazłem nic, co dziś psuje dane. Nowa wada jest
w zachowaniu po naprawie 1: **dzień, który nie przyszedł o 18:00 (awaria biegu albo spóźnione
Yahoo), nie wraca już sam następnego wieczoru**, a README nadal tak obiecuje w dwóch miejscach.
Taki dzień czeka na ręczne nadrobienie, które ma sens dopiero wtedy, gdy Yahoo poda za niego dobrą
cenę. Dla CBF i SNT za 05–06.10 nie podało jej od 16–17 dni. Do tego stróż wysyła mail tylko przy zmianie
stanu, więc po pierwszym mailu taka luka może trwać po cichu i zasłonić następną awarię.

## Stan punktów

| Punkt | Stan |
|---|---|
| 1.1 luka po wstrzymaniu dnia | **decyzja 1 zmieniona 23.10 wieczorem na (b):** tryb `NADROB=gpw` odłożony (notatka i instrukcja zostają jako gotowiec); zostaje wstrzymanie z alarmem, `NADROB=1` po porównaniu z GPW, zasada na czas luki w CLAUDE.md i opis w README. Drugi bieg wieczorem (B) później osobną notatką, zapas ceny (A) odłożony |
| 1.2 nadrabianie wysyła cenę z chwili biegu i jej nie wypisuje | odłożone razem z 1.1 (opcjonalnie później, kilka linii); do tego czasu po `NADROB=1` sprawdzić wysłane ceny w Athenie |
| 1.5 `PRODUCENT_DATA` z datą wstrzymaną wysyła ten dzień z ceną Yahoo | nowe 23.10 wieczorem, opis w 1.5. **Decyzja Gracjana (a): zasada w CLAUDE.md i README — `PRODUCENT_DATA` tylko do testów, nigdy z datą wstrzymaną**; bez zmiany kodu; wpis przy dokumentacji 23.10 |
| 1.3 `NADROB=1` i `/fail` z dopiskiem nigdy nie chodziły na EC2 | decyzja 3 (a). **`/fail` ✅ 23.10 o 17:25** (EC2 15:24 UTC): ręczny `control.py` na bloku z dopiskiem, dwa razy → 2 × `Kontrola: AWARIA - CBF.WA: wstrzymane dni`, u stróża #39 i #40 `Failure`, `POST`, treść 370 B (364 znaki, w UTF-8 co do bajtu); **w dzienniku stróża jedna zmiana stanu `up → down`, po #40 żadnej** — potwierdza 1.1 punkt 2 (mail tylko przy zmianie stanu). Podgląd treści u stróża: polskie litery poprawne (zamyka sprawę #21). **Na Interii jeden mail `DOWN` po 17:25** — drugi `/fail` maila nie dał (potwierdzone). `NADROB=1` na EC2 dalej niesprawdzone |
| 1.4 drobne | bez decyzji, opis niżej |
| Część 3, dokumentacja | ✅ **23.10, koniec sesji:** README (dwa zdania o samonaprawie, stan i liczby 23.10, 120 cen, tabela skryptów, luka i `PRODUCENT_DATA`, mail przy zmianie stanu), CLAUDE.md (stan 23.10, zasada na czas luki, skutek naprawy 1, stróż, przewidywania z numerami +2), sprostowanie w notatce z 12.10 |
| Stary `venv` na EC2 (Część 2) | ✅ **skasowany 23.10** razem z `~/porownanie-1003/` (205M + 256K, dysk 72% → 69%) |

## Podstawa

- **Kod, przeczytany w całości 23.10:** 12 plików w `kod/` (`config.py`, `data_ingestion.py`,
  `session.py`, `kafka_consumer.py`, `silver.py`, `gold.py`, `compaction.py`, `control.py`,
  `path.py`, `wykresy.py`, `ranking.py`, `pipeline.bat`), trzy pliki testów (38 testów),
  `.gitignore`, `requirements-ec2.txt`, stan gita.
- **Dokumentacja, przeczytana w całości:** README, CLAUDE.md, przegląd z 08.10; notatka o naprawach
  1 i 2 z 12.10 (możliwości, ryzyka, decyzje).
- **Przeszukane pod kątem otwartych spraw** („niesprawdzone”, „do decyzji”, „do sprawdzenia”,
  „nieodczytany”, „nadrab”, „spóźni”): wpisy dziennika 08–23.10 i notatki z 12, 13 i 17.10.
  **Wpisów dziennika od 08.10 nie czytałem w całości** i nie czytałem od nowa niczego sprzed 08.10
  — zrobiły to przeglądy z 08.09 i 08.10, a ich otwarte punkty są w Części 2.
- Szkic strony (Artifact) przeglądany osobno w ciągu dnia; kodu strony w repozytorium jeszcze nie ma.

**Waga** jak w poprzednich przeglądach: 🔴 kasuje lub fałszuje dane · 🟠 ukryta awaria, nikt się
nie dowie · 🟡 brud, dług, mylące · ⚪ drobiazg.

---

## Część 1 — Nowe wady

### 1.1 🟠 Dzień, który nie przyszedł o 18:00, zostaje luką do ręcznego nadrobienia, a alarm cichnie po pierwszym mailu

**Jak to idzie, dzień po dniu** (prześledzone w `data_ingestion.py:50–93` i `session.py:11–16`):

| Wieczór | Yahoo ma | Producent | Kontrola o 18:30 |
|---|---|---|---|
| D (np. środa), bieg pada albo Yahoo nie ma jeszcze świecy | — | `nowych dni: 0`, pamięć bez D | `AWARIA` (brak wpisu z D) → mail `DOWN` |
| D+1 | D i D+1 | wysyła D+1; D **wstrzymany**, nie idzie do pamięci | `AWARIA` (wstrzymane dni) → bez nowego maila |
| D+2, D+3, … | D, … | D dalej wstrzymany | `AWARIA` codziennie → bez nowego maila |
| po `NADROB=1` | — | wysyła D z ceną z chwili biegu | `OK` → mail `UP` |

Przed 20.10 Producent sam wysyłał D wieczorem D+1. Notatka z 12.10 świadomie to zmieniła: luka zamiast
złej ceny, a nadrabia człowiek po porównaniu z GPW. Przegląd dodaje trzy rzeczy, których notatka nie
miała:

1. **Nadrabiać nie ma czym, dopóki Yahoo nie poprawi ceny.** Człowiek porówna cenę z dopisku
   z archiwum GPW. Jeśli się nie zgadza, `NADROB=1` wyśle złą cenę. Zostaje tylko czekać. Yahoo
   poprawiło 07–13.10 po 4–10 dniach (17.10), XTB 05–06.10 po 15–16 dniach (21.10), a CBF i SNT
   05–06.10 do 22.10 nie poprawiło (16–17 dni). Luka w S3, w Goldzie i na przyszłej stronie może więc trwać tygodniami.
2. **Stróż wysyła mail przy zmianie stanu**, nie przy każdym zgłoszeniu. Tak opisuje go CLAUDE.md przy
   11.11 („mail `DOWN`, 12.11 `UP`”). Po pierwszym `DOWN` kolejne `/fail` nie dają maila. Jeśli w czasie
   luki padnie coś innego (EC2, Kafka, Athena), nikt się nie dowie. Notatka z 12.10 pisze „stróż alarmuje
   codziennie” — według tego, jak działa stróż, to nieprawda. **Sprawdzone 23.10 o 17:25:** dwa `/fail`
   z rzędu dały w dzienniku stróża jedną zmianę stanu (`up → down`) — drugi `/fail` stanu nie zmienił.
3. **Gold po luce liczy zmianę z dwóch dni** jako zmianę dzienną (`gold.py:11`, `pct_change` po
   kolejnych wierszach). To drobny skutek, ale strona pokaże w tym dniu „najlepszy/najgorszy dzień”
   z dwudniowej zmiany.

Od 12.09 żaden bieg nie miał dwóch nowych dni, więc to się jeszcze nie zdarzyło. Wystarczy jeden zły
wieczór: martwy broker, restart EC2, odmowa Yahoo albo świeca po 18:00 (README: zapas najwyżej
kwadrans).

### 1.2 🟡 Nadrabianie wysyła cenę z chwili biegu, a nie tę sprawdzoną, i jej nie wypisuje

`NADROB=1` (`data_ingestion.py:32`, `69`, `76–79`) wysyła ceny z odpowiedzi Yahoo w chwili ręcznego
biegu. Człowiek sprawdzał cenę z dopisku z biegu 18:00, który był wcześniej. Między jednym a drugim
Yahoo może cenę zmienić. Linia wyniku (`88`) podaje tylko liczby (`nowych dni`, `wysłane`), bez dat
i cen. Co naprawdę poszło, widać dopiero w Athenie (`live`) albo w pamięci po biegu.

### 1.3 🟡 Nadrabianie i `/fail` z dopiskiem nigdy nie chodziły na EC2

Wiadomo od 20.10. `NADROB=1` sprawdzono tylko na kopii z udawanym Yahoo i Kafką (16.10). Wysłania
`/fail` z dopiskiem `wstrzymane` nie sprawdzono w ogóle (alarm z `control.py` na EC2 20.10 był bez
stróża). Po 1.1 to ważniejsze, bo pierwsze nadrabianie wypadnie pod alarmem, w dzień awarii.
`/fail` da się sprawdzić bezpiecznie, jak 06.10: ręczny `control.py` z `KONTROLA_LOG` na
przygotowanym bloku. Przy okazji rozstrzygnęłoby to, czy drugi `/fail` z rzędu daje mail (1.1,
punkt 2). Nadrabiania na prawdziwym dniu nie da się sprawdzić bez prawdziwej luki. Wykasowanie dnia
z pamięci po to, żeby wysłać go drugi raz, groziłoby dwiema różnymi cenami tego samego dnia w `live`
(Silver wybiera wtedy przypadkowo).

### 1.5 🟡 `PRODUCENT_DATA` z datą wstrzymaną omija wstrzymanie (dopisane 23.10 wieczorem)

`PRODUCENT_DATA` (`data_ingestion.py:31`) to udawane „dziś”, wprowadzone 13.10 do testu wstrzymania
(ustawione na wczoraj wstrzymuje dzisiejszą świecę). Działa też w drugą stronę: ręczny bieg na EC2
z `PRODUCENT_DATA` równym **dacie wstrzymanej** sprawia, że `podziel_daty` uzna ją za dzisiejszą i wyśle
z ceną Yahoo z chwili biegu — bez `NADROB=1` i bez porównania z GPW. Warunek: świadomy ręczny bieg
z `KAFKA_BOOTSTRAP`. Dziś chroni przed tym tylko zasada „`PRODUCENT_DATA` tylko do testów”.

### 1.4 Drobne

- ⚪ `silver.py:21–22`: oba `assert` nigdy nie zadziałają — pustą cenę usuwa wcześniej linia 14,
  powtórzony dzień linia 17. Przegląd z 08.10 miał tylko linię 22. Działa naprawdę tylko linia 20
  (za dużo albo za mało spółek). Opis „Gdy coś pójdzie źle” na stronie poprawiony 23.10.
- ⚪ `compaction.py:56`: plik `live` z dniami z dwóch miesięcy (np. nadrabianie 2. dnia miesiąca)
  nie zostanie skasowany, a jego stare dni trafią też do `bronze`. Silver odsieje powtórki z tą samą
  ceną, więc bez skutku.
- ⚪ Szkic strony ma ceny od 18.09 przepisane z wcześniejszego szkicu, nie z drogi danych. Rozwiązuje
  to zatwierdzona notatka z 23.10 (`Notatka-2026-10-23-dane-na-strone.md`).
- ⚪ W katalogu głównym leży pusty `Strona - pomysły.txt` poza gitem (co najmniej od 22.10).
- ⚪ CLAUDE.md znów rośnie: 792 linie (10.10 ok. 700), głównie tabela przewidywań i liczby dzienne.

---

## Część 2 — Wady z 08.10 i 08.09: co dalej jest

| Wada | Dziś | Waga dziś |
|---|---|---|
| Złe ceny Yahoo przy nadrabianiu (08.10, 1.1) | ✅ 20.10, naprawa 1; skutek uboczny w 1.1 wyżej | — |
| Zapasowy adres brokera (08.10, 1.1 p. 2) | ✅ 20.10, naprawa 2; Konsument bez zmiennej sprawdzony tylko na laptopie | — |
| Strażnik kompakcji (08.10, 1.2) | ✅ 09.10; pierwsze prawdziwe kasowanie na nowym kodzie na początku listopada | — |
| Git w OneDrive (08.10, 1.3) | zostawione (decyzja 4); 10.10 755 luźnych obiektów | 🟡 |
| Producent poza `session.py` bez testów (08.10, 1.4) | dalej; logiki przybyło (pamięć bez wstrzymanych dni, dopisek), testy ma tylko `podziel_daty` | 🟡 |
| `ValueError` przy złej linii pamięci (08.10, 1.4) | dalej, dziś `data_ingestion.py:42` | ⚪ |
| `path.py:8` zmienia tabelę wywołującego | dalej | ⚪ |
| `athena-results/` rośnie | dalej, rozmiar niesprawdzony | ⚪ |
| `flush()` bez `close()` | dalej, `data_ingestion.py:99` | ⚪ |
| Kwadrans zapasu u Yahoo (08.09, 2.1) | **zmiana 20.10:** spóźniona świeca nie wraca już sama, patrz 1.1 | 🟠 (razem z 1.1) |
| Korekty Yahoo wstecz (08.09, 2.1) | ograniczenie w README; po naprawie 1 dotyczy tylko dni już wysłanych | 🟡 |
| `except` łapie `TypeError`/`KeyError` (08.09, 2.1) | dalej, `data_ingestion.py:96`; głośne | ⚪ |
| Jedno źródło, bez planu B (08.09, 2.1) | ograniczenie w README; po 1.1 ważniejsze | 🟡 |
| Retencja Kafki 7–14 dni (08.09, 2.2) | bez zmian | 🟡 |
| `t3.micro` bez zapasu (08.09, 2.2) | bez zmian, bez kłopotu | 🟡 |
| Pole `spółka` dubluje partycję w `live` (08.09, 2.3) | dalej | 🟡 |
| `close()` bez `finally` (08.09, 2.3) | ograniczenie w README | ⚪ |
| Nowa spółka niewidoczna w Athenie (08.09, 2.4) | ograniczenie w README; po naprawie 1 nowa spółka wymaga też `NADROB=1` | 🟠 przy 4. spółce |
| `AWSGlueConsoleFullAccess` | osobna decyzja | ⚪ |
| Przypadkowy wybór ceny w Silverze (08.09, 2.5) | dalej; po naprawie 1 dwie różne ceny jednego dnia są mało prawdopodobne | 🟡 (było 🟠) |
| Nierówne okna `range=3y` (08.09, 2.6) | ograniczenie w README | 🟡 przy 4. spółce |
| Ostrzeżenia w logu (08.09, 2.7) | dalej, `pandas` i `value_deserializer` | ⚪ |
| Kompakcja ręczna (08.09, 2.8) | ograniczenie w README | 🟡 |
| Nic nie sprawdza, że kod na EC2 = GitHub (08.09, 2.10) | dalej; `git log -1` przy wdrożeniu | 🟡 |
| Klucz `.pem` w OneDrive (08.09, 2.10) | dalej | ⚪ |
| Power BI na starych plikach | odłożony, dane do 20.09 | 🟡 |
| Stary `venv` na EC2 | termin ok. 17.10 minął, decyzja otwarta | ⚪ |

---

## Część 3 — Dokumentacja niezgodna z dzisiejszym stanem

**README** (numery linii z bieżącego pliku):
- **linie 92–94:** „Gdy broker nie odpowiada, dni polecą przy następnym biegu” — od 20.10 nieprawda,
  następnego wieczoru ten dzień jest wstrzymany (1.1);
- **linie 169–170:** „Gdy Yahoo spóźni się ze świecą, … Producent dociągnie dzień następnego wieczoru”
  — od 20.10 nieprawda (1.1);
- linie 9–12 i 22: stan „10.10”, liczby do 09.10; linia 136 „sprawdzone do 09.10”; linia 140
  „790 dni … 2370 wierszy”, „90 cen”; linia 125 „111 cen … do 20.10” (dziś 117 do 22.10);
- linia 202 (tabela skryptów): Producent bez wstrzymania, `NADROB` i `PRODUCENT_DATA`; linia 203:
  `session.py` bez `podziel_daty`;
- linia 300: przegląd z 08.10 jako źródło prawdy o wadach (do zmiany, jeśli decyzja 5 = a).

**CLAUDE.md:**
- „Wciąż otwarte”, punkt 1: „(e) README 20.10” — README ma dwa zdania sprzeczne z naprawą (wyżej);
- „Ograniczenia opisane w README”: „kwadrans zapasu u Yahoo” — opis w README nieaktualny;
- 792 linie (1.4).

**Notatka z 12.10** (`Notatka-2026-10-12-naprawy-1-i-2.md`, linia 66): „stróż alarmuje codziennie,
dopóki luka jest” — według zasady działania stróża mail przychodzi raz (1.1, punkt 2).

**Przegląd z 08.10:** do oznaczenia jako historia, jeśli decyzja 5 = a.

---

## Część 4 — Jak pracowaliśmy od 08.10 (pomyłki Claude'a, wzór)

Wnioski 13–16 w CLAUDE.md (12, 13, 16 i 20.10) mają wspólny kształt: **opis ogólny zamiast konkretu,
który da się sprawdzić**. Dwa warianty przewidywania z tym samym założeniem. Poprawka wyglądu bez
zobaczenia tego, co widzi Gracjan. Krok opisany słowami zamiast operatorem i wartością. Kroki
z godziną podane przed czasem. Dziś (23.10) ten sam kształt wyszedł przy przeglądzie: notatka
z 12.10 obiecała „alarm codziennie”, nie sprawdziwszy, jak stróż wysyła maile. Przy podglądzie
strony lokalna kopia bez `viewport` pokazała telefon na 980 px. Rozjazd z liczbą wyszedł od razu,
zanim zdążył cokolwiek popsuć.

---

## Część 5 — Niesprawdzone i terminy

**Niesprawdzone:** `NADROB=1` na EC2; `/fail` z dopiskiem `wstrzymane`; dwa `/fail` z rzędu u stróża;
Konsument bez zmiennej na EC2; port 9092 dla laptopa; rozmiar
`athena-results/`; liczba linii przy awarii Atheny na Pythonie 3.14; warunki Yahoo dla publicznej
strony (drugi etap strony); zgłoszenia u stróża #38 (22.10) i #39 (23.10) do odczytu.

**Terminy:** 23.10 po 18:32 kontrola biegu (tabela w CLAUDE.md: start 1588, `wc -l` 1615, `Dane
2400`); 25.10 pierwszy bieg po zmianie czasu (`17:00:0X` w logu); 26.10 pierwszy dzień giełdowy zimą;
01.11 Gold zmienia `117`/`111`; początek listopada kompakcja z prawdziwym kasowaniem na nowym
strażniku; 11.11 fałszywy alarm w święto (pierwszy prawdziwy `DOWN`/`UP` od 06.10); 16, 18 i 20.11
raporty kwartalne; 19.02.2027 koniec darmowego planu AWS. Po terminie: decyzja o starym `venv`
(17.10).

---

## Część 6 — Do decyzji Gracjana

**Decyzja Gracjana 23.10: wszystkie siedem punktów w wariancie (a).** Od dziś ten plik jest źródłem
prawdy o wadach; przegląd z 08.10 to historia.

**Zmiana 23.10 wieczorem (decyzja Gracjana):** punkt 1 → (b) i punkt 2 odłożony (patrz tabela stanu
punktów). Skutek dla punktu 6: skrypt strony (`kod/strona_dane.py`) nie czeka już na 1 i 2 —
instrukcja do niego od 24.10.

Rekomendacja Claude'a pierwsza przy każdym punkcie.

1. **Luka po wstrzymaniu (1.1):**
   - (a) **notatka projektowa „nadrabianie ceną z GPW”:** przy `NADROB=1` Producent bierze cenę
     z małego pliku wpisanego ręcznie z archiwum GPW, a nie z Yahoo. Luka zamyka się tego samego
     wieczoru, w którym ktoś sprawdzi GPW. Do tego jasna zasada na czas luki: codziennie czytać log,
     bo mail nie przyjdzie drugi raz;
   - (b) zostawić kod, opisać w README skutki (luka do poprawki Yahoo, jeden mail) i zasadę czytania
     logu w czasie luki;
   - (c) drugie źródło notowań (możliwość c z 12.10) — najwięcej nowego kodu i nowych awarii.
2. **Wypisywanie wysłanych cen (1.2):**
   - (a) **w trybie `NADROB=1` dopisać do linii wyniku wysłane daty i ceny**, jak przy wstrzymaniu;
     najlepiej w tej samej zmianie co 1(a);
   - (b) sprawdzać po fakcie w Athenie.
3. **Próba `/fail` z dopiskiem na EC2 (1.3):**
   - (a) **w najbliższy dzień z kontrolą, przed 18:00:** ręczny `control.py` z `KONTROLA_LOG` na
     przygotowanym bloku z dopiskiem i ze `STROZ_URL`, dwa razy z rzędu (czy przyjdzie drugi mail),
     potem zwykłe `GET` (`UP`). Przesuwa numery u stróża;
   - (b) czekać na prawdziwy przypadek.
4. **Dokumentacja (Część 3):**
   - (a) **dziś, przy dokumentacji końcowej sesji:** dwa fałszywe zdania w README, stan i liczby,
     tabela skryptów, CLAUDE.md, dopisek w notatce z 12.10;
   - (b) przy następnej dużej dokumentacji.
5. **Źródło prawdy o wadach:**
   - (a) **od dziś ten plik**; przegląd z 08.10 dostaje dopisek „dokument historyczny”;
   - (b) dopisywać do przeglądu z 08.10.
6. **Kolejność:**
   - (a) **4 i 5 dziś; 3 w najbliższy dzień giełdowy; 1 i 2 (notatka projektowa, potem kod) przed
     kodem `kod/strona_dane.py`** — zasada 15, naprawa przed budową. Instrukcja do skryptu strony
     może czekać, a ustalenia strony mogą iść dalej;
   - (b) strona najpierw, a 1 i 2 jako ograniczenia w README do czasu pierwszej luki.
7. **CLAUDE.md (792 linie):**
   - (a) **na koniec każdego miesiąca przenosić przeszłe wiersze przewidywań i liczby dzienne do
     `Historia-stanu.md`**, jak 10.10;
   - (b) zostawić.

---

## Powiązane notatki

- [[Przeglad-2026-10-08-calosc]] — poprzedni przegląd, punkty w Części 2
- [[Notatka-2026-10-12-naprawy-1-i-2]] — decyzja o wstrzymaniu, której skutki opisuje 1.1
- [[Notatka-2026-10-17-porcja-5-wdrozenie]] — wdrożenie napraw i lista niesprawdzonych
- [[Notatka-2026-10-23-dane-na-strone]] — następna budowa, którą wstrzymuje decyzja 6
