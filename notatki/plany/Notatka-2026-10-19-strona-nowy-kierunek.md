# Strona GPW Pulse — nowy kierunek (19.10, szkic wizji do rozmowy)

**Status:** propozycja Claude'a do omówienia, nic niezatwierdzone. Powstała na prośbę Gracjana z 19.10:
strona wygląda „za bardzo AI”, „jak sprzed 20 lat”: jest prostolinijna i bez animacji. Ma być
portal z zakładkami, animacjami 3D i udogodnieniami, których nie mają inne serwisy.

**Decyzje Gracjana z 19.10:**
- **kod strony pisze wyłącznie Claude** (zmiana zasady 1 dla strony); Gracjan uzgadnia każdy
  element. Projekt jest o inżynierii danych, więc tego, jak pisze się stronę, Gracjan się nie uczy;
- ustalenia z partii 1–10 zostają tam, gdzie dotyczą czcionki, kolorów spółek, suwaka, dostępności,
  liczb i dat. Zmienia się wygląd i układ całości;
- partia 11 (kto co generuje) wstrzymana;
- motyw czarno-czerwony to propozycja, nie decyzja.

Źródła: pomysły Gracjana (zrzut pliku `Strona - pomysły.txt`); 5 stron wzorcowych (capital.com/markets,
gocharting.com, amcharts.com, tradingview.com, scrab.com); szukanie na forach (wynik niżej). Przykłady
wyglądu: Artifact „Kierunki strony GPW Pulse” (`https://claude.ai/artifact/Q6aru8Z6RTjJTSoytAfyZa`),
trzy strony główne: A czerń i czerwień z wstęgami cen w 3D, B nocny granat z animowaną drogą danych,
C jasny, redakcyjny, z kartami spółek w 3D. Rekomendacja Claude'a: kolory B, wstęgi 3D z A na Start,
droga danych z B w zakładce Projekt.

---

## 1. Co zobaczyłem na stronach wzorcowych

| Strona | Co z niej wziąć | Czego nie brać |
|---|---|---|
| TradingView | ciemny ekran startowy z jednym mocnym obrazem (Ziemia nocą), duży nagłówek, wykres jako bohater | gęstość narzędzi dla zawodowców |
| GoCharting | ciemne tło, jeden kolor akcentu (pomarańcz) tylko na przyciskach, zrzut aplikacji pod nagłówkiem | nachalne „Create account” |
| Scrab | gradient w tle, zaokrąglone przyciski, prosty przekaz w jednym zdaniu | gradient „jak z AI” (to dokładnie ten wygląd, którego chcemy uniknąć) |
| amCharts | animowane linie wykresu w tle nagłówka (ruch, który coś znaczy) | — |
| capital.com/markets | lista rynków z liczbami i zmianą, kafelki kategorii | baner o ryzyku CFD; przy wejściu ekran zgód (cookies) zasłonił stronę — u nas bez śledzenia, więc bez takiego ekranu |

Wspólny mianownik: ciemne tło, jeden mocny ruchomy element na pierwszym ekranie, dużo powietrza, liczby
duże i równe, akcent w jednym kolorze.

## 2. Czego brakuje użytkownikom (fora i opinie)

Wynik wyszukiwania jest cienki: mało bezpośrednich wątków, dużo stron reklamowych. Poniżej tylko to,
co się powtarzało.
- **Wyjaśnienia prostym językiem.** Serwisy pokazują „P/E 28,4” i zakładają, że czytelnik wie, co to
  znaczy (StockDeck, Indie Hackers). U nas: słownik wpięty w tekst — najechanie na pojęcie pokazuje
  definicję.
- **Streszczenia raportów:** najważniejsze liczby, porównanie z oczekiwaniami i z rokiem wcześniej,
  zmiana prognozy, link do źródła (Vero, Earnings Hub, Tired Banker — wszystkie płatne albo
  amerykańskie).
- **Jeden kalendarz dywidend i wydarzeń** dla obserwowanych spółek. Na forum Freetrade prośba wracała
  wiele razy i była zamykana bez wdrożenia.
- **Rozbieżne daty.** Agregatory podają różne terminy tego samego raportu. Spółki z GPW często
  przesuwają terminy albo czekają do ostatniego dnia (raport Navigator Capital). Pełnego,
  darmowego kalendarza WZ, dywidend i raportów dla GPW nie ma. Źródłem prawdy są komunikaty ESPI/EBI.
- **Powiadomienia o zdarzeniach spółki**, np. zmianach w zarządzie.
- **Konsensus prognoz analityków jest płatny** (BiznesRadar Premium). Darmowego źródła nie
  znalazłem — niesprawdzone do końca.
