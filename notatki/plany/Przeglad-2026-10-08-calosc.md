# Przegląd całości 08.10.2026 — co nie gra po zamknięciu listy z 08.09

Data: 2026-10-08 (czwartek), ok. 16:40–16:50. Przegląd według zasady 16: lista napraw z 08.09
zamknięta 04.10, warunek sesji w Producencie na EC2 od 07.10, a przeglądu po tym nie było.

## Sedno

Łańcuch danych od 08.09 jest naprawiony i pilnowany: wszystkie dziesięć punktów listy zamknięte,
kontrola o 18:30 łapie awarie i brak danych. Dziś wyszła jedna nowa wada w danych: **Yahoo
w trakcie sesji podaje złe ceny nie tylko za dziś, ale też za kilka ostatnich dni**. Warunek z 06.10
chroni tylko dzień dzisiejszy, więc przy ręcznym biegu w ciągu dnia złe ceny mogą trafić do S3.
Do tego dwie mniejsze wady (strażnik kompakcji da się obejść, repozytorium w OneDrive
z przerwanym sprzątaniem gita) i sporo nieaktualnych miejsc w README i CLAUDE.md.

## Stan punktów (aktualizacja 10.10)

| Punkt | Stan |
|---|---|
| 1.1 złe ceny Yahoo (decyzja 1) | **badanie w toku.** 09.10: zakres (`3y`/`5d`) nic nie zmienia, dobra tylko ostatnia świeca, poprzedni tydzień poprawiony po jego końcu. 10.10: w piątek o 18:00 dni 05–08.10 dalej z ceną z 02.10. Brakuje: kiedy dokładnie Yahoo poprawia tydzień. Potem notatka projektowa na decyzje 1 i 2 |
| 1.1 punkt 2, adres brokera (decyzja 2) | czeka na wspólną notatkę z decyzją 1 |
| 1.2 strażnik kompakcji (decyzja 3) | ✅ **09.10** (a)–(d): kod Gracjana, ścieżka błędu `403` → `Traceback` bez zmian w S3, próba generalna `783 → 783`, `Usunięto 0`; 10.10 `(2370, 3)` po próbie. (e) w README. Opis zawężony — sprostowanie w 1.2 |
| 1.3 git w OneDrive (decyzja 4) | zostawione; Ctrl+C przy pytaniu o kasowanie katalogu |
| 1.4 drobne | bez zmian |
| Część 3, dokumentacja (decyzja 6) | ✅ **10.10** (kolejność zmieniona decyzją Gracjana, decyzja 7 niżej): README — wszystkie miejsca z listy w Części 3, do tego warunek sesji, strażnik, złe ceny Yahoo i adres brokera jako ograniczenia „w naprawie”, rozpiska dnia biegu, 90 cen porównanych z GPW; CLAUDE.md 1395 → ok. 700 linii, codzienne sekcje stanu bez zmian w `Historia-stanu.md`; obrazki — bieg Gracjana 10.10 |

## Podstawa

- **Kod, przeczytany w całości:** 13 plików w `kod/` (`config.py`, `data_ingestion.py`,
  `session.py`, `kafka_consumer.py`, `silver.py`, `gold.py`, `compaction.py`, `control.py`,
  `path.py`, `wykresy.py`, `ranking.py`, `pipeline.bat`) i trzy pliki testów (28 testów), oba spisy
  paczek, `.gitignore`.
- **Dokumentacja, przeczytana w całości:** README, CLAUDE.md, przegląd z 08.09 (części 2, 3 i 5),
  notatka o warunku sesji z 04.10, dziennik z 07.10, 14.09 i 26.09 (we fragmentach).
- **Przeszukane pod kątem otwartych spraw** („niesprawdzone”, „do decyzji”, „odłożone”,
  „do przeglądu”, „nieodczytane”): wszystkie notatki projektowe od 10.09 i wszystkie wpisy
  dziennika od 08.09. **Wpisów i notatek sprzed 08.09 nie czytałem od nowa** — zrobił to przegląd
  z 08.09, a wszystko, co z nich wynikało, jest w jego części 2.
