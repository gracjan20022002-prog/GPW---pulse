# Notatka projektowa: strona GPW Pulse (budowana partiami od 10.10)

**Status:** w budowie. Każdy aspekt strony omawiany osobno, jedną partią na raz (prośba Gracjana
10.10: „każdy aspekt strony omówić osobno, aby strona była jak najbardziej dopracowana”). Po każdej
partii decyzje trafiają tutaj. **Kod strony dopiero po naprawach 1 i 2 z przeglądu z 08.10** (decyzja
7) i po zatwierdzeniu całej notatki. Przed kodem przyjdzie pełna instrukcja (zasada 3).

## Podstawa: decyzje z 06.10

1. Ogląda każdy z linkiem, bez logowania.
2. Skrypt w Pythonie składa gotowy plik HTML (strona statyczna). Nie ma aplikacji na serwerze.
3. Wykresy w Plotly. JavaScriptu nie piszemy. Power BI nie trafia na stronę.
4. Najpierw plik na laptopie, potem GitHub Pages. Odświeżanie np. przez GitHub Actions z osobnym
   kluczem AWS tylko do odczytu.
5. Pierwsza wersja to jedna strona: kafelki, wykres trzech spółek i ranking. Zakładki spółek
   i słownik później.

## Wstępne decyzje z 10.10 (na szkicu, przed partiami)

| # | Aspekt | Decyzja Gracjana |
|---|---|---|
| 1 | wykres cen | **(a)** ceny w zł z przyciskami zakresu (1 mies., 6 mies., 1 rok, całość) **oraz ręczny wybór okresu**. Jak dokładnie ma działać ręczny wybór, rozstrzygnie partia o wykresie |
| 2 | kafelki | **(b)** cena i zmiana dzienna (zielona albo czerwona) **plus mały wykres ostatniego miesiąca** w każdym kafelku. Data ostatniej sesji raz, w znaczku u góry |
| 3 | ranking | **(a)** tabela: zmiana od 14.08.2023 i najbardziej zmienny pełny miesiąc, pod tabelą jedno zdanie, co znaczy „zmienny” |
| 4 | nazwy i kolory | **(a)** pełne nazwy ze skrótem (Synektik SNT), jeden stały kolor spółki w kafelku, na wykresie i w rankingu |
| 5 | język | **(a)** polski |
| 6 | stopka | **(a)** źródło, porównanie z GPW, „nie porada inwestycyjna”, link do GitHuba. Ostrzeżenie o starych danych później |

Szkic, na którym padły te decyzje, był obrazkiem w rozmowie z 10.10, nie kodem. Liczby na nim
pochodziły z 09.10.

## HTML — co ustaliliśmy, a czego nie

06.10 ustaliliśmy dwie rzeczy:
- **bez pisania JavaScriptu**, bo interaktywność daje Plotly;
- **bez aplikacji na serwerze.**

HTML był w decyzji od początku: plik HTML składa skrypt w Pythonie. Ustalenia „HTML nie ruszamy”
nie było. Ile HTML i CSS napiszemy ręcznie, a ile wygenerują Plotly i pandas, rozstrzygnie
osobna partia.

## Partie (propozycja 10.10, do zatwierdzenia przez Gracjana)

**A. Zawartość i układ**
1. Układ i kolejność sekcji (co widać bez przewijania).
2. Nagłówek (tytuł, podtytuł, znaczek z datą sesji).
3. Kafelki (cena, zmiana, mini-wykres: zakres, oś, kolor).
4. Wykres główny (zakresy, ręczny wybór okresu, dymek po najechaniu, osie, legenda).
5. Ranking (kolumny, kolejność, objaśnienie, format liczb).
6. Stopka (źródło, zastrzeżenie, linki, godzina wygenerowania strony).

**B. Wygląd**

7. Kolory, czcionki, odstępy (kolory spółek, zielony i czerwony, jasny albo ciemny motyw).
8. Telefon (układ na wąskim ekranie).
9. Liczby i daty po polsku (przecinek, „zł”, DD.MM.RRRR, nazwy miesięcy).
10. Dostępność (kontrast, wzrost i spadek nie tylko kolorem, opisy wykresów).

