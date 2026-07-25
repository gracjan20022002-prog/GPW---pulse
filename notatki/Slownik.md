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

### pandas
Biblioteka do pracy z tabelami w Pythonie. *Excel sterowany kodem.*

### DataFrame
Tabela w pandas. Wiersze i kolumny, jak arkusz.

### Parquet
Format zapisu tabel — mniejszy i szybszy niż CSV, ale nie otworzysz go w Notatniku.

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

### Import
Wciągnięcie kodu z innego pliku lub biblioteki. `import requests`.

### `try` / `except`
Zabezpieczenie. „Spróbuj to zrobić, a jak się nie uda, zrób tamto".
**Już to stosujesz.**

### Wyjątek (exception)
Błąd, który zatrzymuje program. `ValueError`, `KeyError` to nazwy typów błędów.

### Logging
Zapisywanie do pliku, co program robił. **Już to stosujesz.**
*Czarna skrzynka w samolocie — po awarii wiadomo, co się działo.*

### Test
Program sprawdzający inny program.
*Sam napiszesz kod, sam napiszesz sprawdzenie. W tej kolejności.*

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

---

## Powiązane notatki

- [[Plan-ogolny]]
- [[Plan-01-bronze]]
