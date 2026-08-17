# Słownik trudnych słów

Każde hasło: **co to jest** + **przykład z życia**.
Dopisuj własne, gdy spotkasz nowe słowo.

---

## Warstwy danych

### Bronze (brąz)
Magazyn surowca. Dane dokładnie takie, jakie przyszły ze źródła. Nic nie poprawiamy.
*Jak szuflada z paragonami — trzymasz oryginały na wypadek pomyłki.*

### Silver (srebro)
Dane po sprzątaniu. Poprawione daty, liczby zamiast tekstu, usunięte powtórki.
*Paragony przepisane do zeszytu, czytelnie i po kolei.*

### Gold (złoto)
Gotowe odpowiedzi. Nie surowe dane, tylko wyliczenia.
*Nie „lista wydatków", tylko „w maju wydałem 2400 zł, najwięcej na jedzenie".*

### Medallion architecture
Fachowa nazwa układu bronze → silver → gold. Medalion = medal, bo brąz-srebro-złoto.

### Pipeline
Rurociąg. Cała droga danych od pobrania do wyniku, po kolei, automatycznie.

### ETL / ELT
*Extract, Transform, Load* — pobierz, przekształć, załaduj. Trzy kroki pracy z danymi.
ELT to ta sama trójka w innej kolejności (ładujemy przed przekształceniem).

---

## Narzędzia i programy

### Terminal / konsola
Czarne okno, w którym wpisujesz polecenia zamiast klikać.
*Jak SMS do komputera zamiast rozmowy przez przyciski.*

### venv (środowisko wirtualne)
Osobna szuflada z bibliotekami dla jednego projektu.
*Żeby narzędzia z różnych projektów się nie kłóciły.*

### Biblioteka / pakiet
Gotowy kod napisany przez kogoś innego, który możesz wykorzystać.
*`requests` to biblioteka do pobierania danych z internetu.*

### pip
Program do instalowania bibliotek. `pip install requests` = „zainstaluj requests".

### requirements.txt
Lista bibliotek potrzebnych w projekcie. Jedna nazwa w każdej linii.
*Lista zakupów — ktoś inny może kupić to samo i uruchomić Twój program.*

### IDE
Program do pisania kodu. Twoje to **VS Code**.

### Jupyter Notebook
Plik, w którym piszesz kod małymi kawałkami i od razu widzisz wynik pod spodem.
*Dobry do oglądania danych, słaby do gotowych programów.*

### pytest
Biblioteka do pisania testów w Pythonie. Zamiast samemu patrzeć na to, co
wypisze `print()` i oceniać na oko, piszesz zdania `assert` — pytest sam
mówi, czy test przeszedł, czy nie, i przy którym dokładnie się wywalił.
*Uruchomienie: w terminalu, w folderze z testem, komenda `pytest
nazwa_pliku.py`.*

---

## Git i GitHub

### Git
Program pilnujący historii zmian w plikach. Działa na Twoim komputerze.
*Jak „cofnij" w Wordzie, ale dla całego projektu i na zawsze.*

### GitHub
Strona internetowa, na której trzymasz kopię projektu. **Git to program, GitHub to strona.**

### Repozytorium (repo)
Folder projektu pilnowany przez gita.

### Commit
Zapisany punkt w historii, z opisem. *Jak zapis stanu gry.*

### Push
Wysłanie zapisanych zmian z komputera na GitHub.

### Pull
Pobranie zmian z GitHuba na komputer.

### Branch (gałąź)
Osobna wersja projektu do eksperymentów, żeby nie psuć głównej.

### `.gitignore`
Lista rzeczy, których git ma **nie** wysyłać na GitHub. Hasła, dane, `.venv`.

---

## Dane

### CSV
Plik tekstowy, w którym wartości oddziela przecinek. Otwiera się w Excelu i Notatniku.

### JSON
Format zapisu danych używany przez strony internetowe.
W Pythonie zamienia się na słowniki i listy.

### API
Sposób, w jaki program prosi inny program o dane.
*Jak okienko w urzędzie — pytasz w ustalony sposób, dostajesz odpowiedź.*

