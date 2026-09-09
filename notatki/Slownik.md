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

## AWS i Kafka

### Kafka / broker
Program, który pośredniczy w przesyłaniu wiadomości między innymi
programami — nadawca i odbiorca nie muszą nic o sobie nawzajem wiedzieć,
tylko o samej Kafce. „Broker" to sam serwer Kafki, ta część, która
faktycznie przechowuje i przekazuje wiadomości.
*Jak poczta — nadawca zanosi list na pocztę, odbiorca odbiera go z poczty,
nie muszą się nigdy spotkać.*

### Topic
Nazwany „kanał" w Kafce, na który wysyła się wiadomości i z którego się
je odbiera. Jedna Kafka może mieć wiele topiców naraz.
*`gpw_tracker` to topic z cenami spółek — inny topic mógłby nosić zupełnie
inne, niepowiązane dane.*

### Producent / Konsument
Producent wysyła wiadomości na topic. Konsument je odbiera, czytając ten
sam topic. Nie łączą się bezpośrednio ze sobą — oboje rozmawiają tylko
z brokerem, i mogą działać na zupełnie różnych komputerach.

### KRaft
Nowszy sposób, w jaki Kafka pilnuje porządku w klastrze (kto jest kim,
co się dzieje) — bez osobnego programu (ZooKeepera), który kiedyś był do
tego wymagany.

### Listener / `advertised.listeners`
`listeners` to adres, na którym broker faktycznie nasłuchuje. `advertised.listeners`
to adres, który broker **podaje klientom**, żeby wiedzieli, gdzie się
zgłosić. Zwykle to samo, ale nie zawsze — na EC2 broker nasłuchuje
„wszędzie" (`0.0.0.0`), a reklamuje publiczny adres IP, bo to jedyny,
który widać z zewnątrz.

### Hairpin NAT
Sytuacja, w której serwer w chmurze nie potrafi połączyć się sam ze sobą
przez swój własny publiczny adres IP — bo ten adres nie istnieje fizycznie
na jego karcie sieciowej, tylko jest przekierowaniem od dostawcy chmury.
*Dlatego test „z tej samej instancji, przez publiczny IP" czasem nie
działa, mimo że wszystko jest poprawnie skonfigurowane — a z zewnątrz
działa bez problemu.*

### EC2
Usługa AWS dająca wirtualny komputer w chmurze, dostępny przez internet —
instalujesz i uruchamiasz na nim cokolwiek, jakby to był Twój własny
serwer.

### Security Group
Wirtualny firewall instancji EC2 — lista reguł „co wolno wejść, a co nie"
(np. który port, z jakiego adresu IP). Bez odpowiedniej reguły nikt
z zewnątrz się nie połączy, nawet jeśli program w środku działa poprawnie.

### S3 / bucket
S3 to magazyn plików w chmurze AWS — jak dysk, tylko dostępny przez
internet. „Bucket" to pojedynczy magazyn w S3, ma swoją unikalną (w całym
AWS, nie tylko u Ciebie) nazwę.

### IAM / access key
IAM to system AWS pilnujący, kto (jaki użytkownik albo program) ma prawo
robić co na koncie. Access key + secret key to „login i hasło" dla
programu, nie człowieka — pozwalają np. skryptowi w Pythonie łączyć się
z S3 bez klikania w konsoli.
*Nigdy nie trafiają do kodu ani do gita — trzymane osobno, poza
projektem.*

### Daemon (`-daemon`)
Proces działający w tle, niezależnie od okna terminala, w którym go
uruchomiono. Zamknięcie terminala go nie zabija.
*Jak pralka, którą włączasz i wychodzisz z domu — dalej pierze, mimo że
Ciebie już nie ma w pokoju.*

### Cron
Odpowiednik Harmonogramu zadań Windows, ale na Linuksie — samodzielnie
uruchamia wybrany program o wybranej porze, bez klikania.

### Offset
Numer wiadomości w topicu, nadawany po kolei od zera przy zapisie. Numery
nigdy nie wracają — skasowana wiadomość zabiera swój numer ze sobą.
`latest` to numer, jaki dostanie **następna** wiadomość; `earliest` to
numer najstarszej, która **jeszcze leży**. Odczyt:
`kafka-get-offsets.sh --topic gpw_tracker --time earliest`.
*09.09 w `gpw_tracker`: `earliest` 22, `latest` 2330 — w topicu leży 2308
wiadomości, a 22 pierwsze już skasowano.*