**C. Budowa**

11. HTML i CSS: ile ręcznie, ile z Plotly i pandas, szablon.
12. Skąd dane: Athena albo CSV z S3 `gold/`, które kolumny, czego brakuje.
13. Plotly: biblioteka w pliku albo z sieci (CDN), rozmiar strony.
14. Gdzie i jak się odświeża: plik na laptopie, potem GitHub Pages, GitHub Actions, klucz tylko do
    odczytu, godzina.
15. Co może pójść źle: stare dane, brak danych, zła strona nadpisuje dobrą, koniec AWS 19.02.2027,
    złe ceny Yahoo.
16. Jak sprawdzimy: liczby na stronie = liczby w Athenie, przewidywane przed biegiem.

**D. Później:** zakładki spółek, słownik, wersja angielska, ostrzeżenie o starych danych. Od 13.10
(Gracjan): także zakładki z aktualnościami, danymi spółek i celem projektu, sekcje pod pierwszym
ekranem (opcje, informacje, diagramy, wykresy) i przegląd wyglądu, żeby strona nie wyglądała „jak
z AI”.

## Decyzje z partii

*(Dopisywane po każdej partii.)*

### Partia 1 — układ i kolejność sekcji (10.10)

- **1.1 (b) dwie kolumny na szerokim ekranie**: wykres i kafelki obok siebie, ranking pod nimi.
  Dodatkowo **wykres można rozwinąć na pełny ekran**, gdy ktoś potrzebuje. Sposób rozwinięcia
  ustali partia 4. Uwaga: prawdziwy pełny ekran przeglądarki wymaga kilku linii JavaScriptu,
  a 06.10 ustaliliśmy „bez JavaScriptu”. Bez JavaScriptu da się otworzyć sam wykres jako osobną
  stronę na całe okno. Konsekwencje układu: wykres węższy (ok. 2/3 szerokości), kafelki
  z mini-wykresami w wąskiej kolumnie (ok. 1/3), dwa układy do napisania w CSS (szeroki ekran
  i telefon — partia 8).
- **1.2 (a)** kolejność: nagłówek → kafelki → wykres → ranking → o projekcie → stopka. Przy
  dwóch kolumnach dotyczy kolejności na telefonie i w kodzie strony. Który bok dla kafelków —
  pytanie 1.4.
- **1.3 (a)** krótka sekcja „O projekcie” nad stopką (2–3 zdania o drodze danych i link do
  README). Treść ustali partia 6.
- **Doprecyzowanie Gracjana (10.10):** nie pełny ekran, tylko **znaczne powiększenie panelu
  z wykresem**. **Mini-wykresów w kafelkach nie ma** (zmiana wstępnej decyzji 2: kafelki to cena
  i zmiana dzienna). Zamiast nich **jeden duży wykres po lewej**, na którym da się wybrać, **które
  spółki** pokazać, i **okres** (przyciski zakresu i ręczny wybór, jak w decyzji 1). Szczegóły
  ustali partia 4.
- **1.4 (a)** wykres po lewej (ok. 2/3 szerokości), kafelki po prawej, jeden pod drugim. W kodzie
  strony kafelki stoją przed wykresem, więc na telefonie idą pierwsze.
- **1.5 (b)** ranking w prawej kolumnie, pod kafelkami. Na laptopie cała strona ma się zmieścić na
  jednym ekranie, a kolumny mają być równej wysokości. Tabela jest wąska (ok. 350 pikseli), więc
  wymaga krótkich zapisów — partia 5. Na telefonie kolejność: kafelki → wykres → ranking. Przy
  powiększonym wykresie prawa kolumna zjeżdża pod spód.

**Partia 1 zamknięta 10.10.** Układ: nagłówek na całą szerokość; pod nim po lewej wykres (wybór
spółek i okresu, powiększenie), po prawej trzy kafelki i ranking; niżej „O projekcie” i stopka.

### Partia 2 — nagłówek (10.10, zamknięta)

- **2.1 (a)** tytuł „GPW Pulse”.
- **2.2 (a)** podtytuł „Kursy zamknięcia trzech spółek z GPW, aktualizowane w każdy dzień sesji
  wieczorem”.