- **Odczyty dziś:** stan gita na laptopie, pamięć Producenta na laptopie, wyniki ręcznego
  Producenta i zapytania do Yahoo na EC2 (uruchamiał Gracjan, 14:32–14:40 UTC), archiwum notowań
  GPW z 05.10 i 07.10 (strona gpw.pl, odczyt narzędziem w przeglądarce).

**Waga** jak w przeglądzie z 08.09: 🔴 kasuje lub fałszuje dane · 🟠 ukryta awaria, nikt się
nie dowie · 🟡 brud, dług, mylące · ⚪ drobiazg.

---

## Część 1 — Nowe wady

### 1.1 🟠 Yahoo w trakcie sesji podaje złe ceny za ostatnie dni

**Co widać (dziś, 16:32 polskiego, w trakcie sesji):**

| Dzień | Cena z Yahoo o 16:32 (SNT) | Zamknięcie według GPW | W S3 (bieg o 18:00 tego dnia) |
|---|---|---|---|
| 05.10 | 341,60 | 339,80 | 339,80 |
| 06.10 | 341,60 | 343,80 (nie sprawdzone w GPW) | 343,80 |
| 07.10 | 341,60 | 342,20 | 342,20 |
| 08.10 | 344,20 (sesja trwa) | — | — |

Trzy dni z rzędu z tą samą ceną, która nie zgadza się z żadnym zamknięciem. Przy CBF i XTB
pamięć Producenta na EC2 ma po dzisiejszym biegu za 07.10 201,00 i 138,56, a GPW 199,20 i 135,00 —
czyli to samo zjawisko. Ceny w S3 za 05.10 i 07.10 zgadzają się z GPW przy wszystkich trzech
spółkach (sprawdzone dziś), wcześniej zgadzały się 17.09, 18.09 i 21.09.

**Uzupełnienie 08.10 wieczorem — mechanizm inny, niż opisany wyżej.** Bieg `cron` o 18:00
zapisał w pamięci na EC2 za 05, 06 i 07.10: CBF 3 × 201,0, SNT 3 × 341,6, XTB 3 × 138,56, a za
08.10: 196,0 / 342,8 / 137,0. Archiwum GPW z **piątku 02.10**: zamknięcia CBF **201,00**, SNT
**341,60**, XTB **138,56**. Czyli w odpowiedzi Yahoo (`range=3y`) dni bieżącego tygodnia
poprzedzające ostatni mają **piątkowe zamknięcie z poprzedniego tygodnia**, a świeży jest tylko
ostatni dzień. To nie zależy od sesji: tak było o 16:32 i o 18:00. 07.10 o 20:58 polskiego dzień
07.10 był ostatni, więc miał dobrą cenę (199,2). Jeden dzień obserwacji — kiedy Yahoo poprawia
starsze dni (np. w weekend), nie wiadomo.

Skutek dla S3: bieg z jednym nowym dniem wysyła ostatni dzień, czyli świeży — dlatego S3 zgadza
się z GPW. **Bieg z dwoma lub więcej nowymi dniami** (dzień wcześniej padł broker, Yahoo albo
EC2, albo Yahoo spóźniło się ze świecą o 18:00) wysłałby starsze dni z piątkowym zamknięciem
z poprzedniego tygodnia. Kontrola tego nie zobaczy, bo daty są dobre. To podnosi wagę z 🟠 na
🔴 (fałszuje dane), w zwykłym biegu `cron` warunkowo: tylko po dniu z awarią. Od 12.09 każdy
bieg miał `nowych dni` 0 albo 1, więc od tego dnia to się nie zdarzyło. **Do sprawdzenia:**
dni wysłane w biegach z kilkoma nowymi dniami (odzyskanie 26–31.08 dnia 03.09, pierwszy zalew
historii w sierpniu) i serie jednakowych cen w lokalnym `gold/dane_dzienne.csv` (stan 20.09):
CBF 3 × 78,80 do 16.10.2023, 3 × 126,0 do 07.06.2024, 3 × 120,0 do 17.06.2024, 4 × 179,0 do
16.03.2026; SNT 4 × 67,0 do 24.08.2023 — mogą być prawdziwe, nie porównane z GPW. Ceny za 08.10
z S3 do porównania z archiwum GPW 09.10 (o 18:48 archiwum z 08.10 było puste).

