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
**Po co:** bez venv wszystkie projekty na komputerze dzielą jeden wspólny
zestaw bibliotek, a w nim mieści się tylko jedna wersja każdej biblioteki.
Instalacja nowszej wersji dla jednego projektu po cichu zmienia działanie
drugiego. venv daje każdemu projektowi **osobny zestaw bibliotek w jego
własnych wersjach**. Ten zestaw da się spisać (`pip freeze`) i odtworzyć
na innej maszynie (`pip install -r plik`).
**Co to jest:** folder z własnym `python.exe`, własnym `pip` i własnym
miejscem na biblioteki (`Lib\site-packages`). Co `pip` zainstaluje w tym
środowisku, nie trafia do wspólnego zestawu komputera.
*Projekt „Lodziarnia" jest pisany pod pandas 2, projekt „Pogoda" potrzebuje
pandas 3. Bez venv `pip install pandas==3.0.5` dla Pogody usuwa pandas 2,
bo miejsce jest jedno. W Lodziarni warunek `lody["smak"].dtype == object`
zmienia wtedy wynik z `True` na `False`, bo pandas 3 daje kolumnie
z tekstem typ `str`, a nie `object` (sprawdzone 14.09 na pandas 3.0.5).
Czyszczenie spacji przestaje działać, bez żadnego błędu na ekranie. Z venv
każdy projekt ma swoje pandas i nic się nie zmienia. U nas: laptop ma
`.venv` z pandas 3.0.5, EC2 ma `venv` z pandas 2.3.3, bo Python 3.9 na
EC2 nie przyjmie pandas 3.*
**Do zapamiętania:** osobny zestaw bibliotek w konkretnych wersjach dla
jednego projektu — żeby instalowanie czegoś dla innego projektu go nie
zepsuło i żeby dało się ten zestaw odtworzyć na innej maszynie.

### Aktywacja venv (`Activate.ps1`, `deactivate`)
Aktywacja dopisuje folder `.venv\Scripts` na **początek** listy `PATH`,
tylko w tym jednym oknie terminala. Od tej chwili samo słowo `python`
znaczy `.venv\Scripts\python.exe`, a znak zachęty zaczyna się od
`(.venv)`. `deactivate` zdejmuje ten wpis; nowe okno zaczyna bez
aktywacji. Pełna ścieżka do `python.exe` działa tak samo bez żadnej
aktywacji — tak uruchamiają nasze skrypty `pipeline.bat` i `crontab`.
*14.09, pusty folder testowy „lodziarnia": przed aktywacją `python` →
`...\Python314\python.exe`, po aktywacji → `...\lodziarnia\.venv\Scripts\python.exe`,
`pip list` pokazuje tylko `pip`, a `import pandas` kończy się błędem.*

### `PATH`
Lista folderów, w których system szuka programu, gdy wpiszesz samą jego
nazwę, np. `python`. Sprawdza je po kolei i bierze pierwszy trafiony.
*`($env:PATH -split ';')[0]` w PowerShellu pokazuje pierwszy folder
z listy — po aktywacji venv to `.venv\Scripts`.*

### `pyvenv.cfg`
Plik w środku venv z opisem, z jakiego Pythona go zrobiono (`home`,
`version`) i czy widzi biblioteki całego komputera
(`include-system-site-packages = false` — nie widzi).
*W środku venv zapisane są pełne ścieżki, dlatego przeniesienie folderu
go psuje — na EC2 31.08 trzeba było zrobić venv od nowa.*

### Suma kontrolna (SHA256) i `Get-FileHash`
Długi napis wyliczony z każdego bajta pliku. Zmiana choćby jednego znaku
daje zupełnie inny napis, więc dwa pliki z tą samą sumą są identyczne.
W PowerShellu: `Get-FileHash plik -Algorithm SHA256`.
*14.09: `silver/clean_data.csv` przed testem zakładki i po ponownym biegu
Silvera miał tę samą sumę `0F21AA1A…` — powtórki nie zmieniły ani bajta.*

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

### `pip freeze`
Wypisuje **wszystko**, co jest zainstalowane w bieżącym środowisku, po
jednej paczce na linię, w formacie `nazwa==wersja`. Nie lista tego, czego
projekt potrzebuje — lista tego, co faktycznie leży.
*Laptop 11.09: 32 linie. EC2: 19 linii. Ta różnica to nie błąd, tylko
dwie różne maszyny.*

### `pip show nazwa`
Opisuje jedną paczkę: wersję, gdzie leży i — najważniejsze — pole
`Requires`, czyli czego ta paczka sama potrzebuje do działania.
*`pip show matplotlib` pokazał `contourpy, cycler, fonttools, kiwisolver,
numpy, packaging, pillow, pyparsing`. Dzięki temu wiadomo, że te paczki
nie leżą w środowisku przypadkiem.*

### Przypięcie wersji (`==`)
Zapis `pandas==3.0.5` znaczy „dokładnie ta wersja, żadna inna". Bez tego
`pip` weźmie najnowszą dostępną, a najnowsza za pół roku to co innego niż
dziś.
*Przypięcie daje powtarzalność i odbiera aktualizacje. Jedno i drugie
naraz.*