- **2.3** treść **(a)** „Dane z sesji: piątek, 09.10.2026” — z dniem tygodnia (format daty:
  partia 9); kolor **zielony** (wybór Gracjana wbrew rekomendacji „szary”). Świadomy koszt:
  dopóki nie ma ostrzeżenia o starych danych (wstępna decyzja 6, „później”), znaczek jest zielony
  także wtedy, gdy potok stoi. Przy ostrzeżeniu o starych danych naturalne będzie przełączenie
  znaczka na żółty.
- **2.4 (b)** napis na karcie przeglądarki krótki — „GPW Pulse” — **z ikonką** (ikonka: partia 7).
  Gracjan dopuszcza inny napis, jeśli padnie lepszy pomysł.
- **2.5 (a)** link do GitHuba tylko w stopce i w „O projekcie”; nagłówek bez ikonki GitHuba.

### Partia 3 — kafelki (10.10)

- **3.1 (a)** cena, zmiana w zł i w % (względem poprzedniej sesji), strzałka; dwie linie.
  Zmiana w % jest w Goldzie (`zmiana_proc`), zmiana w zł z dwóch ostatnich cen.
- **3.2 (a)** wzrost i spadek: kolor, strzałka i znak +/−.
- **3.3 (a)** zmiana zero: szara, strzałka pozioma, „0,00 zł (0,00%)”.
- **3.4 (a)** kolejność stała, alfabetycznie: Cyber_Folks, Synektik, XTB (jak legenda wykresu).
- **3.5 (a)** pasek w kolorze spółki z lewej strony kafelka. **Kolory spółek według ich logo**
  (prośba Gracjana). Odczytane z plików logo 10.10 (średnia pikseli): Cyber_Folks żółty `#FECD01`
  (i grafit `#404035`), Synektik granat `#153055`, XTB czerwony `#F8313E`. Propozycja poprawek pod
  czytelność — do decyzji (K1–K3 w rozmowie z 10.10).
- **3.6** (klikalny kafelek) — czeka na odpowiedź. *(Rozstrzygnięte w partii 4: 3.6 (b).)*
- **Poprawka 12.10 (kafelki od nowa, uwaga 1 z 10.10).** Szkic: plansze w Artifact „GPW Pulse – kafelki
  i motyw” (jasny i ciemny, dane z 09.10 oraz stany spadek / bez zmiany / wzrost). Kafelek: pierwsza
  linia — nazwa i skrót (przy XTB bez powtórzenia skrótu) oraz cena; druga linia — „względem 08.10”
  i zmiana ze strzałką. Kafelek to prawdziwy przycisk z jawnie ustawionym kolorem tekstu i tła.
  - **3.7 (tak)** napisy czytelne na obu tłach (ocena Gracjana na szkicu). Kontrast policzony
    przez Claude'a: tekst na kartach co najmniej 5,1 : 1 na jasnym, 6,4 : 1 na ciemnym (norma 4,5 : 1).
    Claude szkicu sam nie oglądał (panel przeglądarki niezalogowany do claude.ai).
  - **3.8 (a)** dopisek „względem DD.MM” (dzień poprzedniej sesji) zostaje.
  - Paleta szkicu (do zatwierdzenia w partii 7): jasny — tło `#F4F5F7`, karta `#FFFFFF`, ramka
    `#DDE1E6`, tekst `#16191F`, tekst drugi `#555D6B`, wzrost `#1A7F37`, spadek `#C4202C`;
    ciemny — tło `#15171C`, karta `#1E2129`, ramka `#2E333D`, tekst `#E8EAED`, tekst drugi
    `#A3AAB6`, wzrost `#4AC26B`, spadek `#FF7B72`. Zero w kolorze tekstu drugiego.

### Partia 4 — wykres główny, część 1: styl i kolory (10.10)

Gracjan: wykres to jeden z najważniejszych aspektów strony; ma wyglądać profesjonalnie,
na jasnym i ciemnym tle, linie nie „wąskie i bezwyrazowe”. Pokazane trzy style (Plotly.js, dane do
18.09, co piąta sesja): A czysty z metkami, B z wypełnieniem, C wyrazisty z suwakiem i obwódką.