**Sprawdzone 08.10 ok. 19:00 (decyzja Gracjana: tak):** lokalny `gold/dane_dzienne.csv` (to te
same wiersze co w S3 do 20.09) porównany z archiwum notowań GPW w **66 cenach** — wszystkie zgodne
co do grosza:
- odzyskanie z 03.09 i dni wokół: 26, 27, 28, 31.08, 01 i 02.09, po trzy spółki (18 cen).
  **03.09 był bieg z kilkoma nowymi dniami** (daty wykasowane z pamięci, Producent pobrał je
  ponownie), a 31.08 był wtedy dniem bieżącego tygodnia, nie ostatnim — i przyszedł z dobrą ceną
  (CBF 194,00; piątkowe 28.08 to 198,40). Czyli zjawisko z 08.10 **nie występuje zawsze**;
- wszystkie serie jednakowych cen: CBF 78,80 (12–16.10.2023), 126,00 (05–07.06.2024), 120,00
  (13–17.06.2024), 179,00 (11–16.03.2026), SNT 67,00 (21–24.08.2023) — prawdziwe, tak było na
  giełdzie (wraz z resztą spółek z tych dni: 42 + 4 ceny);
- CBF 11.09 i 14.09 po 201,00 — prawdziwe (podejrzenie z 14.09 zamknięte, tym razem w GPW, nie
  w BiznesRadarze).

Wniosek: w historii w S3 nie ma śladu cen z poprzedniego piątku. Przy okazji: pamięć Producenta
na **laptopie** ma za 01.09 191,30 / 329,60 / 182,32, a GPW i S3 — 191,40 / 327,00 / 182,76. To
przykład „korekty Yahoo” z przeglądu 08.09 (punkt 2.1) — w S3 jest cena prawdziwa, a zła była
pierwsza wartość w pamięci laptopa (najpewniej bieg w trakcie sesji). Opis tej wady w README
(„zostaje cena z pierwszego pobrania”) do sprawdzenia przy dużej dokumentacji.

**Badanie 09–10.10 (decyzja 1a).**
- 09.10 ok. 11:45 polskiego, EC2, `python -c` bez Kafki: `range=3y` i `range=5d` dały **te same**
  ceny co do grosza — za 05–08.10 zamknięcie z 02.10, za 09.10 cena z trwającej sesji. Krótszy zakres
  nie jest drogą naprawy.
- Ten sam dzień, `3y`, dziesięć ostatnich dni: tydzień 28.09–02.10 zgodny z GPW we wszystkich 15
  cenach. Yahoo poprawia tydzień po jego zakończeniu.
- 10.10, pamięć spółek po biegu `cron` z piątku 09.10, 18:00: za 05–08.10 dalej CBF 201,0, SNT 341,6,
  XTB 138,56, za 09.10 dobre zamknięcie (200,0 / 344,0 / 139,72). Poprawka **nie** przychodzi zaraz po
  piątkowej sesji.
- Zostaje do ustalenia: czy poprawka przychodzi w weekend, czy dopiero w poniedziałek (odczyt pamięci
  po biegach 10.10 albo 12.10).

**Dlaczego to w ogóle trafia do pamięci:** `data_ingestion.py:62` (`dane[str(data)] = c`) wpisuje
każdy dzień z Yahoo, także dzień już znany, a linia 80 zapisuje cały plik od nowa. Do Kafki idą
tylko nowe daty (linie 64, 70–72), więc dziś złe ceny zostały w pamięci i nigdzie dalej nie poszły.
O 18:00 pamięć nadpisze się jeszcze raz.