### Pozycja grupy (committed offset) i `commit()`
Kafka zapamiętuje dla każdej grupy konsumentów, do którego numeru ta grupa
już przeczytała — ale tylko wtedy, gdy Konsument sam to zgłosi przez
`commit()`. Przy następnym uruchomieniu Konsument z tej grupy zaczyna od
zapamiętanego numeru. Pozycja znika po 7 dniach bez żadnego połączenia
grupy.
*`kafka-consumer-groups.sh --describe`: `CURRENT-OFFSET` to pozycja
grupy, `LOG-END-OFFSET` to `latest`, `LAG` to różnica — ile wiadomości
czeka na odczyt.*

### `auto_offset_reset` — `earliest` / `latest`
Co Konsument ma zrobić, gdy grupa **nie ma** zapisanej pozycji (pierwszy
bieg, pozycja wygasła, zmieniona nazwa grupy). `earliest` — czytaj od
najstarszej wiadomości, która leży. `latest` — pomiń wszystko, co leży,
czekaj tylko na nowe. Gdy pozycja **jest**, to ustawienie nie ma nic do
roboty.
*Nowy pracownik przychodzi do skrzynki z listami: `earliest` — czyta
wszystkie zaległe, `latest` — zaległe wyrzuca i czeka na jutrzejszą
pocztę.*

### Retencja
Jak długo broker trzyma wiadomości, zanim je skasuje. Domyślnie 7 dni.
Nie kasuje pojedynczych wiadomości, tylko całe segmenty (patrz niżej),
więc w praktyce wiadomość żyje od 7 do około 14 dni.
*Skrzynka na listy opróżniana raz na tydzień: list wrzucony dzień po
opróżnieniu poleży prawie dwa tygodnie.*

### Segment
Topic na dysku brokera to nie jedna lista, tylko ciąg plików. Każdy plik
to segment. Nazwa pliku to numer pierwszej wiadomości w nim
(`00000000000000000022.log` zaczyna się od wiadomości 22). Broker zamyka
bieżący segment, gdy od jego pierwszej wiadomości minęło 7 dni, i kasuje
zamknięty segment, gdy od jego ostatniej wiadomości minęło 7 dni. Obok
`.log` leżą `.index` (numer → miejsce w pliku) i `.timeindex` (godzina →
numer), czyli spisy treści; przy otwartym segmencie mają po 10 MB
z zapasu, przy zamykaniu są przycinane.
*Zeszyty numerowane pierwszą stroną: nowy zeszyt zakładasz tydzień po
pierwszym wpisie w poprzednim, a stary wyrzucasz tydzień po ostatnim
wpisie w nim.*

### `log.dirs`
Wpis w `server.properties` brokera: folder, w którym leżą pliki wszystkich
topiców. W środku jeden podfolder na partycję, np. `gpw_tracker-0`.
*`ls -l --time-style=long-iso <folder>/gpw_tracker-0/` pokazuje segmenty
z datami — godziny w UTC, bo tak chodzi zegar EC2.*

### Obietnica (future) i `.get(timeout=…)`
`producer.send()` nie wysyła od razu — oddaje obiekt, który dopiero
**będzie** wiedział, czy wysyłka się udała. `.get(timeout=10)` czeka
najwyżej 10 sekund na potwierdzenie brokera; gdy nie przyjdzie, rzuca
`KafkaError`. Bez `.get()` skrypt traktuje zlecenie jak fakt.
*Paczka nadana w paczkomacie: `send()` to wrzucenie, `.get()` to czekanie
na SMS „paczka odebrana przez kuriera".*

### Dostarczanie „co najmniej raz" (at-least-once)
Zasada: lepiej wysłać coś dwa razy niż zgubić. Gdy nie ma pewności, że
wiadomość doszła, wysyła się ją ponownie, a powtórki odsiewa odbiorca.
*Producent nie zapisuje „wysłane", dopóki broker nie potwierdzi; jeśli
jutro wyśle dzień drugi raz, `silver.py` odrzuci duplikat. Straconego
dnia nie da się odzyskać, duplikat tak.*

---

## Powłoka i cron (Linux)

### Powłoka (`sh`, `bash`)
Program, który czyta wpisane komendy i je wykonuje — ten sam po
zalogowaniu przez SSH i ten, któremu cron wkleja treść linii `crontab`.
Wykonuje komendy jedną po drugiej i nie zaczyna następnej, dopóki
poprzednia nie skończy.
*`sleep 3 ; echo "gotowe"` — słowo pojawia się dopiero po trzech
sekundach.*

### Kod wyjścia (exit code)
Liczba, którą każdy program oddaje powłoce na koniec: `0` znaczy „poszło
dobrze", każda inna „coś poszło źle". Ostatni kod siedzi w zmiennej `$?`.
Skrypt, który łapie wszystkie swoje błędy w `try/except`, kończy zerem
także wtedy, gdy nic nie zrobił — jak Producent z martwym brokerem.
*`ls /nie-ma ; echo $?` wypisuje komunikat błędu i `2`.*