- **W1 (a) styl A**: linie 2,5 px, tylko poziome linie siatki, metka z ostatnią ceną na końcu
  każdej linii (`SNT 352,60`), wspólny dymek dla trzech spółek, przyciski okresu. Dodatkowo:
  - **legenda (nazwy spółek z kolorami) wyżej**, na równi z przyciskami okresu;
  - **suwak okresu**, ale lepszy niż wbudowany suwak Plotly ze stylu C;
  - **pola wyboru dat** („od”, „do”) w panelu wykresu;
  - w legendzie „XTB” zamiast „XTB XTB”.
- **W2 (a) kolory, bez obwódki:**

  | Spółka | Logo | Jasne tło | Ciemne tło |
  |---|---|---|---|
  | Cyber_Folks | `#FECD01` | `#F2BC00` (1,75 : 1) | `#FECD01` (11,9 : 1) |
  | Synektik | `#153055` | `#24508F` (8,0 : 1) | `#7AA2E3` (6,9 : 1) |
  | XTB | `#F8313E` | `#F8313E` (3,8 : 1) | `#FF5A64` (5,9 : 1) |

  Tła w szkicu: jasne `#FFFFFF`, ciemne `#15171C`. Wszystkie pary rozróżnialne przy daltonizmie
  (sprawdzone wzorami narzędzia do palet, 10.10). **Świadomy koszt:** Cyber_Folks na jasnym tle ma
  kontrast 1,75 : 1, poniżej normy 3 : 1 dla linii; ratują go metka z ceną, legenda i dymek.
- **K3 (a)** czerwony XTB zostaje jako pasek i linia, nigdy jako kolor tekstu; spadek zawsze ze
  strzałką i minusem.
- **J1 (a) JavaScript dopuszczony**: jeden mały, osobny plik, pisze go Gracjan z pełną instrukcją
  od podstaw (zmiana decyzji „bez JavaScriptu” z 06.10). Koszt: nowy język, ok. 1–2 sesje więcej.
- **J2 — jak ma działać zmiana okresu (Gracjan):** wykres **nie przybliża się i nie rozciąga**,
  tylko **powstaje od nowa** dla wybranego okresu: dane przycięte do okresu, oś cen dopasowana,
  **metki na końcu wybranego okresu**. Suwak z C był **za gruby** i miał **niepotrzebną miniaturę
  wykresu** — nowy suwak cienki, z dwoma uchwytami, bez miniatury.
- **3.6 (b)** kliknięcie kafelka zostawia na wykresie tylko tę spółkę; drugie kliknięcie wraca do
  trzech.
- Szkic v3 (10.10, Plotly.js, każda sesja do 18.09): legenda i przyciski okresu jako własne
  przyciski HTML w jednym wierszu nad wykresem; zaznaczanie myszą wyłączone (rozciągałoby
  wykres); przy krótkim okresie oś dat pokazuje dzień i miesiąc (`dd.mm`), przy długim miesiąc
  i rok; kafelki klikalne. Logika w szkicu: ok. 60 linii JavaScriptu (wcześniej Claude
  szacował 30 — szkic ma więcej funkcji).
- **M1 (b)** metka: cena i zmiana w wybranym okresie, np. „SNT 352,60 +12,3%”.
- **Z1 (a)** zaznaczanie fragmentu wykresu myszą wyłączone; okres tylko przyciskami, suwakiem
  i polami dat.
- **S1** suwak z v3 „wydaje się ok” (cienki, dwa okrągłe uchwyty, bez miniatury).

**Uwagi Gracjana na koniec sesji 10.10 — do następnej sesji:**
1. **Kafelki z ceną i zmianą % do poprawy** — na jasnym tle napisy w szkicu v3 były praktycznie
   niewidoczne. Przyczyny Claude nie sprawdził (możliwe, że styl przycisków z okna rozmowy
   nadpisał kolory w szkicu); w następnym szkicu kafelki od nowa i sprawdzone na obu tłach.