**Kiedy złe ceny trafiłyby do S3:**
1. **Ręczny bieg na EC2 w trakcie sesji, gdy w pamięci brakuje ostatnich dni** (np. bieg o 18:00
   dzień wcześniej padł, bo Yahoo nie odpowiadało). Warunek pomija tylko dzisiejszą datę, więc
   wczorajszy dzień poszedłby do Kafki ze złą ceną. Kontrola o 18:30 tego nie zobaczy, bo sprawdza
   daty, nie ceny.
2. **Ręczny bieg z laptopa bez `KAFKA_BOOTSTRAP`.** Pamięć laptopa kończy się na 01.09
   (762 wiersze, EC2 ma 788). Domyślny adres brokera w kodzie (`data_ingestion.py:16`) to broker na
   EC2, więc taki bieg wysłałby **26 dni × 3 spółki** drugi raz, w trakcie sesji część ze złymi
   cenami. Konsument o 18:00 zapisałby je do `live/`, a Silver (`silver.py:15–17`) przy dwóch
   różnych cenach tego samego dnia wybiera **przypadkowo** (znana wada z 08.09, punkt 2.5). Do
   dziś ta wada była uśpiona, bo zakładaliśmy, że powtórka niesie tę samą cenę. **Nie sprawdzone:**
   czy port 9092 brokera jest dziś otwarty dla adresu laptopa.

**Czego nie wiemy:** od której godziny Yahoo podaje złe ceny i kiedy wraca do dobrych; czy to
samo dzieje się przy krótszym `range` niż `3y`; skąd są te liczby. (CBF 201,0 to dokładnie
zamknięcie z 14.09 — zbieżność, nie dowód.) Pierwszy odczyt dziś po 18:32 (Część 5).

**Związek z dotychczasowymi wadami:** to nie są „korekty wstecz” (przegląd 08.09, punkt 2.1),
bo ceny nie są poprawione, tylko złe i — jak przypuszczamy — chwilowe. Wada „cena z trwającej
sesji” była więc szersza, niż ją opisaliśmy 08.09 i 04.10: w trakcie sesji niepewne są ceny
ostatnich kilku dni, nie tylko dzisiejsza.

### 1.2 🟡 Strażnik kompakcji da się obejść jednym błędem S3

`compaction.py:28–32`: pobranie kopii `bronze` łapie **każdy** `ClientError` i przyjmuje wtedy
`poprzedni = 0`. Tak miało być dla nowej spółki (pliku jeszcze nie ma). Ale ten sam wyjątek
przychodzi przy braku uprawnień, przerwie w sieci czy chwilowym błędzie S3. Wtedy:
- nie ma kopii w `bronze/poprzedni/`;
- strażnik w linii 37 porównuje nową liczbę z zerem i przepuszcza wszystko — także pół tabeli
  z Atheny, przed którym miał chronić (04.09: 405 zamiast 2283).

Do tego kopia ma jedno pokolenie: każda kompakcja nadpisuje `bronze/poprzedni/`. Kompakcja jest
ręczna, raz w miesiącu, więc zbieg dwóch rzadkich zdarzeń jest mało prawdopodobny. Następna:
początek listopada.

**Sprostowanie 09.10:** „przerwa w sieci” wyżej to błąd tego przeglądu. Błędy sieci
(`EndpointConnectionError`, `ConnectTimeoutError`, `ReadTimeoutError`) i brak kluczy
(`NoCredentialsError`) nie są `ClientError`, więc już przed poprawką zatrzymywały skrypt. Linia 31
łapała tylko odpowiedzi S3 z kodem błędu (np. `403`, `503`).

**✅ Naprawione 09.10** (notatka `Notatka-2026-10-09-straznik-kompakcji.md`, instrukcja
`Notatka-2026-10-09-jak-poprawic-straznika.md`, pięć decyzji (a)): pobranie kopii przeniesione nad
zapytanie do Atheny, `poprzedni = 0` tylko przy kodzie `"404"`, każdy inny kod → `raise`. Sprawdzone:
kody S3 z laptopa (`404` i `403`), ścieżka błędu na prawdziwym skrypcie (zmyślone klucze →
`Traceback` z `(403) … HeadObject … Forbidden`, `bronze/` i `live/` bez zmian), próba generalna
(3 × `783 → 783`, `Usunięto 0 plików`, rozmiary `bronze/` co do bajtu te same), 10.10 Silver
`(2370, 3)`. Zostaje świadomie: skasowany plik `bronze` dalej wygląda jak nowa spółka; jedno
pokolenie kopii.