### Zależność przechodnia
Paczka, której nie instalowałeś i nie importujesz, a leży w środowisku,
bo potrzebuje jej coś, co zainstalowałeś.
*`pillow` jest na laptopie nie dlatego, że ktoś go chciał, tylko dlatego,
że wymaga go `matplotlib`.*

### `requirements.txt` i spis na maszynę
Plik ze spisem paczek. Instalacja z niego: `pip install -r plik`.
Pułapka: spis opisuje **jedno konkretne środowisko**, a nazwa tego nie
mówi.
*Dlatego od 11.09 mamy dwa: `requirements-lokalny.txt` (32 paczki,
Python 3.14) i `requirements-ec2.txt` (19 paczek, Python 3.9). Jeden
wspólny plik zainstalowałby na EC2 zestaw, którego ten Python nie
przyjmie.*

### `Compare-Object` (PowerShell)
Porównuje dwie listy i pokazuje **tylko różnice**. Strzałka `<=` znaczy
„jest w pierwszej, nie ma w drugiej", `=>` odwrotnie.
*`Compare-Object (Get-Content requirements-lokalny.txt) (pip freeze)` —
pusty wynik znaczy pełną zgodność. Odpowiednik `diff` na Linuksie.*

### `$env:NAZWA` (PowerShell)
Zmienna środowiskowa, czyli ustawienie widoczne dla programów
uruchamianych w **tym samym oknie**. Znika po zamknięciu okna.
*`$env:KAFKA_BOOTSTRAP = "127.0.0.1:9092"` każe Producentowi łączyć się
z martwym adresem zamiast z prawdziwym brokerem. Samo `$env:KAFKA_BOOTSTRAP`
wypisuje obecną wartość — warto sprawdzić przed uruchomieniem.*
`Remove-Item Env:NAZWA` usuwa zmienną z okna; potem `echo $env:NAZWA`
wypisuje pustą linię. **W cmd składnia jest inna:** `set NAZWA=1` ustawia,
`set NAZWA=` usuwa, `%NAZWA%` wstawia wartość. `echo %NAZWA%` wpisane do
PowerShella niczego nie sprawdza — zawsze wypisuje sam napis `%NAZWA%`.
Poznać, gdzie jestem: wiersz PowerShella zaczyna się od `PS`, wiersz cmd nie.
*15.09: `$env:GOLD_DO_S3 = "1"` → `python kod\gold.py` wysłał pliki do S3,
`Remove-Item Env:GOLD_DO_S3` wyłączył przełącznik.*

### `os.environ.get` i przełącznik ze zmiennej
`os.environ.get("NAZWA")` odczytuje w Pythonie zmienną środowiskową.
Zwraca **tekst** albo `None`, gdy zmiennej nie ma. Przełącznik to `if`,
który coś robi tylko przy konkretnej wartości.
*Wejście i wyjście z 15.09 dla `os.environ.get("LODY_DO_S3") == "1"`: brak
zmiennej → `None` → `False`; `1` → `True`; `0`, `tak`, ` 1` ze spacją →
`False`. Ten sam `gold.py` na laptopie tylko pisze „Pominięto", a na EC2
(zmienna w `crontab`) wysyła do S3.*

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

### `git rm`
Kasuje plik z dysku **i** od razu zapisuje to skasowanie w poczekalni
gita, więc nie trzeba potem robić `git add`. Działa tylko na plikach,
które git śledzi; plik z `.gitignore` trzeba skasować zwyczajnie.
*`git rm "kod/pipeline.py"` wypisuje `rm 'kod/pipeline.py'`.*

### `git commit --amend`
„Popraw ostatni commit". Nie edytuje istniejącego commitu, tylko robi
nowy w jego miejsce, z **nowym identyfikatorem**, a stary znika
z historii. Dlatego jest bezpieczny **wyłącznie przed `git push`** —
po wysłaniu zrobiłby drugą, rozjechaną wersję historii, a EC2 pobiera
właśnie z GitHuba. Z flagą `-m` zastępuje **całą** dotychczasową
wiadomość, nie dokleja się do niej.
*Sprawdzenie, czy zdążysz: `git status -sb` pokazuje `[ahead 1]`, gdy
commit jest jeszcze tylko u Ciebie.*

### `git mv`
Zmienia nazwę pliku **i od razu mówi o tym gitowi**. Zwykłe przemianowanie
w Eksploratorze git widzi jako skasowanie jednego pliku i utworzenie
drugiego, a wtedy historia zmian zostaje przy starej nazwie.
*`git mv requirements.txt requirements-lokalny.txt`. Nic nie wypisuje —
cisza to sukces.*

### `renamed` w `git status`
Git nie zapisuje „zmiany nazwy" jako osobnej operacji. Porównuje treść
i sam zgaduje, że to ten sam plik.
*Gdy treść została nietknięta, zobaczysz `renamed: stara -> nowa`. Gdy
przy okazji zmieniłeś zawartość, git pokaże osobno `deleted` i `new
file` — to też jest poprawne, tylko mniej czytelne.*

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

