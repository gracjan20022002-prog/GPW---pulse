# Notatka projektowa — pełne miesiące w rankingu

Napisana 12 września 2026, **przed kodem**, zgodnie z zasadą numer 10
z `CLAUDE.md`. Kolejność jest taka: Gracjan czyta, zatwierdza albo
zmienia decyzje, dopiero potem pisze kod. Ta notatka niczego nie
przesądza.

Dotyczy jednego miejsca: kolumny „najbardziej zmienny miesiąc"
w `gold/ranking.csv`, liczonej w `kod/gold.py` w liniach 13–15.
To punkt 9 z dziesięciu w kolejności napraw z przeglądu z 8 września,
wzięty **poza kolejnością** decyzją Gracjana z 11 września.

---

## 1. Co Gold liczy dziś

Trzy linie, jedna po drugiej:

```
gold["max_zmienny_miesiac"] = gold["data"].dt.to_period("M")
zmiana_msc = gold.groupby(["spolka", "max_zmienny_miesiac"])["zmiana_proc"].std().reset_index().sort_values(by="zmiana_proc", ascending=False)
sp_rank = zmiana_msc.groupby("spolka").head(1).merge(calk_zmiana, on="spolka")
```

Po kolei, zwykłymi słowami.

**Linia pierwsza** dokłada do każdego wiersza kolumnę z miesiącem tego
wiersza. `dt.to_period("M")` bierze pełną datę i zostawia z niej sam
rok i miesiąc: z `2026-09-11` robi `2026-09`. Słowo `period` znaczy
„okres" i jest osobnym typem w pandas — nie tekstem i nie datą, tylko
przedziałem czasu.

**Linia druga** dzieli wiersze na kubełki po spółce i miesiącu, a
w każdym kubełku liczy **odchylenie standardowe** dziennej zmiany
procentowej. Odchylenie standardowe to miara rozrzutu: mówi, jak
daleko od średniej leżą typowe wartości. Duże odchylenie znaczy, że
kurs skakał; małe, że szedł spokojnie. Potem układa wszystko od
największego odchylenia do najmniejszego.

**Linia trzecia** bierze z każdej spółki pierwszy wiersz po tym
sortowaniu, czyli jej miesiąc o największym rozrzucie, i dokleja do
niego kolumny o zmianie za cały okres.

Efekt na dziś, prosto z pliku:

| spółka | miesiąc | odchylenie |
|---|---|---|
| SNT.WA | 2025-06 | 4,087 |
| CBF.WA | 2024-11 | 3,915 |
| XTB.WA | **2026-09** | 3,772 |

---

## 2. Co z tym jest nie tak — zmierzone dzisiaj

Wszystkie liczby w tej sekcji policzyłem 12 września z pliku
`silver/clean_data.csv`, nie z pamięci.

**Dane obejmują 38 miesięcy**, od `2023-08` do `2026-09`. Wszystkie
trzy spółki mają dokładnie te same 770 dni notowań — porównałem zbiory
dat parami i różnic jest zero. Dziury w danych dziś nie ma **u żadnej
spółki**. To ważne, bo część rozważań niżej dotyczy dziury, której
jeszcze nie mamy.

**Dwa z tych 38 miesięcy to kikuty**, czyli miesiące, z których mamy
tylko kawałek:

| miesiąc | dni notowań | dlaczego niepełny |
|---|---|---|
| `2023-08` | 13 | historia zaczyna się 14 sierpnia |
| `2026-09` | 9 | miesiąc trwa |
| pozostałe 36 | od 18 do 23 | pełne |

Najkrótszy pełny miesiąc ma 18 dni notowań, najdłuższy 23. Między
najdłuższym kikutem (13) a najkrótszym pełnym miesiącem (18) jest
wyraźna przerwa i nic w niej nie leży. To się przyda przy decyzji
pierwszej.

**Kikut wrześniowy dziś wygrywa u XTB**, mając 9 dni przeciwko
dwudziestu paru. Trzy odczyty tej samej komórki z trzech dni:

| dzień odczytu | co pokazywał XTB |
|---|---|
| 8 września | `2026-09` |
| 10 września | `2025-01` |
| 11 września | `2026-09`, odchylenie 3,77 wobec 3,70 dla stycznia 2025 |

Wystarczył jeden mocniejszy dzień XTB, skok ze 144,34 na 148,50, żeby
niedokończony wrzesień przeskoczył pełny styczeń i wrócił na pierwsze
miejsce.