### Endpoint
Konkretny adres API, pod który wysyłasz pytanie.

### Status code
Trzycyfrowa odpowiedź serwera. **200** = w porządku. **404** = nie znaleziono.
**500** = awaria po ich stronie.

### Scraping
Wyciąganie danych ze strony internetowej, gdy nie ma API.
*Trudniejsze i wrażliwe — strona się zmieni i program przestaje działać.*

### Upsert
Skrót od *update + insert*. Scalanie nowych danych z już istniejącymi: jeśli
coś jest pod tym samym kluczem (np. tą samą datą), nadpisz świeższą
wartością; jeśli danego klucza jeszcze nie było, dodaj go jako nowy wpis.
*`Data ingestion 2.py` robi dokładnie to — świeża cena z danego dnia
nadpisuje starą, a dni, których jeszcze nie było w pliku, po prostu
dochodzą.*

### Ruchome okno (rolling window)
Zakres danych liczony zawsze względem „dziś", a nie od jednej stałej daty.
Jutro całe okno przesuwa się o dzień do przodu.
*API Yahoo Finance zwraca „ostatnie 3 lata od dziś" — bez zapisywania
danych po swojej stronie, najstarszy dzień wypadałby z okna i znikał
bezpowrotnie przy każdym kolejnym pobraniu.*

### pandas
Biblioteka do pracy z tabelami w Pythonie. *Excel sterowany kodem.*

### DataFrame
Tabela w pandas. Wiersze i kolumny, jak arkusz.

### Series
Jedna kolumna z tabeli (albo jeden wiersz) w pandas, wyciągnięta pojedynczym nawiasem.
*`tabela["cena"]` to Series — jedna kolumna cen, nie cała tabela.*

### dtype
Typ danych jednej kolumny w pandas — liczby, tekst albo daty. Cała kolumna ma zawsze jeden typ.
*`.dtypes` pokazuje, że kolumna „cena" to `float64`, a „spolka" to tekst.*

### NaN
*Not a Number* — specjalna wartość pandas oznaczająca „tu nic nie ma". To nie to samo co zero albo pusty tekst.
*Dzień bez ceny zamknięcia po nieudanej konwersji zamienia się w `NaN`, nie w `0`.*

### Wektoryzacja
Operacja na całej kolumnie naraz, zamiast na jednym elemencie po drugim w pętli `for`.
*`tabela["cena"] * 2` mnoży od razu wszystkie ceny — bez pętli po każdym wierszu.*

### groupby
Podział tabeli na grupy i liczenie czegoś osobno w każdej grupie, bez pisania pętli samemu.
*`tabela.groupby("spolka")["cena"].mean()` — średnia cena osobno dla każdej spółki, jedną linijką.*

### pct_change
Funkcja pandas liczącą zmianę procentową względem poprzedniego wiersza.
*Cena wczoraj 100 zł, dziś 110 zł → `pct_change()` da `0.10`, czyli +10%.*

### merge
Sklejenie dwóch tabel obok siebie po wspólnej kolumnie. Inaczej niż `concat`, które skleja tabele jedna pod drugą.
*Tabela z cenami spółek i tabela z ich sektorami, połączone po kolumnie „spolka" — każda spółka dostaje swój sektor w tym samym wierszu.*

### agg
Liczy kilka podsumowań na grupę naraz, po `groupby`. Wynik to nowa, mniejsza
tabela — jeden wiersz na grupę, nie tyle wierszy co na starcie.
*`tabela.groupby("spolka")["cena"].agg(["first", "last"])` — pierwsza
i ostatnia cena każdej spółki, jedną linijką.*

### reset_index
Zamienia kolumnę, po której grupowałeś (`groupby`), z powrotem w zwykłą
kolumnę. Po `groupby(...).agg(...)` ta kolumna „chowa się" jako indeks
tabeli, a nie zwykła kolumna.
*Bez `reset_index()` kolumna „spolka" siedzi tam, gdzie normalnie są numery
wierszy — trudno się do niej odwołać tak jak do innych kolumn.*