### `AWS_ENDPOINT_URL_S3`
Zmienna środowiskowa, którą mówi się `boto3`: „adres S3 jest tutaj",
zamiast prawdziwego adresu AWS. Służy do testów na lokalnych podróbkach
S3 — i do celowego psucia połączenia.
*17.09 tak odcięliśmy Konsumentowi zapis do S3, żeby pokazać utratę
danych: `AWS_ENDPOINT_URL_S3=http://localhost:1` przed komendą. Nikt nie
słucha na porcie 1, więc `put_object` rzucił
`EndpointConnectionError`. Nic nie wyszło na zewnątrz, nic w AWS nie
zostało ruszone i kod pozostał nietknięty.*
*Przy okazji wyszło coś ważniejszego: `boto3.client("s3")` przeszedł bez
błędu, bo klient powstaje **bez** łączenia się z siecią. Awaria przychodzi
dopiero przy pierwszym prawdziwym zapisie.*

### Status code
Trzycyfrowa odpowiedź serwera. **200** = w porządku. **404** = nie znaleziono.
**500** = awaria po ich stronie.

### `timeout` (limit czasu)
Dodatkowa informacja podana przy pytaniu do API: ile sekund czekać na
odpowiedź, zanim uznamy, że jej nie będzie. Bez niego `requests` czeka
bez końca. Można podać jedną liczbę albo dwie w nawiasie: pierwsza to
czas na nawiązanie połączenia, druga na przysłanie danych po jego
nawiązaniu. Przekroczenie limitu podnosi wyjątek z rodziny
`RequestException`, więc łapie go zwykły `except` na błędy sieci.
Uwaga: druga liczba nie jest limitem na całość pobierania, tylko na
ciszę między kolejnymi porcjami danych.
*Dzwonisz i czekasz dziesięć sygnałów na odebranie, a potem najwyżej pół
minuty ciszy w słuchawce, zanim się rozłączysz.*

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

### `aws sts get-caller-identity`
Pyta AWS: „kim jestem?". Wypisuje numer konta i `Arn`, czyli pełną nazwę
tożsamości, której używa ta maszyna.
*15.09 z laptopa: `Arn` kończy się na `:user/gpw-tracker-admin`.*

### Rola i polityka IAM (`list-attached-role-policies`, `list-role-policies`)
**Rola** to zestaw uprawnień, który maszyna (np. EC2) dostaje bez hasła.
**Polityka** to jedna lista „wolno / nie wolno". Do roli można podpiąć
gotowe polityki AWS (`list-attached-role-policies`) albo wpisać własne
wprost w rolę (`list-role-policies`) — to dwie osobne listy i trzeba
sprawdzić obie.
*15.09 dla `gpw_tracker_ec2_role`: podpięte `AmazonS3FullAccess`
i `AmazonAthenaFullAccess`, wpisane wprost `[]`.*

### Polityka bucketa (`get-bucket-policy`)
Sam bucket S3 może mieć politykę, która zabrania zapisu niezależnie od
uprawnień roli. `aws s3api get-bucket-policy --bucket nazwa` ją wypisuje.
*15.09: błąd `NoSuchBucketPolicy` — tu błąd był dobrą wiadomością, bo znaczy
„bucket nie ma własnych zakazów".*

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

### Dostarczanie „co najwyżej raz" (at-most-once)
Przeciwieństwo powyższego: wiadomość nigdy się nie zdubluje, ale może
przepaść. Tak zachowuje się odbiorca, który odhacza przeczytane **przed**
zapisaniem — gdy zapis padnie, nie ma już do czego wrócić.
*Tak działał nasz Konsument do 17.09, przez włączony
`enable_auto_commit`. Wybór między tymi dwiema zasadami jest wyborem, co
boli mniej. U nas powtórki nie bolą wcale, bo Silver je odsiewa dwoma
sitami: `UNION` w zapytaniu i `drop_duplicates` po dniu i spółce. Utrata
boli na zawsze. Dlatego 17.09 wybraliśmy „co najmniej raz".*

### Członek grupy i `consumer.close()`
Konsument, który czyta, jest **członkiem** swojej grupy. `consumer.close()`
mówi brokerowi „wychodzę". Bez niego broker trzyma Konsumenta na liście
jeszcze kilkanaście sekund, aż uzna ciszę za wyjście. Ma to skutek
praktyczny: `--reset-offsets` wymaga grupy bez aktywnych członków.
*14.09 tuż po ręcznym biegu `--describe` pokazał `kafka-python-3.0.11-…`
z `/127.0.0.1` zamiast `no active members`; minutę później lista była
pusta. W lodziarni: kucharz wyszedł bez „do widzenia".*
*17.09 dopisane do Konsumenta — po udanym biegu `--describe` od razu pokazał
`no active members`. **Ale `close()` stoi za `put_object`**, więc przy
awarii zapisu program pada, zanim do niego dojdzie: sprzątanie po sobie
działa tylko na ścieżce, która się udaje. Pełne rozwiązanie wymagałoby
`finally`.*

### `--delete --group` a `--reset-offsets`
`kafka-consumer-groups.sh --delete --group nazwa` kasuje grupę razem z jej
pozycją — przy następnym biegu Konsument nie ma zakładki i włącza się
`auto_offset_reset`. `--reset-offsets --to-earliest --execute` tylko
przestawia pozycję na początek — zakładka dalej jest, więc
`auto_offset_reset` nie ma nic do roboty.
*Test 14.09 użył `--delete`: `Odebrano 15 wiadomości` pokazało, że
`earliest` naprawdę działa.*