**Czego nie sprawdziłem:** jakie odchylenie ma kikut z sierpnia 2023
i którym byłby w kolejce. Nie liczyłem tego. Wiem tylko, że dziś nie
wygrywa u żadnej z trzech spółek, bo zwycięzcy to `2025-06`, `2024-11`
i `2026-09`.

---

## 3. To są dwie różne wady, nie jedna

Przegląd z 8 września opisywał jedną rzecz: bieżący miesiąc ma za mało
dni. Po policzeniu dni w każdym miesiącu widać, że są to **dwa osobne
problemy z dwiema różnymi przyczynami**, i że każdy potrzebuje innej
reguły.

**Wada pierwsza: miesiąc, który jeszcze trwa.** Wrzesień 2026 rośnie
z dnia na dzień. Każdy nowy dzień zmienia jego odchylenie, więc
odpowiedź na pytanie „który miesiąc był najbardziej zmienny" zmienia
się razem z nim. To jest **przyczyna migotania**. Czytelnik strony
zobaczy liczbę, która zmienia się bez powodu widocznego z zewnątrz.

**Wada druga: kikut na początku historii.** Sierpień 2023 ma 13 dni
i już nigdy nie będzie miał więcej. On **nie migocze** — jest stały.
Ale startuje w tym samym wyścigu co miesiące dwudziestodniowe, mimo że
opiera się na znacznie mniejszej próbce.

Rozróżnienie ma praktyczny skutek. Gdybyśmy naprawili to jedną regułą
„miesiąc musi mieć co najmniej piętnaście dni notowań", to wrzesień
wypadłby dziś (9 dni), ale **wróciłby około dwudziestego pierwszego
września**, gdy uzbiera piętnasty dzień. I od tego dnia do końca
miesiąca znowu by migotał. Reguła progowa przesuwa migotanie na koniec
miesiąca zamiast je usunąć.

Dlatego proponuję dwie reguły, każda do swojego zadania. Szczegóły
w decyzji pierwszej.

---

## 4. Kształt na innych danych

Lodziarnia „Zimny Kubek" zapisuje dzienną sprzedaż. Interesuje nas
miesiąc, w którym sprzedaż najbardziej skakała z dnia na dzień. Liczymy
to tak samo: dzienna zmiana w procentach, potem odchylenie standardowe
w każdym miesiącu.

### Kikut wygrywa

Wejście, dzienne zmiany w procentach:

| miesiąc | dzienne zmiany | dni |
|---|---|---|
| 2026-04 | +20, −20 | 2, bo zapisy zaczęto 29 kwietnia |
| 2026-05 | dwadzieścia dni, spokojnie | 20 |
| 2026-06 | +15, −15 | 2, bo dziś jest 2 czerwca |

Wyjście dzisiejszego kodu:

```
sklep         miesiac   odchylenie
Zimny Kubek   2026-04   28,28
```

Odchylenie z dwóch liczb +20 i −20 wynosi 28,28. Odchylenie z dwudziestu
spokojnych dni maja wyszło 5,48. Dwudniowy kikut z kwietnia wygrywa
z pełnym majem pięciokrotnie, i to nie dlatego, że kwiecień był
ciekawy, tylko dlatego, że dwie liczby zawsze leżą daleko od swojej
średniej.

Wyjście po naprawie, gdy kwiecień i czerwiec wypadają z wyścigu:

```
sklep         miesiac   odchylenie   dni
Zimny Kubek   2026-05   5,48         20
```

### Migotanie, dzień po dniu

Teraz to samo, ale patrzymy na czerwiec przez trzy kolejne dni. Maj
stoi na 9,00 i się nie zmienia, bo się skończył.

| dzień | zmiany w czerwcu | odchylenie czerwca | kto wygrywa |
|---|---|---|---|
| 2 czerwca | +7, −7 | 9,90 | czerwiec |
| 3 czerwca | +7, −7, 0 | 7,00 | maj |
| 4 czerwca | +7, −7, 0, +14 | 9,04 | czerwiec |

Trzy dni, trzy odczyty, dwie zmiany zdania. Nikt nie ruszał kodu ani
starych danych. To dokładnie to, co XTB zrobiło między ósmym
a jedenastym września.

Rachunek do sprawdzenia na piechotę, żeby nie trzeba było wierzyć na
słowo. Dla dwóch liczb +7 i −7 średnia wynosi zero, odległości od
średniej to 7 i −7, ich kwadraty 49 i 49, suma 98. Dzielimy przez
liczbę wartości mniej jeden, czyli przez 1, i pierwiastkujemy: 9,90.
Po dołożeniu zera suma kwadratów zostaje 98, ale dzielimy już przez 2,
więc wychodzi 7,00.

