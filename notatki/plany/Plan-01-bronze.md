# Etap 1 — BRONZE, krok po kroku

Data utworzenia: 2026-07-21

---

## Najpierw: co to znaczy „bronze"

Bronze to po angielsku brąz. Nazwa jest umowna — mogłaby być „magazyn surowca".

**Bronze to miejsce, gdzie wrzucasz dane dokładnie takie, jakie przyszły z internetu.
Niczego nie poprawiasz. Niczego nie usuwasz.**

### Dlaczego nie poprawiać od razu?

Wyobraź sobie, że dostajesz paragon ze sklepu. Możesz od razu przepisać go
do zeszytu wydatków — ale paragon wyrzucasz.

Za tydzień okazuje się, że źle przepisałeś jedną kwotę. Paragonu już nie ma.
Nie masz jak sprawdzić.

**Bronze to szuflada z paragonami.** Trzymasz oryginały. Jak się pomylisz
w dalszej obróbce — wracasz do oryginału, zamiast pobierać wszystko od nowa
z internetu.

To jest cała filozofia tej warstwy. Nic więcej.

### Trzy zasady bronze

1. **Zapisuj wszystko** — nawet to, czego teraz nie potrzebujesz
2. **Nie zmieniaj nic** — żadnego poprawiania dat, liczb, nazw
3. **Tylko dopisuj** — nigdy nie kasuj tego, co już zapisałeś

---

## Co konkretnie ma się znaleźć w naszym bronze

### Jakie dane

Ceny akcji **trzech spółek**, dzień po dniu, za ostatnie 2 lata.

Proponuję: **PKN** (Orlen), **PKO** (bank PKO BP), **CDR** (CD Projekt).
Trzy różne branże, więc wykresy będą się różnić i będzie ciekawiej.

Możesz wybrać inne. Tylko trzy — nie trzydzieści. Trzy wystarczą,
żeby program działał, a błędy wychodzą szybciej.

### Jak ma wyglądać zapis na dysku

```
gpw-pulse-v2/
└── dane/
    └── bronze/
        ├── pkn_2026-07-22.csv
        ├── pko_2026-07-22.csv
        └── cdr_2026-07-22.csv
```

**Dlaczego data w nazwie pliku?**
Jak pobierzesz te same dane za tydzień, dostaniesz nowy plik obok starego.
Stary zostaje. To realizacja zasady „tylko dopisuj".

**Dlaczego CSV?**
CSV to zwykły plik tekstowy, gdzie wartości oddziela przecinek. Otworzysz go
w Notatniku i w Excelu. Na start nie ma nic prostszego.

### Co ma być w środku pliku

Kolumny, które daje giełda:

| Kolumna | Co znaczy |
|---|---|
| Data | dzień notowania |
| Otwarcie | cena na początku dnia |
| Najwyzszy | najwyższa cena tego dnia |
| Najnizszy | najniższa cena tego dnia |
| Zamkniecie | cena na koniec dnia — **ta jest najważniejsza** |
| Wolumen | ile akcji sprzedano |

Zapisujesz **wszystkie**, nawet jeśli teraz użyjesz tylko `Zamkniecie`.
Zasada numer 1.

---

## Skąd weźmiemy dane

Serwis **stooq.pl** udostępnia notowania w pliku CSV do pobrania.
Nie trzeba się rejestrować ani mieć klucza — po prostu wchodzisz pod adres
i plik się pobiera.

**Uwaga — nie podaję Ci gotowego adresu.** Sprawdzimy go razem na pierwszej sesji.
Powód: strony się zmieniają, a ja nie mam pewności, jak stooq wygląda dzisiaj.

**To jest pierwsza lekcja data engineeringu:**
nigdy nie pisz programu pod źródło, którego nie sprawdziłeś na własne oczy.

---

## Podział na sesje

Jedna sesja = jeden dzień = 1,5–2 godziny. **Jedna nowa rzecz na sesję.**

---

### Sesja 1 — Poznajemy źródło (bez pisania programu)

**Co robisz:** wchodzisz na stooq.pl przez przeglądarkę. Znajdujesz stronę
ze spółką Orlen. Szukasz linku do pobrania danych historycznych.
Pobierasz plik ręcznie, myszką. Otwierasz go w Notatniku i patrzysz, co jest w środku.

**Czego się uczysz:** że przed programowaniem trzeba zobaczyć dane.

**Skąd wiesz, że gotowe:** masz na dysku plik CSV i umiesz mi opisać,
jakie ma kolumny i ile ma wierszy.

**Ani jednej linijki kodu.** To celowe.

---

### Sesja 2 — Środowisko wirtualne i nowe repozytorium

**Co robisz:** zakładasz folder projektu, tworzysz w nim środowisko wirtualne,
instalujesz `requests`. Zakładasz puste repozytorium na GitHubie i łączysz z folderem.