### `--reset-offsets --shift-by` i `--dry-run`
`--shift-by n` przesuwa zakładkę o `n` pozycji; `n` może być **ujemne**,
czyli cofać. Zakres trzeba podać jawnie: `--topic nazwa` albo
`--all-topics`. **`--dry-run` jest domyślny** — bez `--execute` narzędzie
tylko wypisuje plan i niczego nie zmienia. Wymaga grupy bez aktywnych
członków.
*17.09 na EC2: `--shift-by -3 --dry-run` wypisało `NEW-OFFSET 2348`, potem
to samo z `--execute` zapisało tę pozycję. Tak przygotowaliśmy trzy
wiadomości do testu — bezpiecznie, bo były już w S3 z biegu o 18:00.*

### Automatyczny zapis pozycji (`enable_auto_commit`)
Ustawienie `kafka-python`. Gdy włączone (domyślnie), biblioteka sama
zapisuje pozycję grupy co 5 sekund w trakcie czytania, niezależnie od
naszego `commit()`. Zapis zachodzi wewnątrz `poll()`, czyli **w trakcie**
pętli po wiadomościach, a nie po niej. Trzecim miejscem zapisu jest
`close()`, które sprawdza ten sam przełącznik.
*17.09 podejrzenie z 14.09 potwierdzone w kodzie biblioteki i pokazane na
żywo: zakładka przeskoczyła 2348 → 2351, choć w `live/` nie pojawił się ani
jeden plik. Naprawa: `enable_auto_commit=False`, więc zakładkę przesuwa
tylko nasz `commit()` — po udanym zapisie do S3. Kucharz odhacza zamówienie
dopiero wtedy, gdy lody wyjdą z kuchni.*

### `aws s3 ls --recursive --summarize` i `aws s3 cp … -`
`aws s3 ls s3://bucket/folder/` wypisuje pliki w S3. `--recursive` schodzi
do podfolderów, `--summarize` dopisuje na końcu `Total Objects` (liczba
plików) i `Total Size` (bajty). `aws s3 cp s3://…/plik -` kopiuje plik na
`-`, czyli na ekran, zamiast na dysk.
*14.09: `Total Objects: 24` przed testem zakładki i `27` po; nowy plik CBF
wypisany na ekran miał 5 linii.* *15.09: godzinę pliku `aws s3 ls` na
laptopie pokazuje w czasie laptopa (polskim), np. `19:19:08`.*

### Prefiks, czyli „folder" w S3, i `PRE`
S3 nie ma prawdziwych folderów. `gold/ranking/ranking.csv` to **jedna długa
nazwa pliku**, a `gold/ranking/` to jej początek, czyli prefiks. `aws s3 ls`
i Athena pokazują prefiksy tak, jakby były folderami; w wypisie oznacza je
`PRE`.
*15.09: `aws s3 ls s3://gpw-tracker-bucket/` → `PRE athena-results/`,
`PRE bronze/`, `PRE live/`.*

### `upload_file` i nadpisanie pliku w S3
`s3.upload_file(plik_na_dysku, bucket, nazwa_w_S3)` wysyła plik **taki,
jaki leży na dysku w chwili wysyłki**. Wysłanie pod tę samą nazwę zastępuje
poprzedni plik bez pytania i bez błędu.
*15.09: dlatego w `gold.py` wysyłka stoi pod oboma `to_csv` — wysłana
przed nimi byłaby wczorajsza, a log i tak napisałby „wysłano".*

### Tabela w Athenie to opis folderu
Tabela w Athenie nie kopiuje danych. Mówi tylko: pliki leżą pod tym
prefiksem i mają takie kolumny. Przy każdym zapytaniu Athena czyta
**wszystkie** pliki pod prefiksem; kolumny CSV dopasowuje po kolejności,
nie po nazwie.
*Lodziarnia: w folderze `wyniki/ranking_lodow/` jeden plik z 2 smakami →
`SELECT *` zwraca 2 wiersze; ktoś zostawia obok kopię → 4 wiersze, bez
błędu.*

### `CREATE EXTERNAL TABLE`
Polecenie SQL, którym zakłada się taki opis folderu. Nie tworzy pliku i nie
kopiuje danych — dopisuje wpis do katalogu Atheny. Cztery części, które
trzeba znać:
- **`EXTERNAL`** — dane są na zewnątrz, więc `DROP TABLE` kasuje **sam
  opis**, a pliki w S3 zostają nietknięte. Dlatego pomyłkę w tabeli naprawia
  się przez skasowanie i założenie od nowa.
- **`ROW FORMAT DELIMITED` + `FIELDS TERMINATED BY ','`** — plik jest
  tekstowy, a kolumny rozdziela przecinek (*delimited* = rozdzielony,
  *fields* = kolumny).
- **`LOCATION 's3://…/folder/'`** — folder, nie plik, z ukośnikiem na końcu.
- **`TBLPROPERTIES ('skip.header.line.count'='1')`** — pomiń pierwszą linię
  każdego pliku, czyli nagłówek (*header* = nagłówek).