Widać z tego coś, co warto zapamiętać: **dołożenie jednego spokojnego
dnia potrafi zbić odchylenie o jedną trzecią**, gdy dni jest mało. Przy
dwudziestu dniach jeden dzień prawie nic nie zmienia. Stąd bierze się
cała ta wada.

---

## 5. Decyzje do podjęcia przed kodem

### Decyzja 1 — co znaczy „miesiąc, który się liczy"

**Możliwość A: próg dni notowań.** Miesiąc wchodzi do wyścigu, jeśli ma
co najmniej piętnaście dni notowań. Próg leży w przerwie między
najdłuższym kikutem (13) a najkrótszym pełnym miesiącem (18), więc dziś
odcina dokładnie to, co trzeba.

- Za: jedna linia kodu, jedna liczba, łatwo wytłumaczyć czytelnikowi.
- Za: łapie **dziurę w danych**. Gdyby Atena kiedyś oddała pół tabeli
  albo spółka stanęła na trzy tygodnie, miesiąc z sześcioma dniami
  wypadnie sam.
- Przeciw: **nie usuwa migotania**, tylko przesuwa je na trzecią
  dekadę miesiąca, tak jak opisano w sekcji 3.

**Możliwość B: pierwszy i ostatni miesiąc historii spółki poza
wyścigiem.** Liczymy dla każdej spółki jej najwcześniejszy
i najpóźniejszy miesiąc w danych i oba wyrzucamy.

- Za: **kasuje migotanie całkowicie**. Miesiąc wchodzi do rankingu
  dopiero wtedy, gdy nie może już urosnąć, więc jego odchylenie jest
  ostateczne.
- Za: żadnej wymyślonej liczby, reguła sama się dostraja do danych.
- Za: kształt kodu jest bliźniaczo podobny do tego, co w Goldzie już
  stoi. Linia 9 robi `groupby("spolka")["cena"].agg(["first", "last"])`
  i dokleja wynik przez `merge`. Tutaj byłoby to samo, tylko `min`
  i `max` na kolumnie z miesiącem.
- Przeciw: gubi pierwszy miesiąc nawet wtedy, gdy historia zaczęła się
  akurat pierwszego dnia miesiąca. Koszt: jeden miesiąc z 38.
- Przeciw: nie widzi dziury w środku.

**Możliwość C: obie naraz.** Miesiąc liczy się, jeśli nie jest ani
pierwszym, ani ostatnim miesiącem historii spółki, **i** ma co najmniej
piętnaście dni notowań.

**Rekomendacja: możliwość C.** Każda połowa ma inne zadanie i żadna nie
zastąpi drugiej. Reguła „pierwszy i ostatni" zamyka migotanie, czyli tę
wadę, dla której robimy dzisiejszą sesję. Próg dni pilnuje dziury,
której dziś nie ma, ale która jest wprost wymieniona w zasadzie 10
z `CLAUDE.md` jako rzecz do przewidzenia — „Atena zwraca pół tabeli".
Dodatkowo próg da się sprawdzić już dziś, podkręcając go na chwilę do
dwudziestu pięciu; opisuję to w teście trzecim.

### Decyzja 2 — co pokazać spółce, której nie zostanie ani jeden miesiąc

**Poprawka do pierwszej wersji tej notatki, wniesiona przez Gracjana
12 września.** Napisałem tu najpierw, że czwarta spółka przez dwa
miesiące będzie miała same kikuty. To nieprawda. Producent pyta Yahoo
o `range=3y` przy **każdym** biegu, a spółka bez pliku pamięci ma pusty
zbiór `stare_daty`, więc wszystkie mniej więcej 750 dni liczy jako nowe
i wszystkie wysyła do Kafki. Nowa spółka wchodzi z trzema latami
historii od pierwszego biegu, nie z dwoma dniami.

Zostaje z tego przypadek dużo węższy: **spółka notowana od niedawna**,
na przykład po debiucie sprzed miesiąca. Wtedy Yahoo samo nie ma nic
starszego, niezależnie od tego, o jaki zakres poprosimy.

#### Dwie rzeczy, które wyszły przy tym pytaniu