- **Polscy inwestorzy (OBI, artykuły Parkietu, SII):** oczekują przejrzystej, wieloletniej polityki
  dywidendowej i kompletnej strony dla inwestorów. Skarżą się, że spółki zwlekają z informacjami.
  W teście Parkietu część spółek z WIG20 nie odpowiedziała drobnym inwestorom.
- **Śledzenie transakcji insiderów** (w USA OpenInsider). Na GPW odpowiednikiem są komunikaty
  o transakcjach osób z zarządu, publikowane w ESPI. Pomysł: osobny filtr w Aktualnościach i znaczniki
  na wykresie.

## 3. Zakładki (propozycja)

1. **Start.** Pierwszy ekran z animacją 3D (np. trzy linie cen jako wstęgi w przestrzeni),
   kafelki trzech spółek, najbliższe wydarzenia z kalendarza, ostatnie streszczenia, pojęcie dnia
   ze słownika, pasek „co się zmieniło od Twojej ostatniej wizyty”, zaproszenie do zakładki Projekt.
2. **Wykresy.** Duży wykres z ustaleniami z partii 4 i 8–10, znaczniki wydarzeń na osi
   (dywidenda, WZ, raport), porównanie spółek od wspólnej setki, kalkulator „gdybyś kupił za 1000 zł
   dnia X” (z zastrzeżeniem, że to nie porada).
3. **Spółki.** Karta każdej spółki: czym się zajmuje, zarząd, akcjonariat, wyniki kwartalne
   (tabela i wykres), historia dywidend, wskaźniki z objaśnieniem.
4. **Raporty.** Streszczenia raportów okresowych w pięciu liczbach, porównanie rok do roku,
   „co nowego”, link do raportu źródłowego.
5. **Aktualności i walne zgromadzenia.** Oś zdarzeń z komunikatów ESPI/EBI z filtrami (WZ,
   dywidenda, zarząd, umowy). Przy WZ: termin, porządek obrad, uchwały, wynik. Bez przepisywania
   artykułów mediów — tylko własne skróty i link.
6. **Kalendarz.** Duży kalendarz z widokiem miesiąca i listą. Przy każdym wydarzeniu stopień
   pewności terminu („potwierdzony w ESPI”, „przewidywany wg zeszłego roku”, „przesunięty”), a po
   wydarzeniu „jak się skończyło”: wynik a rok wcześniej, dywidenda uchwalona a proponowana.
   Dopisanie do własnego kalendarza (plik `.ics`).
7. **Słownik.** Tylko pojęcia giełdowe (data engineering zostaje w lokalnym słowniku). Każde
   pojęcie podlinkowane tam, gdzie występuje na stronie.
8. **Projekt.** Interaktywna droga danych: Yahoo → Producent → Kafka → Konsument → S3 → Athena →
   pandas → strona, z animowanymi paczkami danych. Kliknięcie etapu pokazuje opis, narzędzie i liczby
   z ostatniego biegu. Przewijanie prowadzi przez cały proces krok po kroku. Jest też panel jakości
   danych: liczba cen zgodnych z GPW, godzina ostatniego biegu, stan kontroli.

## 4. Udogodnienia, których inni nie mają (moje pomysły)

- **Panel zaufania do danych.** Pokazuje, ile cen sprawdzono z archiwum GPW (dziś 108 zgodnych), kiedy
  był ostatni bieg i czy kontrola dała OK. Wynika wprost z tego, co projekt już robi, i żaden portal
  tego nie pokazuje.
- **„Od Twojej ostatniej wizyty”.** Przeglądarka zapamiętuje dzień wizyty (bez logowania i bez
  ciasteczek śledzących) i pokazuje zmianę cen oraz nowe wydarzenia od tamtej chwili.
- **Słownik w tekście** (patrz punkt 2) i przełącznik „tryb początkującego”, który dokleja
  objaśnienia przy liczbach.
- **Kalendarz z pewnością terminu i historią przesunięć** (patrz punkt 2).
- **Wydarzenia na wykresie.** Kliknięcie znacznika otwiera streszczenie komunikatu.

## 5. Co to znaczy dla inżynierii danych

Nowe zakładki potrzebują nowych źródeł danych, a każde źródło to osobna droga danych w projekcie:
pobranie, bronze, silver, gold i kontrola. To jest praca Gracjana, nie strony.
- **Komunikaty ESPI/EBI** (aktualności, WZ, dywidendy, terminy raportów). Sposób pobierania i warunki
  korzystania z serwisu — niesprawdzone.
- **Wyniki finansowe** z raportów (PDF albo XBRL/ESEF) — trudne; niesprawdzone, czy da się to zrobić
  darmowo i legalnie.
- **Streszczenia.** Trzy możliwości: pisze je Gracjan ręcznie, robi je model językowy z kontrolą
  liczb, albo strona pokazuje tylko liczby i link. Do decyzji.