*16.09 tak powstały `gold_dane_dzienne` i `gold_ranking_spolek`.*

### `ALTER TABLE … CHANGE COLUMN`
Zmienia nazwę, typ, kolejność albo komentarz kolumny w tabeli Atheny.
Składnia: `ALTER TABLE tabela CHANGE COLUMN stara nowa typ`. **Typ trzeba
podać, nawet gdy się nie zmienia.** Nie rusza plików w S3 — poprawia sam
opis w katalogu Glue. Dla kilku kolumn naraz jest
`ALTER TABLE … REPLACE COLUMNS (…)`.
*Lodziarnia: `ALTER TABLE lody CHANGE COLUMN ile galki int` — kolumna `ile`
nazywa się od tej chwili `galki`, liczby te same, plik nietknięty.*
*17.09 Gracjan zmienił tak `pierwsza_cena` na `pierwotna_cena`
i `ostatnia_cena` na `aktualna_cena` w `gold_ranking_spolek`. Skutek
uboczny: nagłówek w pliku CSV ma nadal stare nazwy. Nie szkodzi, bo
nagłówek jest pomijany, a kolumny dopasowują się po kolejności — ale
czytając plik i tabelę obok siebie widać rozjazd.*

### `NULL` (pusta komórka)
Brak wartości — nie zero i nie pusty tekst. W pliku CSV puste pole między
dwoma przecinkami, w Athenie `NULL`. Szuka się go przez `WHERE kolumna IS
NULL`, nigdy przez `= NULL`.
*16.09: `zmiana_proc` jest pusta w pierwszym dniu notowań każdej spółki, bo
nie ma jeszcze dnia poprzedniego — zapytanie zwróciło 3 wiersze, po jednym
na spółkę.*

### `Data scanned`
Liczba, którą konsola Atheny pokazuje przy każdym zapytaniu: ile bajtów
naprawdę przeczytała. Athena liczy po niej opłatę, ale przydaje się też jako
darmowe sprawdzenie, czy tabela czyta ten plik, o którym myślisz.
*16.09: `0.36 KB` przy pliku `ranking.csv` o rozmiarze 365 bajtów.*

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

### `CRON_TZ` i strefa czasowa systemu
Cron czyta godziny z `crontab` w strefie czasowej **systemu**. EC2
chodzi na czasie uniwersalnym (UTC), dlatego wpis `0 16` daje bieg
o 18:00 polskiego latem i dałby 17:00 zimą, bo Polska cofa zegary,
a UTC nie. Linia `CRON_TZ=Europe/Warsaw` na górze `crontab` każe cronowi
czytać godziny po polsku, więc zmiana czasu przestaje mieć znaczenie.
**Pułapka:** dopisanie samej tej linii przesuwa istniejące wpisy, bo te
same cyfry zaczynają znaczyć co innego. Strefa i godziny muszą zmienić
się jednym ruchem.
*Sprawdzenie bez ruszania harmonogramu: `rpm -q cronie` (odmiana
i wersja), `grep -a -c CRON_TZ /usr/sbin/crond` (czy program zna to
słowo), `timedatectl` (strefa systemu), `ls /usr/share/zoneinfo/Europe/Warsaw`
(czy system wie, kiedy Polska zmienia czas).*

### `cut`, `sort`, `uniq -c`
Trójka do liczenia powtórek w pliku tekstowym. `cut -c1-10` bierze
z każdej linii pierwsze dziesięć znaków, `sort` układa wyniki po kolei,
`uniq -c` zlicza sąsiadujące powtórzenia. `uniq` widzi tylko sąsiadów,
dlatego `sort` musi iść **przed** nim.
*`cut -c1-10 errors.log | sort | uniq -c` → `8 2026-08-31`, czyli cały
plik to osiem wpisów z jednego dnia.*

### `grep -a` i `grep -c`
`-a` każe traktować plik binarny jak zwykły tekst (normalnie `grep`
odmawia go czytać). `-c` zlicza pasujące linie zamiast je wypisywać.
Razem dają tani sposób sprawdzenia, czy program obsługuje jakąś opcję:
jeśli obsługuje, jej nazwa musi być gdzieś w pliku wykonywalnym.
*`grep -a -c CRON_TZ /usr/sbin/crond` → `1`.*

### `rpm -q` i `timedatectl`
`rpm -q nazwa` odpowiada, czy pakiet o tej nazwie jest zainstalowany
i w jakiej wersji (Amazon Linux, Fedora, RHEL). `timedatectl` pokazuje
czas lokalny, uniwersalny i ustawioną strefę.
*`rpm -q cronie` → `cronie-1.5.7-1.amzn2023.0.2.x86_64`.*

### `wc -l`
Liczy linie w pliku. Najtańsze możliwe sprawdzenie „czy coś przybyło".
*`wc -l companies/errors.txt` → `440`. Policzone **przed** biegiem
i **po** nim daje dowód, którego nie da się podrobić okiem.*

### Podstawienie procesu `<( )`
Pozwala podać **wynik komendy** tam, gdzie program spodziewa się nazwy
pliku. Powłoka tworzy plik tymczasowy w locie.
*`diff <(sort plik.txt) <(pip freeze | sort)` porównuje plik z żywym
stanem maszyny, bez zapisywania niczego na dysk. Działa w `bash`, nie
w PowerShellu — tam ten sam efekt daje `Compare-Object`.*