**Nowa spółka jest zatrzymywana wcześniej i głośno.** Athena nie widzi
nowej partycji `live/spolka=NOWA/`, dopóki ktoś nie uruchomi `MSCK
REPAIR TABLE live;` albo crawlera — to punkt 2.4 przeglądu, dokładnie
to zablokowało XTB i SNT 25 sierpnia. Do tego czasu Silver nie znajdzie
nowej spółki w wyniku zapytania i przerwie na `assert` z linii 20, bo
zbiór spółek w danych nie zgadza się z listą z `config.py`. Gold przez
`&&` w ogóle nie wystartuje. Znaczy to, że „nowa spółka nie dojechała"
jest już dziś awarią głośną, a decyzja 2 dotyczy tylko sytuacji „spółka
dojechała, ale ma za krótką historię".

**Okna nie są równe i to jest osobna, nowa obserwacja.** `range=3y`
liczy się wstecz od **dnia zapytania**. Trzy obecne spółki mają dane od
14 sierpnia 2023, a trzy lata wstecz od dzisiaj to 12 września 2023.
Spółka dodana dzisiaj zaczynałaby więc historię mniej więcej miesiąc
później niż pozostałe. Dla rankingu miesięcznego to bez znaczenia, bo
miesiące każdej spółki są oceniane osobno. Dla kolumny
`zmiana_caly_okres` znaczenie ma duże, bo ta kolumna po cichu zakłada,
że wszystkie spółki mierzymy w tym samym oknie. **Nie sprawdziłem**,
dlaczego obecna historia zaczyna się akurat 14 sierpnia 2023, a nie
trzy lata przed pierwszym biegiem projektu — to osobne pytanie.

**Możliwość A: zostaje jak jest.** `groupby("spolka").head(1)` po prostu
nie zwróci dla niej wiersza, a `merge` go nie dorobi. Spółka **zniknie
z rankingu bez śladu**. To cicha awaria, a zasada 9 punkt c mówi, że
awaria ma być głośna.

**Możliwość B: spółka zostaje, bez miesiąca.** Zmieniamy `merge` tak,
żeby zachował wszystkie spółki z tabeli `calk_zmiana`, czyli dodajemy
`how="right"`. Spółka dostaje wiersz z pustą kolumną miesiąca. Zmiana za
cały okres i tak się dla niej liczy, bo do tego wystarczą dwa dni.

**Rekomendacja: możliwość B, ale z uczciwym uzasadnieniem.** Po
poprawce wyżej ta ścieżka nie broni już przed „każdą nową spółką",
tylko przed spółką po świeżym debiucie. To przypadek rzadki. Zostaję
przy niej, bo kosztuje jedno słowo w linii, którą i tak przepisujemy,
a brak wiersza jest nieodróżnialny od błędu. Przy okazji poznajesz
`how=` w `merge`, czyli sterowanie tym, które wiersze przeżywają
sklejenie. Gdybyś wolał nie dokładać kodu pod rzadki przypadek, to
uzasadniony wybór — wtedy spółka bez pełnego miesiąca po prostu znika
z rankingu, a test trzeci pokaże plik z samym nagłówkiem.

### Decyzja 3 — co ze zmianą z pierwszego dnia miesiąca

Dzienna zmiana pierwszego dnia miesiąca jest liczona **względem
ostatniego dnia poprzedniego miesiąca**, bo `pct_change` patrzy o jeden
wiersz wstecz i nie zna granic miesiąca. Odchylenie każdego miesiąca
zawiera więc jeden skok przez granicę.

**Rekomendacja: zostawiamy tak, jak jest.** Ta zmiana naprawdę
wydarzyła się tego dnia, więc należy do tego miesiąca. Wyrzucenie jej
byłoby stratą prawdziwej informacji i dodatkową linią kodu. Ważniejsze:
dzisiejsza zmiana ma ruszyć **jedną rzecz**, żeby dało się ją
sprawdzić. Przy okazji drobiazg: pierwszy wiersz całej historii spółki
ma w tej kolumnie `NaN`, bo nie ma się do czego odnieść, a `std()`
pomija `NaN` po cichu.

### Decyzja 4 — czy Gold ma powiedzieć, ile miesięcy odrzucił

**Możliwość A: nic nie wypisuje.** Reguła działa niewidocznie.

**Możliwość B: jedna linia** z dwiema liczbami: ile wierszy miała
tabela miesięczna przed odsianiem i ile po.

**Poprawka do pierwszej wersji tej notatki, 12 września.** Napisałem
tu najpierw „38 i 36". To są liczby **miesięcy**, a tabela miesięczna
ma jeden wiersz na **parę spółka-miesiąc**, czyli trzy razy tyle.
Prawidłowe liczby to **114 przed odsianiem i 108 po**. Rachunek: trzy
spółki razy 38 miesięcy daje 114, a po wyrzuceniu pierwszego
i ostatniego miesiąca każdej spółki zostaje trzy razy 36, czyli 108.
Próg piętnastu dni nie usuwa nic ponadto, bo wszystkie pozostałe
miesiące mają od 18 do 23 dni.