### Akcesor `.dt`
Dostęp do części daty w kolumnie typu `datetime` — dnia, miesiąca, roku —
bez pisania własnej funkcji do wycinania tekstu.
*`tabela["data"].dt.to_period("M")` zamienia całą kolumnę dat na „rok-miesiąc"
(np. `2026-08`), żeby policzyć coś osobno dla każdego miesiąca.*

### dropna
Metoda pandas, która wyrzuca z tabeli wiersze z brakującą wartością (`NaN`)
w wybranej kolumnie.
*`tabela.dropna(subset=["cena"])` usuwa każdy wiersz, w którym nie ma ceny —
reszta kolumn w tym konkretnym wierszu nie ma już znaczenia, wiersz i tak
znika.*

### Odchylenie standardowe
Jedna liczba mówiąca, jak bardzo wartości „skaczą" wokół średniej. Duże odchylenie = duże wahania.
*Miesiąc, w którym cena akcji codziennie mocno skakała w górę i w dół, ma wyższe odchylenie standardowe niż spokojny miesiąc.*

### Parquet
Format zapisu tabel — mniejszy i szybszy niż CSV, ale nie otworzysz go w Notatniku.

---

## Wykresy i dashboardy

### matplotlib
Biblioteka do rysowania wykresów w Pythonie. `plt.plot(...)` rysuje linię —
dobra do pokazania **zmiany w czasie**. `plt.bar(...)` rysuje słupki —
dobre do **porównania kategorii** obok siebie.
*Cena trzech spółek dzień po dniu → linia. Która spółka urosła najbardziej
→ słupki.*
**Ważna kolejność:** `plt.savefig(...)` musi być **przed** `plt.show()` —
`show()` czyści rysunek po zamknięciu okna, więc `savefig()` po nim
zapisałby pustą kartkę.

### Power BI
Darmowy program od Microsoftu do budowania wykresów i dashboardów
przeciąganiem myszką, bez pisania kodu. Dane wczytuje się z pliku
(**Get Data → Text/CSV**), wykresy dodaje się z panelu **Visualizations**.
*To, co w Pythonie robisz linijką `plt.plot(...)`, w Power BI robisz
przeciągnięciem nazwy kolumny na wykres.*

### Dashboard
Jedna strona z kilkoma wykresami naraz, które można razem oglądać
i (czasem) razem filtrować.
*Wykres liniowy z cenami i wykres słupkowy z rankingiem spółek, obok
siebie, na jednej stronie w Power BI.*

### Fragmentator (Slicer)
Klikalny filtr na stronie w Power BI. Kliknięcie w niego zmienia od razu
wszystkie wykresy na tej stronie naraz, nie tylko jeden.
*Klik w „CBF.WA" na Fragmentatorze — oba wykresy pokazują od razu tylko tę
jedną spółkę.*

---

## Automatyzacja

### Harmonogram zadań (Task Scheduler)
Wbudowane w Windows narzędzie, które samo uruchamia program o wybranej
porze — bez klikania czegokolwiek przez Ciebie.
*Codziennie o 10:25 sam odpala pobieranie nowych danych giełdowych, nawet
gdy nikt nie siedzi przy komputerze.*

### Wyzwalacz (trigger)
Reguła „**kiedy**" w Harmonogramie zadań: codziennie o określonej godzinie,
raz w tygodniu, itd.
*„Codziennie o 10:25" to wyzwalacz.*

### Akcja
Reguła „**co**" w Harmonogramie zadań: jaki program albo plik ma się
uruchomić.
*„Uruchom `pipeline.bat`" to akcja.*

### Plik `.bat`
Plik z listą komend Windows, wykonywanych po kolei, jedna po drugiej.
W przeciwieństwie do pliku `.py`, jest **bezpośrednio wykonywalny** — nie
potrzebuje interpretera (np. Pythona) przed sobą, Windows wie sam, jak go
uruchomić.
*`pipeline.bat` odpala po kolei trzy skrypty Pythona: pobranie danych,
czyszczenie, liczenie wskaźników — jedno zadanie w Harmonogramie zamiast
trzech osobnych.*