### `sed 's/stare/nowe/'`, `-e` i `^`
`sed` czyta plik linia po linii i wypisuje go ze zmianami; samego pliku nie
zmienia. Reguła `s/stare/nowe/` zamienia w linii pierwszy napis `stare` na
`nowe`. `-e` dokłada kolejną regułę. `^` na początku wzorca znaczy „tylko na
początku linii" — bez niego wzorzec trafia też w środek innych napisów.
*`sed -e 's/^0 5 /0 7 /' -e 's/^10 5 /10 8 /' plan.txt`: chleb z 5:00 na
7:00, bułki z 5:10 na 8:10. Bez `^` bułki lądują na 7:10, bo `0 5 ` siedzi
w środku `10 5 `.*

### `sed` z adresem i `a` (dopisz linię)
`s` zamienia, `a` **dopisuje nową linię pod** tą, którą wskazał adres.
Adresem może być wzorzec w ukośnikach — `/^SKLEP=/` znaczy „linia
zaczynająca się od `SKLEP=`" — albo numer linii. Bez adresu polecenie
działa na **każdej** linii. `a` pochodzi od angielskiego *append*, czyli
„dołącz".
*`sed '/^SKLEP=/a BUDZET=50' lista.txt` wstawia `BUDZET=50` zaraz pod
`SKLEP=Biedronka`, a `mleko` i `chleb` zostają niżej, nietknięte.*
*Dlaczego adresem jest treść, nie numer: `sed '2a …'` zadziała tak samo
dziś, ale gdyby coś doszło na górze pliku, wstawiłoby linię w złe miejsce
bez żadnego błędu. 17.09 tak wstawialiśmy `GOLD_DO_S3=1` pod
`KAFKA_BOOTSTRAP=` w `crontab`.*

### Adresy w wypisie `diff`: `a`, `c`, `d`
Pierwsza linia bloku mówi, co się stało: `a` — dodano (*add*), `c` —
zmieniono (*change*), `d` — usunięto (*delete*). Liczby po lewej to linie
pierwszego pliku, po prawej drugiego.
*`0a1` — na samym początku dodano linię 1 drugiego pliku; `2,3c3,4` — linie
2–3 pierwszego zmieniły się w linie 3–4 drugiego.*

### `NAZWA=wartość komenda` i `date "+%H:%M %Z"`
Zapis przed komendą ustawia zmienną środowiskową tylko dla tej jednej
komendy (w PowerShellu tego skrótu nie ma). `date "+…"` wypisuje czas
w podanym formacie: `%H` — godzina, `%M` — minuty, `%Z` — skrót strefy.
*`date "+%H:%M %Z"` → `13:03 UTC`; `TZ=Europe/Warsaw date "+%H:%M %Z"` →
`15:03 CEST`.*

### CEST i CET
Polski czas letni (CEST) jest dwie godziny przed UTC, zimowy (CET) —
godzinę. Zmiana w ostatnią niedzielę marca i ostatnią niedzielę
października (w 2026 — 25.10).
*Bieg `cron` o 18:00 polskiego pokazuje w logu EC2 `16:00` latem i `17:00`
zimą. Oba odczyty są poprawne.*

### Czego `CRON_TZ` nie zmienia
Strefa działa tylko wewnątrz `cron`, gdy liczy, czy już pora. Skrypt jej nie
dostaje: `datetime.now()`, czas plików w `ls -l` i dziennik systemowy
zostają w UTC. `CRON_TZ` działa tylko na linie pod sobą, więc stoi na samej
górze. Cron nie sprawdza, czy nazwa strefy istnieje.
*Po zmianie z 13.09 linia startu Producenta dalej pokazuje `16:00:0X` — i tak
ma być.*

### `sudo` i `journalctl`
`sudo` uruchamia jedną komendę z uprawnieniami administratora. `journalctl`
czyta dziennik systemowy, do którego piszą usługi, między innymi `cron`.
`--since "30min ago"` — tylko ostatnie 30 minut; `--no-pager` — wszystko
naraz, bez przewijanego podglądu. Godziny są w strefie systemu, na EC2 UTC.
*`sudo journalctl --since "30min ago" --no-pager | grep -i cron`.*

### `LIST`, `REPLACE`, `RELOAD`, `CMD` w dzienniku `cron`
Ślady w dzienniku systemowym: `LIST` — ktoś wypisał harmonogram
(`crontab -l`), `REPLACE` — wgrano nowy (`crontab plik`), `RELOAD` — sam
`cron` wczytał zmieniony plik (przy pełnej minucie), `CMD` — `cron`
uruchomił zadanie.
*13.09: `REPLACE` o 13:03:53 UTC, `RELOAD` o 13:04:01 UTC, osiem sekund
później.*

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

### Stała
Zmienna ustawiana raz, której nikt później nie zmienia. W Pythonie nic
tego nie pilnuje, jest tylko zwyczaj: nazwy stałych pisze się WIELKIMI
literami. **Już to stosujesz** — `BASE_DIR` i `BOOTSTRAP` to stałe.
*Trzymane razem w jednym pliku (u nas `config.py`), żeby nazwa bucketa
stała w projekcie raz, a nie w sześciu miejscach.*