**Rekomendacja: możliwość B.** Bez tej linii nie da się z zewnątrz
odróżnić „reguła odrzuciła dwa kikuty" od „reguła odrzuciła wszystko
i ranking liczy się z resztek". Jedna liczba zamienia niewidoczne
w sprawdzalne.

**Skutek uboczny do przewidzenia:** blok wieczornego biegu w logu na
EC2 urośnie o tę linię, z 23 do 24. Dziś wieczorem potwierdzamy
podsumowanie Producenta i chcemy mieć blok równo 23-linijkowy, więc
**ranking nie powinien trafić na EC2 dzisiaj**. Nic nas nie goni: na
EC2 wynik Golda i tak kończy na dysku i nikt go nie czyta. Naturalny
termin to poniedziałek, razem z potwierdzeniem `nowych dni 1` na dniu
giełdowym.

### Decyzja 5 — nazwy dwóch mylących kolumn

To żółty punkt 2.6 z przeglądu. Skoro i tak ruszamy linię 13, to jest
moment.

- W `gold/dane_dzienne.csv` kolumna nazywa się `max_zmienny_miesiac`,
  a trzyma **miesiąc danego wiersza**, nie żaden maksymalny. Propozycja:
  `miesiac`.
- W `gold/ranking.csv` kolumna `zmiana_proc` trzyma **odchylenie
  standardowe**, a w `dane_dzienne.csv` ta sama nazwa trzyma dzienną
  zmianę procentową. Dwa różne znaczenia, jedna nazwa. Propozycja:
  `odchylenie`.

**Sprawdziłem, czy coś te nazwy czyta**, zamiast zakładać.
`kod/ranking.py` sięga tylko po `spolka` i `zmiana_caly_okres`.
`kod/wykresy.py` sięga tylko po `data`, `cena` i `spolka`. Żaden z nich
nie dotyka obu zmienianych nazw, więc zmiana nic nie psuje.

**Rekomendacja: zmieniamy obie.** Dziś kosztuje to dwa słowa. Gdy
kolumny trafią na stronę albo do Power BI, będzie to kosztowało
poprawki w kilku miejscach.

---

## 6. Co może pójść źle

**Reguła odetnie za dużo i nikt tego nie zauważy.** Zabezpieczenie:
linia z decyzji 4 i test trzeci.

**Historia zacznie się pierwszego dnia miesiąca i stracimy pełny
miesiąc.** Dziś nie zachodzi, bo dane zaczynają się 14 sierpnia. Gdyby
kiedyś zaszło, kosztem jest jeden miesiąc z kilkudziesięciu. Uznaję to
za cenę do zapłacenia za brak wymyślonej liczby w regule.

**Pierwszego dnia miesiąca ranking się zmieni i będzie wyglądał jak
migotanie.** Pierwszego października wrzesień stanie się zamknięty
i wejdzie do wyścigu, więc odpowiedź może się zmienić. **To jest
poprawne zachowanie, nie awaria.** Zapisuję to tutaj, żeby za trzy
tygodnie nikt nie szukał wady tam, gdzie jej nie ma. Różnica wobec
dzisiejszej wady: po naprawie zmiana może nastąpić najwyżej raz
w miesiącu i z podanego powodu.

**Potok stanie na tydzień.** Najnowszy miesiąc w danych przestanie się
posuwać, więc poprzedni miesiąc zostanie zablokowany dłużej, niż
trzeba. Ranking będzie wtedy o jeden miesiąc uboższy, ale nie
nieprawdziwy.

**Dojdzie czwarta spółka.** Wejdzie od razu z trzema latami historii,
więc werdykt dostanie w pierwszym biegu — pod warunkiem, że ktoś
wcześniej zarejestruje jej partycję w Athenie. Bez tego zatrzyma ją
`assert` w Silverze, głośno. Szczegóły w decyzji 2. Werdyktu nie
dostanie tylko spółka po świeżym debiucie, bo wtedy Yahoo samo nie ma
starszych danych.

**Ktoś przeliczy Golda na starym `clean_data.csv`.** Dostanie inną
odpowiedź niż z pliku bieżącego, bo „ostatni miesiąc historii" będzie
inny. To nie jest nowa wada — dziś jest dokładnie tak samo — ale po
naprawie łatwiej to zrozumieć.