### 1.3 🟡 Repozytorium w OneDrive i przerwane sprzątanie gita (07.10)

Po commicie `41029da` git sam zaczął sprzątanie (`git gc --auto`), Windows nie pozwolił skasować
pustego katalogu (najpewniej trzymał go OneDrive — nie sprawdzone), Gracjan przerwał Ctrl+C.
Stan dziś (`git count-objects -v`): **734 luźne obiekty, wszystkie już w paczce**
(`prune-packable: 734`), 4 puste katalogi w `.git/objects`, zero plików-konfliktów OneDrive w
`.git`. Danych to nie rusza, commit i `push` z 07.10 są w porządku. **Nie sprawdziłem**, przy
którym commicie git znów sam ruszy sprzątanie.

Ważne przy decyzji: dziennik leży w folderze repozytorium (poza gitem) i jego **jedyna kopia
w chmurze to OneDrive** (decyzja 06.10). Przeniesienie repozytorium poza OneDrive zabrałoby
dziennikowi tę kopię.

### 1.4 Drobne

- 🟡 **Kod Producenta poza `session.py` nie ma testów** — scalanie pamięci z odpowiedzią Yahoo,
  wybór nowych dni, flaga zapisu (linie 33–84). Dzisiejsza wada siedzi właśnie tam. Plik nie ma
  części `__main__`, więc nie da się go zaimportować w teście (wiadomo od 04.10).
- ⚪ `data_ingestion.py:37`: linia pamięci bez `", "` daje `ValueError` poza `try` → `Traceback`,
  Producent staje przy tej i kolejnych spółkach. Głośne (kontrola), a plik pisze tylko program.
- ⚪ `path.py:8`: `sprawdz_daty` dopisuje kolumnę `dzien` do tabeli, którą dostała, czyli zmienia
  dane wywołującego. Dziś bez skutku.
- ⚪ `s3://gpw-tracker-bucket/athena-results/` rośnie bez końca — każde zapytanie (Silver,
  kontrola, wykresy, kompakcja) zostawia plik wyniku. Koszt pomijalny; **rozmiaru nie sprawdziłem**.
- ⚪ `data_ingestion.py:89–90`: `flush()` bez `close()` — bez skutku.

---

## Część 2 — Wady z 08.09: co dalej jest