### Krotka (tuple)
Lista, której nie da się zmienić po utworzeniu. Zapisuje się ją
w nawiasach okrągłych zamiast kwadratowych. Elementy wyciąga się tak
samo jak z listy, przez numer w nawiasie kwadratowym.
*`wspolrzedne = (52.23, 21.01)`, potem `wspolrzedne[0]` daje `52.23`.*

### Martwy kod
Linie, których program nigdy nie wykonuje: zakomentowane bloki, wypisy
z czasu pisania, importy niczego nieużywające. Nic nie psują od razu,
ale przy kolejnej zmianie nie widać, co jest nowe, a co leży tu od
miesięcy.
*`from config import ticker` w Konsumencie — nazwa importowana i nigdy
nieużyta, bo Konsument bierze spółkę z treści wiadomości.*

### `py_compile`
`python -m py_compile plik.py` tłumaczy plik na postać wewnętrzną
i zgłasza błędy składni, ale go **nie uruchamia**. Bezpieczny sposób
sprawdzenia po edycji, także dla skryptów, których uruchomienie byłoby
groźne.
*Po skasowaniu kilku linii: brak jakiegokolwiek wypisu znaczy, że
składnia jest cała.*

### Log a przekierowanie — dwa różne pliki
`logging.basicConfig(filename=…)` kieruje wpisy z `logging.error` do
**wskazanego pliku**. Przekierowanie `>>` w `crontab` kieruje do innego
pliku to, co skrypt wypisuje przez `print`, oraz niezłapane `Traceback`.
To są dwa osobne strumienie i mogą trafiać w dwa osobne miejsca.
`basicConfig` ustawia przy tym log dla **całego** Pythona, więc do tego
samego pliku dopisują się też biblioteki.
*U nas: `logging.error` → `companies/errors.log`, `print` i `Traceback`
→ `companies/errors.txt`. Czytając wieczorem tylko drugi, nie widzisz
zgłoszonych błędów Producenta.*

### `.append()`
Dokłada element na **koniec** listy.
*`raport.append("Kraków: brak odczytu")` — lista rośnie o jedną pozycję.*

### Indeks ujemny (`[-1]`)
Liczenie od końca. `[-1]` to ostatni element, `[-2]` przedostatni.
Działa też przy przypisaniu, czyli do nadpisania ostatniej pozycji.
*`raport[-1] = "Kraków: pomiarów 3, zapisanych 2"` zamienia wartość
domyślną na prawdziwą, gdy obsługa się powiodła.*

### Wartość domyślna przed ryzykiem
Wzorzec, nie słowo kluczowe. Dokładasz do listy linię „nie udało się"
**jako pierwszą rzecz w pętli**, a dopiero potem próbujesz zrobić to, co
może się nie udać. Gdy się uda, nadpisujesz ją przez `[-1]`.
*Dzięki temu pozycja, która wypadła po drodze, zostawia po sobie ślad.
Bez tego awaria objawia się **brakiem** linii, a brak jest nie do
odróżnienia od tego, że skrypt się nie uruchomił.*

### `continue`
Przerywa bieżący obrót pętli i przechodzi do następnego. Reszta ciała
pętli w tym obrocie się nie wykona.
*Różnica wobec `break`, który wychodzi z pętli w ogóle.*

### `+=`
Skrót od „zwiększ o". `x += 1` znaczy `x = x + 1`.
*Licznik liczy tylko to, co naprawdę przeszło. `wyslane += 1` stoi
**po** potwierdzeniu wiadomości przez brokera, nie przed wysłaniem —
inaczej liczyłby zamiary zamiast faktów.*

### Wyrażenie warunkowe (jednoliniowy `if`)
`a if warunek else b` wybiera jedną z dwóch wartości w jednej linii.
To samo, co czteroliniowy `if/else` z przypisaniem.
*`stan = "zapisane" if flaga else "nietknięte"`.*

### `strftime`
Zamienia datę z godziną na tekst według wzorca. `%Y` rok czterocyfrowy,
`%m` miesiąc, `%d` dzień, `%H` godzina, `%M` minuta, `%S` sekunda.
*`datetime.now().strftime('%Y-%m-%d %H:%M:%S')` → `2026-09-11 17:45:09`.
Wzorzec w apostrofach, gdy cały f-string jest w cudzysłowach.*

### `ModuleNotFoundError`
Python mówi, że nie znalazł biblioteki o tej nazwie. Nie „biblioteka jest
zepsuta", tylko „nie ma jej w tym środowisku".
*Na EC2 `import pyarrow` daje ten błąd i **tak ma być** — ta biblioteka
jest potrzebna tylko do zapisu Parquetu, a EC2 Parquetu nie zapisuje.*

### Ostrzeżenie (`DeprecationWarning`, `UserWarning`)
Biblioteka mówi, że coś działa **dziś**, ale kiedyś przestanie albo nie
jest przetestowane. Program się nie zatrzymuje.
*Trzy takie stoją w naszym logu przy każdym biegu. Najpoważniejsze mówi,
że `boto3` przestał wspierać Pythona 3.9 od 29 kwietnia 2026 — czyli
termin już minął, a EC2 dalej ma 3.9.*