**Miesiąc z dziurą przejdzie próg.** Gdy spółka stanie na tydzień,
miesiąc może mieć 16 dni i wejść do rankingu z niepełną próbką. Próg
piętnastu dni to zabezpieczenie zgrubne, nie dokładne. Do rozważenia
kiedyś: porównanie z liczbą dni notowań u pozostałych spółek.

---

## 7. Jak to sprawdzimy

Wszystkie trzy testy robimy **na laptopie** i żaden nie potrzebuje
giełdy, brokera ani EC2. Dlatego akurat ta naprawa pasuje do soboty.

Stan wyjściowy, policzony dziś przed jakąkolwiek zmianą:

| Co | Wartość dziś |
|---|---|
| `silver/clean_data.csv` | 2310 wierszy, po 770 na spółkę |
| miesięcy w danych | 38, od `2023-08` do `2026-09` |
| ranking SNT | `2025-06`, odchylenie 4,087 |
| ranking CBF | `2024-11`, odchylenie 3,915 |
| ranking XTB | `2026-09`, odchylenie 3,772 |
| `zmiana_caly_okres` SNT / CBF / XTB | 367,797 / 165,873 / 291,407 |

### Test 1 — zwykły bieg Golda po zmianie

**Przewidywanie, zapisane przed uruchomieniem:**

- XTB przestaje pokazywać `2026-09` i pokazuje `2025-01`. Podstawa:
  10 września, gdy wrzesień był chwilowo słabszy, na tym miejscu stał
  właśnie styczeń 2025 z wynikiem 3,70.
- SNT zostaje na `2025-06`, CBF zostaje na `2024-11`. Oba to miesiące
  pełne, więc reguła ich nie dotyka.
- **Trzy kolumny o całym okresie muszą zostać identyczne co do ostatniej
  cyfry.** Zmiana dotyka wyłącznie części miesięcznej. Gdyby ruszyła się
  choć jedna cyfra w `zmiana_caly_okres`, znaczyłoby to, że zmiana
  sięgnęła dalej, niż zamierzaliśmy.
- `gold/dane_dzienne.csv` ma dalej 2310 wierszy. Zmienia się tylko
  nazwa jednej kolumny w nagłówku.
- Nowa linia w wyjściu pokazuje **114 wierszy przed odsianiem i 108
  po**. To pary spółka-miesiąc, nie miesiące: trzy spółki razy 38
  miesięcy.

**Ryzyko tego przewidywania:** nie liczyłem odchylenia dla `2023-08`.
Jeżeli sierpień 2023 miał u XTB odchylenie wyższe niż 3,70, to przy
regule samego progu wyszedłby on, a nie styczeń. Przy rekomendowanej
regule C sierpień 2023 wypada jako pierwszy miesiąc historii, więc
przewidywanie zostaje. Gdyby jednak wyszło coś innego niż `2025-01`,
**pierwsze, co sprawdzamy, to czy nie wygrał właśnie sierpień 2023** —
to byłby znak, że reguła „pierwszy miesiąc" nie zadziałała.

### Wynik testu 1 — wykonany 12 września, zdany

Siedem przewidywań, siedem trafień. Linia w wyjściu pokazała 114 i 108.
XTB przeszło z `2026-09` na `2025-01` z odchyleniem 3,7011990688949696,
a to zgadza się z 3,70 zapisanym dziesiątego września, gdy wrzesień
akurat przegrywał. Dwa odczyty z różnych dni dały tę samą liczbę.
Kolumna `dni` pokazała 19, 20 i 21, zgodnie z policzonymi wcześniej
dniami notowań w listopadzie 2024, czerwcu 2025 i styczniu 2025.

Najmocniejszy dowód leży jednak w liczbach, które **nie** miały drgnąć.
Odchylenia CBF i SNT to w pliku `3.9145458843735463`
i `4.086839347653686`, czyli znak w znak to samo co przed zmianą.
Wszystkie trzy kolumny o całym okresie również bez zmiany choćby
ostatniej cyfry. Porównanie robione w pliku, nie na ekranie, bo pandas
wypisuje sześć miejsc po przecinku i ukryłby różnicę dalej.

**Jedna rzecz zmieniła się poza przewidywaniem i nie jest błędem:**
kolejność wierszy w pliku. Było od największego odchylenia (SNT, CBF,
XTB), jest alfabetycznie (CBF, SNT, XTB), bo przy `how="right"`
kolejność bierze się z prawej tabeli, a ta przyszła z grupowania po
spółce. Gdyby układ od najbardziej zmiennej był potrzebny na stronie,
wymaga jednego sortowania na końcu. Do decyzji kiedy indziej.