- **Przewidywania wyników:** darmowego konsensusu nie znalazłem. Bezpieczniej pokazać wynik sprzed
  roku i ewentualną prognozę zarządu niż własne przewidywania (ryzyko rekomendacji inwestycyjnej,
  wiedza ogólna, niesprawdzone).

## 6. Ryzyka

- **Zakres.** To kilka razy więcej pracy niż jedna strona z 06.10. Bez etapów łatwo nie skończyć
  przed 19.02.2027 (koniec darmowego AWS).
- **Kolejność:** decyzja 7 (kod strony po naprawach 1 i 2) dalej obowiązuje, porcja 5 jest 20.10.
- **Czerwony akcent a spadek.** Na giełdzie czerwony znaczy spadek, a XTB ma czerwony kolor
  spółki. Przy motywie czarno-czerwonym akcent nie może wyglądać jak spadek (strzałki i znaki z 3.2
  muszą zostać).
- **3D a dostępność i telefon.** Zgodnie z partią 10: ruch wyłączony przy „ogranicz ruch”. Plik
  three.js to ok. 600 kB (wiedza ogólna, do sprawdzenia przy kodzie). Na słabym telefonie wersja
  bez 3D.
- **Prawo:** warunki Yahoo i GPW, prawa autorskie do artykułów, zasady publikowania prognoz.
  Wszystko niesprawdzone, do partii o ryzykach.

## 7. Propozycja etapów

1. Start, Wykresy, Projekt — dane, które już mamy.
2. Słownik i Kalendarz — kalendarz najpierw ręcznie, potem z ESPI.
3. Spółki, Raporty, Aktualności i WZ — wymagają nowych dróg danych.

## 8. Odpowiedzi Gracjana (19.10)

1. **Dane do strony przygotowuje Gracjan** (Python, drogi danych). Claude pisze HTML, CSS
   i JavaScript.
2. **Streszczenia pisze Claude.** Styl, długość i charakter ustalimy później.
3. **Zakres: trzy spółki**, później może więcej.
4. **Przewidywania:** zamiast konsensusu analityków wynik sprzed roku i prognoza zarządu, jeśli spółka
   ją publikuje.
5. **Kolejność:**
   - wersja 1: to, co już mamy — Start, Wykresy, Słownik, Projekt;
   - kolejne wersje: streszczenia, wydarzenia, aktualności;
   - **kalendarz możliwie szybko**, na początek nieinteraktywny, zrobiony przez Claude'a z danych
     znalezionych w sieci (szczegóły do ustalenia).
6. **Strona statyczna** zostaje.
7. **Wygląd:** kolory z kierunku A (czerń i czerwień), grafika z kierunku C (karty spółek w 3D),
   ale płynniejsza.
8. **Teksty na stronie:**
   - bez informacji typu „ceny sprawdzone z archiwum GPW” — panel zaufania i podobne dopiski znikają;
   - bez podpisów pod sekcjami i bez znaczka „Dane z sesji: …” (zmienia 2.3 z partii 2);
   - w opisach bez nazw spółek, tylko „spółki z GPW” albo podobnie.

---

## 9. Decyzje Gracjana z 20.10 (szkic: Artifact „Strona startowa GPW Pulse”)

**Start (zamknięta, „wygląda świetnie”; wrócimy przy nowych pomysłach):**
- animacje **zawsze włączone**, także przy systemowym „ogranicz ruch” (zmienia partię 10);
  przełącznik „Animacje” na razie zostaje — do decyzji, czy zostaje na stałe;
- podtytuł bez słowa „czytelnym”: „Notowania, zmiany i wykresy wybranych spółek z GPW w jednym miejscu.”;
- siatka 3D: hasło **„Wszystkie sesje w jednej przestrzeni”**; kliknięcie liczone na wysokości
  siatki (wcześniej 0,9 jednostki nad nią — pierścień lądował ok. 66 px niżej niż kursor);
  na dotyku kamera nie podąża za palcem;
- panel „Jak powstaje ta strona”: **wariant B** — czerwone światło ze srebrną smugą płynie bez
  przerwy po obwódkach etapów i przewodzie, 90 px/s; cały bieg w jednym wierszu (panel 3 : 2,
  dwie kolumny od 1150 px, na telefonie zawija się);
- stos kart: zostaje dawny ruch z przenikaniem (przejście po łuku odrzucone).

**Kalendarz (pierwsza wersja zaakceptowana):**
- zakres: raporty okresowe, dni bez sesji, walne zgromadzenia, dywidendy (1b); u góry 4 najbliższe
  wydarzenia, niżej siatka miesiąca na kratce z czerwoną poświatą, od stycznia 2026 do sierpnia 2027;