### `[3 rows x 6 columns]` — tabela ucięta
Pandas, gdy tabela nie mieści się w szerokości, chowa środkowe kolumny
pod `...` i dopisuje tę linię na końcu.
*W logu na EC2 ranking miesięczny pokazywał tylko cztery z sześciu kolumn;
od 14.09 nowy Gold ma siedem kolumn i `[3 rows x 7 columns]`. Ukryte
kolumny dalej trafiają do pliku CSV w całości — ucięcie dotyczy wyłącznie
wypisu. Gdy wypis idzie do pliku, jak w `cron`, pandas przyjmuje szerokość
80 znaków (sprawdzone 14.09 na kopii `gold.py`).*

### `how=` w `merge`
Mówi, które wiersze przeżywają sklejenie dwóch tabel. Domyślnie `inner`:
tylko te, które pasują po obu stronach. `how="right"`: wszystkie wiersze
prawej tabeli, a brakujące wartości z lewej zostają puste.
*Lewa tabela ma zwycięskie miesiące dwóch sklepów, prawa ma trzy sklepy. Bez
`how` trzeci sklep znika bez śladu, z `how="right"` zostaje z pustym
miesiącem.*

### `NaT`
Skrót od *Not a Time*: znacznik braku w kolumnie z datą albo okresem,
odpowiednik `NaN` dla liczb. Pandas dobiera znacznik do rodzaju kolumny.
W zapisanym CSV oba wychodzą jako puste pole.
*Test z 12.09 z progiem 25: miesiąc `NaT`, odchylenie i dni `NaN`.*

### Maska z kilkoma warunkami
Wybiera wiersze spełniające kilka warunków naraz. Każdy warunek we własnych
nawiasach okrągłych, między nimi `&` („i jednocześnie"). Słowo `and`
w pandas kończy się błędem.
*`t[(t["miesiac"] != t["pierwszy"]) & (t["count"] >= 15)]` — miesiące, które
nie są pierwsze i mają co najmniej 15 dni.*

### `&` między dwiema liczbami
W masce `&` znaczy „i jednocześnie". Między dwiema liczbami całkowitymi
porównuje je bit po bicie i zwraca trzecią liczbę, bez żadnego błędu.
*`114 & 108` daje `96`: `1110010` i `1101100` mają wspólne jedynki tylko na
miejscach `1100000`.*

### `sort_values` przed `groupby(...).head(1)`
`sort_values` układa wiersze w kolejności, `groupby` dzieli je na kubełki,
`head(1)` bierze pierwszy wiersz z każdego kubełka. Żeby „pierwszy" znaczył
„największy", sortowanie musi iść przed grupowaniem. Samo `head(1)` bez
`groupby` bierze jeden wiersz z całej tabeli.
*`t.sort_values(by="std", ascending=False).groupby("sklep").head(1)` —
najbardziej zmienny miesiąc każdego sklepu.*

### `rename` milczy, `drop` krzyczy
`rename` z nazwą kolumny, której nie ma, nic nie robi i nic nie mówi. `drop`
z taką nazwą przerywa skrypt błędem `KeyError`. W potoku `drop` bywa
sojusznikiem: zatrzyma skrypt, zamiast zapisać zły plik.
*`t.rename(columns={"nie_ma": "x"})` — tabela bez zmian;
`t.drop(columns=["nie_ma"])` — `KeyError`.*

### Końcówki `_x` i `_y` po `merge`
Gdy obie sklejane tabele mają kolumnę o tej samej nazwie (poza kluczem),
pandas zostawia obie i dokleja końcówki: `_x` z lewej, `_y` z prawej. Bez
błędu.
*Doklejenie tej samej tabeli drugi raz robi z `ostatnia_cena` dwie kolumny:
`ostatnia_cena_x` i `ostatnia_cena_y`.*

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

### Zmiana procentowa a zmiana ilościowa
Zmiana ilościowa to zwykłe odejmowanie: o ile złotych podrożało.
Procentową dostaje się przez podzielenie tej różnicy przez cenę
**początkową** i pomnożenie przez sto. To dzielenie zamienia „o ile
złotych" na „jaką część ceny wyjściowej stanowi ta zmiana".
Procenty **nie są symetryczne**, bo za każdym razem dzieli się przez
inną cenę początkową.
*10 zł → 15 zł to +50%, a 15 zł → 10 zł to −33%. Ta sama różnica pięciu
złotych, dwie różne liczby.*
**W tym projekcie:** kolumna `zmiana_caly_okres` w `gold/ranking.csv`
jest procentowa. XTB: 37,94 → 151,76 to +300%, bo cena końcowa jest
czterokrotnością początkowej. Nazwa kolumny nie niesie jednostki, więc
na stronie każda taka liczba będzie wymagała podpisu.

---

## Powiązane notatki

- [[Plan-ogolny]]
- [[Plan-01-bronze]]
- [[Plan-02-silver]]
- [[Plan-03-gold]]
- [[Plan-04-pokazanie-wyniku]]
- [[Plan-05-aws-migracja]]
- [[Przeglad-2026-09-08-co-nie-gra]]