### Test 2 — dowód, że migotanie zniknęło

To jest właściwy test dzisiejszej naprawy i najważniejsza rzecz w tej
notatce.

**Pomysł:** skoro po naprawie niedokończony wrzesień ma nie mieć wpływu
na wynik, to usunięcie września z danych **nie może niczego zmienić**.

**Jak:** robimy kopię `silver/clean_data.csv` bez wierszy z datą
`2026-09`, uruchamiamy Golda na kopii i porównujemy oba rankingi.

**Przewidywanie:** oba rankingi identyczne co do ostatniej cyfry,
we wszystkich kolumnach poza `ostatnia_cena` i `zmiana_caly_okres`,
które muszą się różnić, bo one z założenia patrzą na ostatni dzień
danych.

To jest test symulujący upływ czasu bez czekania. Gdyby wynik części
miesięcznej się zmienił, znaczyłoby, że niedokończony miesiąc nadal ma
wpływ, i cała naprawa jest pozorna.

**Rzecz do wiedzenia zawczasu, bo inaczej wynik wygląda na błąd.** Po
usunięciu września ostatnim miesiącem historii staje się sierpień 2026
i to **on** wypada teraz z puli. Z wyścigu znika więc dwa razy po jednym
miesiącu, nie raz. Zwycięzców to nie dotyczy, bo żaden z nich nie jest
sierpniem. Liczby wierszy spadają z 114 i 108 na 111 i 105.

### Pytanie Gracjana i odpowiedź, którą warto zapamiętać

Gracjan zapytał, czy sierpień wypada z wyścigu na stałe, czy tylko na
czas tego testu. Tylko na czas testu. Reguła nie zna kalendarza, tylko
patrzy w dane, i liczy się od nowa przy każdym biegu.

Najprościej myśleć o tym tak: **miesiąc siedzi poza wyścigiem tylko
dopóki może jeszcze urosnąć.** Wykluczenie przesuwa się z czasem jak
kursor, zawsze obejmuje dokładnie jeden miesiąc na końcu danych i nigdy
nie zostaje na stałe. Po biegu w czwartek 1 października ostatnim
miesiącem w danych stanie się październik, wrzesień wejdzie do wyścigu
po raz pierwszy, a sierpień przez cały ten czas się nie ruszy. Jedyne
wykluczenie trwałe to sierpień 2023, bo przed 14 sierpnia 2023 nikt już
nic nie dopisze.

### Wynik testu 2 — wykonany 12 września, zdany

Wszystkie przewidywania trafione: kształt `(2283, 3)`, linia z liczbami
111 i 105, dni 19, 20 i 21 bez zmian, pierwsze ceny bez zmian.
Nowe ostatnie ceny 194,0 dla CBF, 335,0 dla SNT i 184,16 dla XTB,
a zmiana za cały okres 156,613762, 373,163821 i 385,398024 wobec
liczonych na piechotę 156,61, 373,16 i 385,40.

**Rozstrzygające jest to, co się nie zmieniło**, sprawdzone w pliku na
pełnej precyzji:

| Odchylenie | Bieg zwykły | Bieg bez września |
|---|---|---|
| CBF.WA | 3.9145458843735463 | 3.9145458843735463 |
| SNT.WA | 4.086839347653686 | 4.086839347653686 |
| XTB.WA | 3.7011990688949696 | 3.7011990688949696 |

Ani jednej różnej cyfry, mimo usunięcia 27 wierszy danych i wypchnięcia
z puli dodatkowego miesiąca. Część miesięczna przestała zależeć od tego,
ile dni ma miesiąc bieżący. **To jest dowód, dla którego robiliśmy tę
naprawę.**

### Test 3 — próg i ścieżka „za mało danych"

**Jak:** podkręcamy próg z piętnastu na dwadzieścia pięć i uruchamiamy
Golda raz. Dwadzieścia pięć jest wyżej niż najdłuższy miesiąc w danych,
który ma 23 dni, więc **nie przejdzie żaden miesiąc**.

**Przewidywanie:** wszystkie trzy spółki zostają w rankingu, każda
z pustym miesiącem, i widać linię mówiącą, że ze 114 wierszy weszło 0.

Ten jeden bieg sprawdza dwie rzeczy naraz: że próg w ogóle działa,
i że ścieżka z decyzji 2 nie gubi spółek. Potem wracamy próg na
piętnaście i uruchamiamy Golda jeszcze raz, żeby pliki wróciły do stanu
prawidłowego.