2. **Motyw strony (jasny/ciemny) przełączany w menu strony, dla całej strony naraz** — nie przy
   wykresie. Zmienia partię 2 (nagłówek dostaje menu albo przełącznik) i partię 7.
3. **Metki do poprawy** — „nie prezentują się do końca zadowalająco”. Co dokładnie — do ustalenia
   na początku następnej sesji, z nowym szkicem.

*Stan uwag 12.10: 1 — zamknięta (poprawka w partii 3); 2 — zamknięta („Motyw strony” niżej);
3 — metki od nowa, osobny szkic w następnej partii.*

**Partia 4, część 2 (12.10, zamknięta poza telefonem).** Szkic: strona „Wykres – metki” w Artifact
„GPW Pulse – szkice strony” (rysunek SVG, nie Plotly; 6 mies. do 18.09 z lokalnego Golda; trzy
wersje metek na obu tłach; działający dymek). Gracjan: „pełna zgoda” z rekomendacjami.
- **M2 (A)** metka to kolorowa plakietka przy prawej krawędzi wykresu, z cienką kreską do końca
  linii: „SNT 352,60 zł +28,4%” (skrót, cena na koniec okresu, zmiana w okresie). Tekst plakietki:
  ciemny `#16191F` na żółtym CBF i czerwonym XTB, biały na granatowym SNT (jasne tło), ciemny na
  wszystkich trzech na ciemnym tle — najsłabszy kontrast 4,6 : 1 (XTB, jasne tło). Plakietki
  rozsuwane w pionie, gdy końce linii są bliżej niż ok. 28 px. Na końcu linii kropka z obwódką w kolorze
  karty.
- **D1 (a)** dymek: dzień tygodnia i data („piątek, 18.09.2026”), pod spodem trzy wiersze — kropka
  w kolorze spółki, nazwa, cena — w kolejności alfabetycznej jak kafelki; pionowa przerywana linia
  i kropki na liniach w miejscu kursora; dymek przeskakuje na lewą stronę kursora przy prawej
  krawędzi.
- **O1 (a)** osie: liczby bez „zł”, „zł” raz nad osią; siatka tylko pozioma, co 50 zł (przy
  innych okresach krok dobierany do zakresu — szczegół w kodzie); miesiące skrótem pod osią
  („kwi”, „maj”…; format: partia 9).
- **P1 (a)** powiększenie: przycisk ze strzałkami w prawym górnym rogu panelu; panel zajmuje całą
  szerokość strony, prawa kolumna zjeżdża pod spód, wykres robi się wyższy; drugie kliknięcie albo
  Esc wraca. (Do JavaScriptu Gracjana.)
- **W1 (tak)** wysokość wykresu = wysokość prawej kolumny (kafelki + ranking), nie mniej niż ok.
  420 px (wynika z 1.5).

**Partia 4 — co jeszcze otwarte:** zachowanie na telefonie (z partią 8).

### Partia 5 — ranking (12.10, zamknięta)

Szkic: strona „Ranking” w Artifact „GPW Pulse – szkice strony” (trzy wersje na obu tłach, szerokość
prawej kolumny 400 px, liczby z biegu 12.10). Gracjan: „pełna zgoda” z rekomendacjami.
- **R1 (A)** tabela w prawej kolumnie pod kafelkami: miejsce, nazwa z kolorową kreską (kolor spółki),
  zmiana (zielona przy wzroście), najbardziej zmienny pełny miesiąc. Nagłówek „Ranking”, obok
  „zmiana od 14.08.2023”. Najniższa z trzech wersji (strona ma się mieścić na jednym ekranie).
- **R2 (a)** kolejność malejąco po zmianie od 14.08.2023, z miejscami 1–3 (12.10: SNT, XTB, CBF).
- **R3 (a)** zapis zmiany „+401,4%” (jedno miejsce po przecinku).
- **R4 (a)** przy miesiącu bez liczby (odchylenia nie pokazujemy).
- **R5 (a)** pod tabelą dwa zdania: „Zmiana: od pierwszego notowania w danych (14.08.2023) do
  ostatniej sesji. Najbardziej zmienny miesiąc: pełny miesiąc, w którym dzienne zmiany ceny były
  najbardziej rozrzucone (odchylenie standardowe).”