| Wada (punkt przeglądu 08.09) | Dziś | Waga dziś |
|---|---|---|
| Cena z trwającej sesji (2.1) | Warunek na EC2; dowód pominięcia dziś 14:32 UTC; brakuje dzisiejszego biegu `cron` | 🟨 → po wieczorze ✅, ale patrz 1.1 |
| Kwadrans zapasu u Yahoo (2.1) | Ograniczenie w README; od 26.09 głośne (kontrola: brak świecy) i samo się naprawia | 🟡 |
| Korekty Yahoo wstecz (2.1) | Ograniczenie w README; dziś uzupełnione o złe ceny w trakcie sesji (1.1) | 🟠 |
| `except` łapie `TypeError`/`KeyError` (2.1) | Dalej, `data_ingestion.py:87`: błąd w kodzie wygląda jak błąd pobierania. Głośne (brak `stan: zapisane`) | ⚪ |
| Adres brokera na sztywno (2.1, 2.3) | Dalej, `data_ingestion.py:16`, `kafka_consumer.py:7`. Na EC2 bezpieczne od 08.09; z laptopa — patrz 1.1 | 🟠 (z laptopa) |
| Jedno źródło, bez planu B (2.1) | Ograniczenie w README | 🟡 |
| Retencja Kafki 7–14 dni (2.2) | Złagodzone: martwy Konsument daje alarm pierwszego wieczoru. Nie ma spisanego sposobu odzyskania, gdyby leżał ponad tydzień | 🟡 |
| `t3.micro` bez zapasu (2.2) | Bez zmian, od 31.08 bez kłopotu | 🟡 |
| Pole `spółka` dubluje partycję w `live` (2.3) | Dalej | 🟡 |
| `close()` bez `finally` (2.3) | Ograniczenie w README | ⚪ |
| Nowa spółka niewidoczna w Athenie (2.4) | Ograniczenie w README, warunek „przed dodaniem spółki” | 🟠 przy 4. spółce |
| `AWSGlueConsoleFullAccess` (po 2.4) | Możliwe zawężenie, osobna decyzja | ⚪ |
| Przypadkowy wybór ceny w Silverze (2.5) | Dalej; po 1.1 groźniejszy, bo dwie różne ceny tego samego dnia są realne | 🟠 |
| `assert` po `drop_duplicates` zawsze przejdzie (2.5) | Dalej, `silver.py:22`; liczbę dni między spółkami sprawdza od 26.09 kontrola | ⚪ |
| Nierówne okna `range=3y` (2.6) | Ograniczenie w README | 🟡 przy 4. spółce |
| Kolejność wierszy rankingu (notatka 12.09, „do decyzji kiedy indziej”) | Sprawa strony | ⚪ |
| Ostrzeżenia w logu (2.7) | Zostały dwa rodzaje: `pandas` (SQLAlchemy) i `kafka-python` (`value_deserializer`); `boto3` zniknęło 03.10 | ⚪ |
| Kompakcja ręczna (2.8) | Ograniczenie w README; do tego 1.2 | 🟡 |
| Nic nie sprawdza, że kod na EC2 = GitHub (2.10) | Dalej; w praktyce `git log -1` przy każdym wdrożeniu | 🟡 |
| Klucz `.pem` w OneDrive (2.10) | Dalej | ⚪ |
| Power BI na starych plikach | Odłożony 03.10, README mówi „dane do 20.09” | 🟡 |

---

## Część 3 — Dokumentacja niezgodna z dzisiejszym stanem

**README** (sprawdzone dziś, numery linii z bieżącego pliku):
- linia 9: „stan … dotyczy 04.10”; linie 21 i 112: liczby do 02.10 (2355 wierszy, 785 dni,
  procenty); obrazki z tytułem „stan na: 2026-10-02” (sprawdzony `ranking.png`);
- linia 108: „sprawdzone do 06.10”;
- linie 95 i 165: „18 testów” — jest 28 (10 w `test_session.py`);
- tabela skryptów (151–167): brak `session.py` i `test_session.py`; linia 156 bez warunku sesji;
- linie 120–123: warunek opisany jako „na EC2 jeszcze go nie ma”;
- linia 146: „uprawnienie IAM do odpięcia” — odpięte 04.10;
- linie 124–125: korekty wstecz — do uzupełnienia o 1.1;
- sekcja „Jak projekt pilnuje sam siebie” (71–97): brak warunku sesji.

**CLAUDE.md:**
- „Wciąż otwarte” ma pozycje zamknięte: „Producent uruchomiony przed 17:00…” (warunek na EC2),
  „Testy sprawdzają rzeczy obok potoku” (zamknięte 26.09), „README obiecuje więcej, niż jest”
  (04.10), „Nowe 21.09: wykresy … czytają lokalne” (03.10), „(15.09) kompakcja, wykresy i Power BI
  nie mają miejsca w kolejności” (rozstrzygnięte 03.10);
- „32 pliki dziennika na 15.09” — dziś 48;
- **1311 linii.** Większość to codzienne sekcje stanu. Plik czyta się na starcie każdej sesji;
  zasady giną między liczbami z poszczególnych dni.

**Przegląd z 08.09:** część 5 — wiersz „Cena z trwającej sesji” do zamknięcia po dzisiejszym
wieczorze. W części 2 kilka punktów bez dopisku o dzisiejszym stanie (tabela w Części 2 wyżej
je zbiera).