### `;` i `&&`
Dwa sposoby sklejenia komend w jednej linii. `A ; B` — wykonaj A, potem
B, bez patrzenia na kod wyjścia A (lista zakupów: nie było mleka, i tak
kupujesz chleb). `A && B` — B tylko wtedy, gdy A oddało `0` (przepis: nie
ma jajek, nie smażysz). `&&` jest właściwe, gdy B korzysta z tego, co
zrobiło A (`silver.py && gold.py` — Gold czyta plik Silvera). `;` jest
właściwe, gdy B nie zależy od A (`data_ingestion.py ; kafka_consumer.py`
— Konsument bierze to, co leży w Kafce).
*`ls /nie-ma ; echo "i tak leci"` wypisze oba; `ls /nie-ma && echo
"tylko po sukcesie"` — tylko błąd.*

### Przekierowanie `>`, `>>` i `2>&1`
`>` zapisuje wyjście komendy do pliku od zera, `>>` dopisuje na koniec.
Każdy program ma dwa kanały: `1` na zwykłe wypisy, `2` na błędy; `2>&1`
znaczy „kanał 2 wyślij tam, gdzie idzie kanał 1". Przekierowanie
przykleja się do **jednej** komendy: w `A ; B >> plik` do pliku trafia
tylko B, a wyjście A w cronie ginie. Albo każda komenda dostaje własne
`>> plik 2>&1`, albo obie w nawiasach `( A ; B ) >> plik 2>&1`.
*`echo "jeden" ; echo "dwa" >> p.txt` — na ekranie `jeden`, w pliku
tylko `dwa`.*

### `crontab -l`, `crontab plik`, `crontab -e`
Cron trzyma harmonogram w swoim folderze systemowym; jedyną furtką jest
komenda `crontab`. `-l` (list) wypisuje harmonogram, `crontab plik`
wgrywa treść pliku jako nowy harmonogram (zastępuje cały), `-e` (edit)
otwiera w edytorze i po zapisie od razu podmienia — bez kopii poprzedniej
wersji. Bezpieczna edycja: `crontab -l > kopia`, praca na drugim pliku,
`diff`, `crontab nowy`; powrót to `crontab kopia`.
*Pięć pól czasu na początku linii: minuta, godzina, dzień miesiąca,
miesiąc, dzień tygodnia; `*` znaczy „dowolny". `0 16 * * *` — codziennie
o 16:00.*

### `diff`
Porównuje dwa pliki linia po linii. Linie tylko w pierwszym pliku
z `<`, tylko w drugim z `>`, kreski `---` między nimi, pierwsza linia
wypisu to adres zmiany (`2,3c2` — linie 2–3 pierwszego zmieniły się
w linię 2 drugiego). Brak wypisu = pliki identyczne.
*Lista `mleko, chleb, masło` kontra `mleko, ser`: `< chleb`, `< masło`,
`---`, `> ser`.*

### `grep`, `sed -n`, `head`, `tail`, `cp`
`grep "tekst" plik` wypisuje linie zawierające tekst (`-n` dodaje numer
linii, `\|` znaczy „albo", `^(` — linia zaczynająca się od nawiasu).
`sed -n '324,330p' plik` wypisuje linie od 324 do 330 i nic poza tym.
`head -n 1` — pierwsza linia, `tail -n 1` — ostatnia. `cp a b` kopiuje
plik `a` pod nazwę `b`.
*`grep -n "Odebrano" errors.txt | tail -n 3` — trzy ostatnie wypisy
Konsumenta z numerami linii.*

### `nano`
Domyślny edytor tekstu na EC2 (to on otwiera się pod `crontab -e`).
Strzałki — ruch, `Ctrl+K` — wytnij linię, `Ctrl+O` + `Enter` — zapisz,
`Ctrl+X` — wyjdź. Skróty widać na dole ekranu, `^K` znaczy `Ctrl+K`.
Komendy vima (`:wq`, `dd`) wpisują się tu jako zwykłe litery.

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

### Strażnik (guard)
Sprawdzenie **przed** zapisem albo kasowaniem, które przerywa skrypt,
gdy dane wyglądają podejrzanie — zamiast liczyć, że wszystko poszło
dobrze. Zwykle `assert` porównujący „jest" z „było", gdzie „było"
pochodzi z niezależnego źródła.
*`compaction.py` pobiera obecny `bronze` z S3 i przerywa, gdy nowa liczba
wierszy spółki jest mniejsza — Athena raz oddała 405 zamiast 2283 bez
żadnego błędu.*

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
- [[Plan-05-aws-migracja]]
- [[Przeglad-2026-09-08-co-nie-gra]]