- Dane z Golda: `zmiana_caly_okres`, `miesiac` (kolumny `gold_ranking_spolek`); miesiąc zapisany
  słownie („czerwiec 2025” — format: partia 9).

### Partia 6 — „O projekcie” i stopka (12.10)

- **6.1 (c)** opis słowny i pod nim łańcuch techniczny. Gracjan: opis **formalny** (bez potocznych
  słów) i **dokładniejszy** — cała droga danych z Producentem, Konsumentem, Pythonem. Tekst zatwierdzony
  (wersja 2 z poprawką Gracjana o kompakcji) poniżej. Sekcja jest dłuższa niż 2–3 zdania z 1.3 — stoi
  pod główną częścią strony, więc nie psuje zasady „jeden ekran” z 1.5. Etap 5 opisuje stronę
  w ustalonej postaci — prawdziwy dopiero razem z kodem strony.

  > **O projekcie**
  >
  > GPW Pulse jest projektem edukacyjnym z zakresu inżynierii danych. Strona prezentuje kursy
  > zamknięcia trzech spółek notowanych na Giełdzie Papierów Wartościowych w Warszawie (Cyber_Folks,
  > Synektik i XTB) od 14 sierpnia 2023 r. Dane są aktualizowane w każdy dzień sesji, w następujących
  > etapach (godziny według czasu polskiego):
  >
  > 1. **Pobranie danych (18:00).** Program Producenta, napisany w języku Python i uruchamiany przez
  >    harmonogram `cron` na serwerze Amazon EC2, pobiera notowania z serwisu Yahoo Finance.
  >    Notowania nieobecne we wcześniej zapisanych danych wysyła jako wiadomości do brokera Apache
  >    Kafka, działającego na tym samym serwerze. Zapis lokalny jest aktualizowany dopiero po
  >    potwierdzeniu odbioru wiadomości przez brokera.
  > 2. **Zapis danych źródłowych.** Program Konsumenta, również w języku Python, odczytuje wiadomości
  >    z Kafki i zapisuje je jako pliki JSON w magazynie Amazon S3. Odczyt jest zatwierdzany w Kafce
  >    dopiero po udanym zapisie, co zapobiega utracie danych. Raz w miesiącu skrypt kompakcji
  >    w języku Python, uruchamiany ręcznie, przepisuje dane z zakończonego miesiąca do formatu
  >    Parquet (warstwa *bronze*).
  > 3. **Oczyszczenie i obliczenia (18:10).** Zapytanie SQL w usłudze Amazon Athena łączy dane
  >    historyczne z bieżącymi i usuwa powtórzone notowania (warstwa *silver*). Następnie biblioteka
  >    pandas oblicza dzienne zmiany procentowe oraz ranking spółek. Wyniki są zapisywane w Amazon S3
  >    jako pliki CSV (warstwa *gold*).
  > 4. **Kontrola (18:30).** Skrypt kontrolny weryfikuje zapis przebiegu oraz tabelę wynikową
  >    w Athenie, w tym obecność notowania z bieżącej sesji i jednakową liczbę dni dla wszystkich
  >    spółek. Wynik jest przekazywany do zewnętrznej usługi monitorującej, która w razie
  >    nieprawidłowości wysyła powiadomienie e-mail.
  > 5. **Publikacja.** Strona jest statycznym plikiem HTML, generowanym skryptem w języku Python na
  >    podstawie danych z warstwy *gold*. Wykres jest tworzony w bibliotece Plotly.
  >
  > Pełny opis architektury, wyników sprawdzeń oraz znanych ograniczeń znajduje się w pliku README
  > w repozytorium GitHub.
  >
  > *Yahoo Finance → Producent (Python) → Apache Kafka → Konsument (Python) → Amazon S3 → Amazon
  > Athena (SQL) → pandas → strona (Plotly)*