**Czego się uczysz:** czym jest `venv` i dlaczego bez niego projekty sobie
nawzajem psują biblioteki.

**Skąd wiesz, że gotowe:** w terminalu przed ścieżką widzisz `(.venv)`,
a na GitHubie widzisz swój pierwszy commit.

Szczegóły: [[Codzienna-rutyna]]

---

### Sesja 3 — Pobranie jednego pliku programem

**Co robisz:** piszesz program, który pobiera dane **jednej** spółki
i wypisuje je na ekran. Jeszcze nie zapisuje na dysk.

**Co już umiesz:** to jest dokładnie `requests.get()` z Twojej lekcji
„Python 4". Różnica: tam przychodził JSON, tu przyjdzie zwykły tekst.
Zamiast `.json()` użyjesz `.text`.

**Nowa rzecz:** sprawdzenie, czy odpowiedź nie jest pusta lub błędna.

**Skąd wiesz, że gotowe:** uruchamiasz program, na ekranie widzisz dane.

---

### Sesja 4 — Zapis do pliku

**Co robisz:** to samo co wczoraj, ale wynik ląduje w pliku CSV
w folderze `dane/bronze/`.

**Co już umiesz:** `with open(...)` z lekcji „Python 5". To dokładnie to samo.

**Nowa rzecz:** tworzenie folderu z poziomu programu (żeby nie trzeba było
klikać myszką) i wstawienie dzisiejszej daty do nazwy pliku.

**Skąd wiesz, że gotowe:** plik istnieje, ma dzisiejszą datę w nazwie,
otwiera się w Excelu.

---

### Sesja 5 — Trzy spółki zamiast jednej

**Co robisz:** przerabiasz program tak, żeby pobierał trzy spółki po kolei.

**Co już umiesz:** pętla `for` po liście. Nic nowego.

**Nowa rzecz:** wyciągnięcie listy spółek na górę pliku, do jednego miejsca.
Dodanie czwartej spółki ma być zmianą **jednego słowa**, nie kopiowaniem kodu.

**Skąd wiesz, że gotowe:** trzy pliki w folderze, jedno uruchomienie programu.

---

### Sesja 6 — Co, gdy coś pójdzie nie tak

**Co robisz:** dokładasz `try/except` i `logging`. Program ma przetrwać sytuację,
w której internet nie działa albo giełda nie zna takiej spółki.

**Co już umiesz:** `try/except` i `logging` — masz to w „Python 4" i „Python 5".

**Nowa rzecz:** jedna zepsuta spółka nie może zatrzymać pozostałych dwóch.
Program loguje błąd i leci dalej.

**Skąd wiesz, że gotowe:** wpisujesz celowo nieistniejącą spółkę.
Program nie wywala się, tylko zapisuje błąd do pliku z logami,
a pozostałe spółki pobiera normalnie.

---

### Sesja 7 — Sprawdzasz swój własny kod

**Co robisz:** piszesz program, który sprawdza program z sesji 6.
Czy plik powstał? Czy nie jest pusty? Czy ma tyle kolumn, ile powinien?

**To Ty piszesz sprawdzenie, do swojego kodu.** Ja mogę pokazać, jak wygląda
sprawdzanie czegoś zupełnie innego — ale co i jak sprawdzić u siebie,
decydujesz sam.

**Czego się uczysz:** że program można sprawdzić programem,
zamiast klikać i patrzeć oczami.

---

### Sesja 8 — Porządki i zapis na GitHub

**Co robisz:** czytasz swój kod od góry do dołu. Poprawiasz nazwy zmiennych,
żeby były zrozumiałe. Dopisujesz krótki `README`. Wysyłasz na GitHub.

**Czego się uczysz:** że kod pisze się dla człowieka, który będzie go czytał
za pół roku. Tym człowiekiem będziesz Ty.

**Skąd wiesz, że gotowe:** wchodzisz na github.com i widzisz swój projekt.

---

## Ile to potrwa

Osiem sesji, około 12–16 godzin. Przy dwóch godzinach dziennie: **8 dni.**

Jeśli któraś sesja zajmie dwa dni — **to jest normalne i w porządku.**
Plan ma Ci służyć, nie odwrotnie.

---

## Czego NIE robimy na tym etapie

Wypisuję to, żeby Cię nie kusiło i żebyś nie czuł, że coś pomijasz:

- ❌ pandas — dopiero w etapie SILVER
- ❌ klasy — na razie w ogóle niepotrzebne
- ❌ bazy danych — pliki CSV wystarczą
- ❌ Databricks — najpierw ma działać lokalnie
- ❌ czyszczenie danych — to nie jest zadanie bronze
- ❌ trzydzieści spółek — trzy

---

## Powiązane notatki

- [[Plan-ogolny]] — cały projekt
- [[Codzienna-rutyna]] — jak zacząć dzień pracy
- [[Slownik]] — trudne słowa