**Słownik:** dziś nowe `python -c` i znacznik czasu Unix (sekundy od 01.01.1970 UTC). Indeks
ujemny (`[-4:]`) już jest (linia 1546).

---

## Część 4 — Jak pracowaliśmy od 08.09 (pomyłki Claude'a, wzór)

Pomyłki z listy w CLAUDE.md mają dwa powtarzające się kształty:
1. **Przewidywanie z głowy zamiast z kodu albo z liczenia:** godziny `date` (21.09, 07.10, dziś),
   liczba linii w commicie (17.09, 03.10), dni w przewidywaniach na kilka biegów naprzód (25.09,
   03.10), dziś cena CBF w pamięci — przewidziana stara, choć linia 62 nadpisuje stare ceny przy
   każdym biegu.
2. **Twierdzenie bez otwarcia pliku:** komentarz w `compaction.py` (04.10), `Codzienna-rutyna`
   (04.10), słownik (26.09 i dziś: indeks ujemny przedstawiony jako nowy).

Żadna z nich nie zepsuła danych, bo liczby przewidywane są przed biegiem i każdy rozjazd wychodzi
od razu. Ale to ten sam mechanizm, który 08.09 kosztował zaufanie: pewność bez sprawdzenia.

---

## Część 5 — Niesprawdzone i terminy

**08.10 po 18:32 — kontrola pierwszego biegu `cron` na nowym kodzie, zrobiona (odczyt 16:46 UTC):**
wszystko trafione — start 1168, `wc -l` 1195, blok 28, 3 × `nowych dni: 1, wysłane: 1, stan:
zapisane` bez dopisku, `Odebrano 3`, 2 × `(2367, 3)`, `Kontrola: Dane 2367 wierszy`, `OK`, zakładka
2396, pliki 789 × 3, `errors.log` 8, S3 158499 B / 339 B (16:10:07 UTC), `git status --short`
pusty, stróż #24 `OK`, na Interii brak maila. Odczyt do 1.1 (`tail -n 4 companies/*.WA.txt`):
**przewidywanie „Yahoo wieczorem wraca do dobrych cen” chybione** — za 05–07.10 dalej piątkowe
zamknięcie z 02.10 (opis w 1.1). Ceny za 08.10 w S3: CBF 196,0, SNT 342,8, XTB 137,0 —
porównanie z GPW 09.10.

**Dalej niesprawdzone:** treść zgłoszenia #21 u stróża (polskie litery); port 9092 dla laptopa;
rozmiar `athena-results/`; ~~od której godziny Yahoo psuje ostatnie dni~~ — to nie zależy od
godziny, tylko od tego, czy po dniu przyszedł następny (09.10); zostaje: kiedy Yahoo poprawia tydzień.

**09.10 (kontrola zrobiona 10.10, 12:35 UTC):** wiersz 09.10 tabeli w CLAUDE.md trafiony w całości —
start 1196, `wc -l` 1223, `Odebrano 3`, 2 × `(2370, 3)`, `Dane 2370`, `OK`, pliki 790 × 3, zakładka
2399, S3 158692 B / 338 B, stróż #25. Ceny z 08.10 i 09.10 w S3 zgodne z archiwum GPW.

**Terminy (bez zmian):** ok. 17.10 stary `venv` na EC2 do decyzji; 25.10 pierwszy bieg po zmianie
czasu (`17:00:0X`), sprawdzian strefy u stróża; 26.10 pierwszy dzień giełdowy zimą; 01.11 Gold
zmienia `117`/`111`; początek listopada kompakcja (po decyzji o 1.2); 11.11 fałszywy alarm w
święto; 19.02.2027 koniec darmowego planu AWS.

---

## Część 6 — Do decyzji Gracjana

**Decyzja Gracjana 08.10 ok. 16:50: wszystkie siedem punktów w wariancie (a)** („pełna zgoda”).
Skutek: od dziś ten plik jest źródłem prawdy o wadach; złe ceny w trakcie sesji najpierw badamy
(odczyt 08.10 po 18:32 i 09.10 w trakcie sesji), potem jedna notatka projektowa na punkty 1 i 2
razem; strażnik kompakcji przed listopadem; CLAUDE.md odchudzony przy dużej dokumentacji.