---

## Kod

### Funkcja (`def`)
Kawałek kodu z nazwą, który możesz wywołać wiele razy.
*Przepis: raz napisany, używany zawsze.*

### Argument / parametr
To, co podajesz funkcji do środka.

### Zwracanie (`return`)
To, co funkcja oddaje po zakończeniu.

### Type hints (podpowiedzi typów)
Dopisek mówiący, jakiego rodzaju dane wchodzą i wychodzą.
`def licz(kwota: int) -> float:` — *wchodzi liczba całkowita, wychodzi ułamek.*
**Już to stosujesz w swoich lekcjach.**

### Klasa
Własny typ danych, łączący dane i funkcje w jedną całość.
*Jeszcze nie potrzebujesz. Powiem, kiedy nadejdzie moment.*

### Moduł
Jeden plik `.py`. Możesz z niego importować rzeczy do innych plików.
*`kod/config.py` trzyma listę spółek w jednym miejscu — inne pliki robią
`from config import ticker` zamiast wpisywać tę samą listę osobno w każdym
z nich.*

### Import
Wciągnięcie kodu z innego pliku lub biblioteki. `import requests`.

### Dekorator (`@`)
Linijka nad funkcją, zaczynająca się od `@`, która zmienia albo rozszerza
sposób działania tej funkcji — bez zmieniania jej wnętrza.
*`@pytest.mark.parametrize("tick", ticker)` nad funkcją testową sprawia, że
pytest odpala tę samą funkcję osobno dla każdej spółki z listy, bez pisania
pętli `for` samemu.*

### `try` / `except`
Zabezpieczenie. „Spróbuj to zrobić, a jak się nie uda, zrób tamto".
**Już to stosujesz.**

### Wyjątek (exception)
Błąd, który zatrzymuje program. `ValueError`, `KeyError` to nazwy typów błędów.

### Logging
Zapisywanie do pliku, co program robił. **Już to stosujesz.**
*Czarna skrzynka w samolocie — po awarii wiadomo, co się działo.*

### assert
Zdanie w kodzie w stylu „to musi być prawdą, inaczej zatrzymaj program i
pokaż błąd". Używane do pilnowania, czy dane albo wynik są poprawne.
*`assert dane["cena"].isna().sum() == 0, "zostały puste ceny"` — program
zatrzyma się z tym komunikatem, jeśli choć jedna cena jest pusta.*

### Test
Program sprawdzający inny program.
*Sam napiszesz kod, sam napiszesz sprawdzenie. W tej kolejności.*
**W tym projekcie:** `pytest` — patrz sekcja „Narzędzia i programy".

### Refaktoryzacja
Poprawianie kodu, żeby był czytelniejszy, bez zmiany tego, co robi.

---

## Giełda

### Ticker
Krótki symbol spółki. `PKN` = Orlen, `CDR` = CD Projekt.

### OHLC
*Open, High, Low, Close* — otwarcie, najwyższa, najniższa, zamknięcie.
Cztery ceny opisujące jeden dzień notowań.

### Wolumen
Ile akcji sprzedano danego dnia.

### WIG20 / mWIG40
Indeksy — listy największych spółek na warszawskiej giełdzie.

### ESPI / EBI
Systemy, przez które spółki ogłaszają ważne wiadomości.
*Oficjalna tablica ogłoszeń giełdy.*

### Sesja
Jeden dzień handlu. Na GPW od 9:00 do 17:00.

### Zmienność / wolatylność
Jak bardzo cena danej spółki waha się w krótkim czasie. Wysoka zmienność = duże, częste ruchy ceny w obie strony.
*Mała, mało znana spółka potrafi zmienić się o kilkanaście procent w jeden dzień — to wysoka zmienność.*

---

## Powiązane notatki

- [[Plan-ogolny]]
- [[Plan-01-bronze]]
- [[Plan-02-silver]]
- [[Plan-03-gold]]
- [[Plan-04-pokazanie-wyniku]]