### Wynik testu 3 — wykonany 12 września, zdany

Linia w wyjściu pokazała **114 i 0**, czyli próg odrzucił wszystko, tak
jak miał. W rankingu **zostały trzy wiersze**, po jednym na spółkę,
z pustym miesiącem, pustym odchyleniem i pustą liczbą dni, ale
z wypełnionymi cenami i zmianą za cały okres. Gdyby `how="right"` nie
zadziałało, plik miałby sam nagłówek i spółki zniknęłyby bez śladu.

Przy okazji wyszło rozróżnienie warte zapamiętania. W pustych komórkach
pandas wypisał **dwa różne znaki**: `NaT` w kolumnie z miesiącem i `NaN`
w kolumnach liczbowych. `NaT` znaczy „nie ma czasu" i jest znacznikiem
braku dla dat i okresów, `NaN` znaczy „nie ma liczby". Pandas dobiera
znacznik do rodzaju kolumny. W zapisanym pliku CSV obydwa wychodzą jako
puste miejsce.

Po powrocie progu na 15 bieg porządkowy dał znowu 114 i 108, a plik
`ranking.csv` jest znak w znak taki sam jak po pierwszym udanym biegu.
Sprawdzone przez odczytanie pliku.

**Uwaga o porządku dnia:** lokalny Harmonogram Windows uruchamia Silver
i Gold o 18:10 i nadpisze pliki w `silver/` i `gold/`. Testy robimy
przed tą godziną albo z pełną świadomością, że o 18:10 pliki zostaną
przeliczone jeszcze raz. Stan sprzed zmiany jest bezpieczny, bo leży
w gicie w commicie `76b86b6`.

---

## 8. Co to zepsuje za miesiąc

**Opisy w starych notatkach przestaną pasować.** Wpisy dziennika z 8,
10 i 11 września mówią o XTB z wrześniem 2026 na pierwszym miejscu. Po
naprawie będą historią, nie stanem. Przegląd trzeba poprawić w punkcie
2.6 w tej samej sesji, w której kod wejdzie.

**Blok wieczornego biegu w logu urośnie o jedną linię**, gdy ranking
trafi na EC2. Każde liczenie linii po tym dniu musi brać pod uwagę 24,
nie 23.

**Nazwy kolumn w dwóch plikach się zmienią.** Kto miał stary
`ranking.csv` otwarty w arkuszu, zobaczy inną nazwę. Dziś nikt nie ma,
sprawdziłem oba skrypty, które te pliki czytają.

**Pierwszego października ranking się ruszy.** Powód opisany
w sekcji 6. Warto mieć to zapisane, bo tego samego dnia wypada
pierwsza kompakcja z prawdziwym kasowaniem i łatwo będzie zrzucić winę
nie na to, co trzeba.

---

## 9. Czego ta zmiana nie naprawia

- **Wynik dalej kończy na dysku.** `gold/ranking.csv` na EC2 nikt nie
  czyta. To krok 5 z kolejności napraw i dzisiejsza zmiana go nie
  dotyka. Z pięciu warunków „zrobione" ta naprawa spełni cztery;
  piątego, czyli wdrożenia tam, gdzie ma działać, nie spełni dziś
  świadomie, bo odkładamy wgranie na EC2 na poniedziałek.
- **Ranking pokazuje jedną liczbę bez kontekstu.** Nie widać, o ile
  zwycięzca wyprzedził drugiego. Przy XTB różnica wynosiła 3,77 do
  3,70, czyli prawie nic, i to jest informacja, której czytelnik nie
  dostaje. Do rozważenia przy stronie.
- **Nic nie sygnalizuje awarii.** To krok 8.
- **Dziura w danych w środku miesiąca** jest łapana tylko zgrubnie,
  progiem. Opisane w sekcji 6.

---

## Powiązane notatki

- [[Przeglad-2026-09-08-co-nie-gra]] — punkt 2.6 opisuje tę wadę,
  z uzupełnieniem z 11 września o migotaniu; punkt 9 w Części 5 to
  miejsce tej naprawy w kolejności
- [[Notatka-2026-09-11-podsumowanie-w-producencie]] — druga zmiana
  dzisiejszego dnia, ta, która czeka na wieczorny bieg na EC2
- [[Plan-03-gold]] — skąd wzięła się dzisiejsza postać Golda
- [[Slownik]] — odchylenie standardowe, `period`, maska logiczna,
  `how=` w `merge`: do dopisania w tej sesji