- kafelki dni i karty u góry: **szkło** (biel 7,5% z rozmyciem, kratka prześwituje);
- okres raportu w miesiącach kalendarzowych (3a); dni bez sesji szare, kreskowane (4a);
- statusy: **zapowiedziany**, **opublikowany** (raporty), **zakończone** (WZ i dywidendy) (5a);
- opis dnia po najechaniu, dotknięciu albo z klawiatury.
- Źródła dat: harmonogramy ESPI spółek (XTB 1/2026, Cyber_Folks 1/2026, Synektik 48/2026),
  uchwała GPW 753/2025 (przez SII); WZ i dywidendy: Synektik 6/2026 (przeczytany), XTB 12/2026
  (streszczenie wyszukiwarki i artykuł z 08.05), Cyber_Folks — zwołanie ZWZ na 18.05 (przeczytane),
  dywidenda z trzech portali. Synektik 12.02: publikacja potwierdzona artykułem PAP, dzień nie.

**Wykresy (w toku):**
- układ (a): karty spółek u góry, duży wykres na całą szerokość, pod nim statystyki, mapa miesięcy,
  ranking; rysunek **własny SVG** (zamiast Plotly z 06.10); ruch przy wejściu i zmianie okresu;
  przełącznik **Cena / Zmiana %**;
- linie **czyste (D)**: bez cieniowania i bez świecenia; plakietki 15 px, pogrubione;
- wybór spółek: kliknięcie karty albo legendy dodaje lub zdejmuje spółkę; nic nie wybrane = trzy;
- pełny ekran = cały ekran okna (✕ albo Esc), nie rozciąganie w dół;
- „Na wykresie”: **Wydarzenia** (znaczki R/W/D z kalendarza, włączone na start), **Pomiar**
  (1. klik początek, 2. koniec, 3. usuwa, 4. nowy), **Średnia 20 sesji** (szara, przerywana);
- pod wykresem: **statystyki okresu**, **mapa miesięcy**; w kartach **„dziś na tle historii”**;
- odrzucone: maks. i min.; wolumen — może w przyszłości (nowa droga danych Gracjana); WIG20 — nie teraz.

---

## 10. Decyzje Gracjana z 22–23.10: zakładka Projekt

**Treść (22.10, „według Twoich rekomendacji”):** tekst „O projekcie” z 12.10 jako podstawa, z trzema
poprawkami (własny rysunek zamiast Plotly; Producent wysyła tylko dzisiejszą świecę, zaległe dni
wstrzymuje; „trzech spółek” zamiast nazw); 5 ograniczeń z linkiem do README; liczby z biegu 22.10
wpisane na stałe. Sekcje: wstęp, schemat drogi danych z kartą, dzień biegu, warstwy danych, przy
awarii, narzędzia, ograniczenia.

**Układ (22.10): B — schemat i karta.** Schemat całej drogi (10 elementów w 5 etapach), kliknięcie
elementu otwiera kartę: etap, opis, narzędzie, gdzie działa, kiedy, liczba z ostatniego biegu,
„gdy coś pójdzie źle”, poprzedni / następny. Układy A (opowieść) i C (dokument) odrzucone.

**Wygląd schematu (23.10): 1 — tor do wybranego**, po trzech rundach (wersje 27–29; odrzucone: ikony,
karty 3D, etapy w kolumnach, lista z kartą obok, linia metra w trzech odmianach):
- kafelki z numerem etapu, godziną, nazwą i rolą; numery etapów przed wybranym czerwone, wybrany
  kafelek z cienką czerwoną obwódką, kafelki za nim przygaszone do 60%;
- przewody przed wybranym jednolicie czerwone, bez płynących kresek i bez poświaty („za dużo się
  dzieje”);
- światło przechodzi raz po każdym wyborze, od Yahoo Finance do wybranego kafelka, 1,4–3,2 s,
  z łagodnym startem i końcem, i znika;
- od 700 px dwa rzędy po 5; na telefonie kafelki jeden pod drugim na całą szerokość, z krótkim
  pionowym przewodem pod numerem etapu, światło z góry na dół;
- kompakcja z przerywaną obwódką (ręcznie, raz w miesiącu).

Przy okazji poprawiony tekst awarii przy Athenie (23.10), zgodnie z `kod/silver.py`: „Brak albo
nadmiar spółki: program Silver przerywa pracę z błędem. Pustą cenę i powtórzony dzień usuwa bez
komunikatu, a przy dwóch cenach z jednego dnia zostawia przypadkową.”

**Wykresy i Start (23.10):**
- kolumny „Najwyższa” i „Najniższa” w tabeli statystyk okresu **zostają** (są w szkicu);
- siatka 3D na Start **zostaje od 18.03.2026** — jest tylko wizualizacją, nie ma dostarczać danych.

Dalej: notatka projektowa o danych na stronę, `Notatka-2026-10-23-dane-na-strone.md`.