- **6.2 (a)** „Dane: Yahoo Finance. Część cen sprawdzona ręcznie z archiwum notowań GPW.”
- **6.3 (a)** „To nie jest porada inwestycyjna. Dane mogą zawierać błędy i opóźnienia.”
- **6.4 (a)** w stopce godzina wygenerowania strony („Strona wygenerowana: poniedziałek, 12.10.2026,
  18:12”); pod nią podepnie się kiedyś ostrzeżenie o starych danych.
- **6.5 (a)** podpis: login GitHub z linkiem (bez imienia i nazwiska).
- Do partii 15: nie sprawdzone, czy warunki Yahoo pozwalają pokazywać dane na publicznej stronie.

### Motyw strony — jasny i ciemny (12.10, uwaga 2 z 10.10)

Przełącznik dla całej strony, w nagłówku po prawej (zmienia partię 2), nie przy wykresie.
- **T1 (b)** sama ikonka (słońce albo księżyc), bez napisu. Na szkicu były dwa przyciski
  z napisami „Jasny / Ciemny” — do przerysowania.
- **T4 (a)** ikonka pokazuje motyw, na który się przełączy (księżyc na jasnym, słońce na
  ciemnym), z opisem „Przełącz na ciemny” / „Przełącz na jasny” po najechaniu i dla czytników
  ekranu.
- **T2 (a)** przy pierwszym wejściu motyw taki, jaki ma ustawiony komputer albo telefon
  odwiedzającego.
- **T3 (a)** przeglądarka odwiedzającego zapamiętuje wybór na następne wejście.
- Koszt: T2 i T3 to kilka linii JavaScriptu więcej w pliku Gracjana (odczyt ustawienia systemu,
  zapis i odczyt wyboru w przeglądarce). Nowe pojęcia wejdą do pełnej instrukcji przed kodem.

### Partia 7 — kolory, czcionki, odstępy, ikonka (13.10)

Szkic: strona „Cała strona – kolory, czcionki” w Artifact „GPW Pulse – szkice strony” (cała strona na
obu tłach, trzy czcionki, trzy ikonki w 16, 32 i 64 px).
- **7.1 (a)** kolory całej strony jak na szkicu (paleta zapisana w partii 3, „Paleta szkicu”, plus
  znaczek z datą: jasny `#DCF3E2` / `#14622B`, ciemny `#183323` / `#7EE29A`; linki: jasny `#1D4F91`,
  ciemny `#8AB4F8`, kontrast 8,1 i 7,6 : 1).
- **7.2 (B) Source Sans 3** (wbrew rekomendacji IBM Plex Sans). Dodatkowo, prośba Gracjana: w kafelku
  **mniejszy odstęp między wierszami** (cena a zmiana, nazwa a „względem”), kafelek bardziej zbity.
  Szkic 13.10: wysokość wiersza 1,15 rozmiaru czcionki (wcześniej domyślna czcionki) i odstęp między
  wierszami 2 px (wcześniej 5 px); porównanie „przed i po” na osobnej planszy. **Zatwierdzone 13.10**
  („wydaje mi się, że jest ok”).

**Partia 7 zamknięta 13.10.**
- **7.3 (a)** odstępy 12 i 24 px, rogi 10–12 px, bez cieni.
- **7.4 (A)** ikonka na karcie przeglądarki: linia pulsu.

**Uwagi Gracjana 13.10 na później** (nie zmieniają partii 1–7, „wszystko w swoim czasie”):
1. Strona będzie jeszcze modyfikowana, żeby **nie wyglądała „jak z AI”**, tylko bardziej naturalnie.
   Ustalenia z partii 1–7 zostają jako punkt wyjścia.
2. **Nie wszystko na jednym ekranie:** na pierwszym ekranie najważniejsze informacje (jak w 1.5), a niżej,
   po przewinięciu, kolejne opcje, informacje, diagramy i wykresy.
3. **Zakładki:** informacje o spółkach, aktualności, dane spółek, słownik, cel projektu i inne. Rozszerza
   punkt D („Później”).

## Powiązane notatki

- [[Plan-06-domkniecie-i-strona]] — wątek 4, pomysł z 01.09
- [[Przeglad-2026-10-08-calosc]] — decyzja 7: kod strony po naprawach 1 i 2