Rekomendacja Claude'a pierwsza przy każdym punkcie. Zasada 15 („najpierw naprawa”) dotyczyła
listy z 08.09, która jest zamknięta. O tym, czy nowe wady blokują dużą dokumentację i stronę,
decydujesz teraz.

1. **Złe ceny w trakcie sesji (1.1):**
   - (a) **najpierw zbadać, bez kodu:** dzisiejszy odczyt po 18:32 i jeden odczyt jutro w trakcie
     sesji. Potem wybór między (b) i (c), z notatką projektową;
   - (b) przed 17:55 Producent nic nie pobiera i nic nie wysyła, tylko wypisuje, że bieg pominięty.
     Skutek: ręczny bieg w ciągu dnia staje się bezużyteczny, ale bezpieczny; nadrabianie zawsze
     o 18:00 albo ręcznie po 17:55. Mała zmiana pliku, który właśnie wdrożyliśmy;
   - (c) zostawić kod, opisać w README i spisać zasadę „ręczny Producent tylko po 18:00”.
2. **Domyślny adres brokera (1.1, punkt 2):**
   - (a) **bez domyślnego adresu:** brak `KAFKA_BOOTSTRAP` = głośny błąd na starcie. Na EC2 nic się
     nie zmienia (`crontab` i ręczne biegi już go podają). Najlepiej w tej samej zmianie co 1(b);
   - (b) zostawić i opisać.
3. **Strażnik kompakcji (1.2):**
   - (a) **przed listopadową kompakcją:** tylko „nie ma takiego pliku” znaczy nową spółkę, każdy inny
     błąd S3 przerywa bieg przed zapisem;
   - (b) opisać jako ograniczenie.
4. **Git w OneDrive (1.3):**
   - (a) **zostawić**; gdy pytanie o kasowanie katalogu wróci — przerwać jak 07.10 albo wstrzymać
     OneDrive na czas commita;
   - (b) jednorazowe sprzątanie (`git prune-packed`) przy wstrzymanym OneDrive;
   - (c) przenieść repozytorium poza OneDrive — wtedy dziennik traci jedyną kopię w chmurze.
5. **Źródło prawdy o wadach:**
   - (a) **od dziś ten plik**; przegląd z 08.09 dostaje blok „dokument historyczny” jak stare plany;
   - (b) dopisywać dalej do przeglądu z 08.09.
6. **CLAUDE.md (1311 linii):**
   - (a) **przy dużej dokumentacji przenieść codzienne sekcje stanu do osobnego pliku z historią**,
     w CLAUDE.md zostawić zasady, stan dzisiejszy, kontrolę i terminy;
   - (b) zostawić.
7. **Kolejność:**
   - (a) **1 i 2 przed dużą dokumentacją** (dotyczą Producenta, który README i tak będzie opisywał
     od nowa), 3 przed kompakcją w listopadzie, reszta Części 2 jako ograniczenia w README;
   - (b) wszystko jako ograniczenia, duża dokumentacja od razu.

   **Zmiana 10.10 (decyzja Gracjana, zgodnie z rekomendacją Claude'a):** duża dokumentacja przed
   naprawami 1 i 2, bo notatka o nich czeka na dane (kiedy Yahoo poprawia tydzień). Koszt: po
   naprawach README trzeba poprawić drugi raz w kilku miejscach (opis Producenta, ograniczenia).
   1 i 2 dalej przed kodem strony (ustalenia jej wyglądu mogą iść wcześniej). Punkt 3 zrobiony
   09.10.

---

## Powiązane notatki

- [[Przeglad-2026-09-08-co-nie-gra]] — poprzedni przegląd, numery punktów 2.x w Części 2
- [[Notatka-2026-10-04-producent-przed-zamknieciem]] — warunek sesji, którego dotyczy 1.1
- [[Notatka-2026-10-04-jak-napisac-warunek-sesji]] — Część 8: wdrożenie i dzisiejszy dowód
