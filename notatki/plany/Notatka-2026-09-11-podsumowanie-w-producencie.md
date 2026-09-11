# Notatka projektowa — podsumowanie w Producencie

**Data:** 11 września 2026
**Dotyczy:** `kod/data_ingestion.py`
**Skąd to się wzięło:** punkt 2.1 przeglądu z 8 września; zdjęte z planu
10 września, bo sprawdzenie wymagało żywego brokera, a tamtego wieczoru
broker miał potwierdzać co innego.
**Status:** zatwierdzona przez Gracjana 11 września. Wszystkie cztery
decyzje z części 6 rozstrzygnięte zgodnie z rekomendacją. Kod pisany
tego samego dnia, lokalnie; na EC2 najwcześniej w następnej sesji.

---

## 1. Co Producent wypisuje dziś

Cztery linie na bieg, zawsze tyle samo, niezależnie od tego, co się
wydarzyło.

Pierwsza pochodzi z linii 9 pliku i jest ścieżką do samego skryptu:

```
/home/ec2-user/GPW---pulse/kod/data_ingestion.py
```

Kolejne trzy pochodzą z linii 50, po jednej na spółkę, i są adresem,
pod który poszło zapytanie do Yahoo:

```
https://query1.finance.yahoo.com/v8/finance/chart/CBF.WA?range=3y&interval=1d
https://query1.finance.yahoo.com/v8/finance/chart/XTB.WA?range=3y&interval=1d
https://query1.finance.yahoo.com/v8/finance/chart/SNT.WA?range=3y&interval=1d
```

Wypis adresu stoi wewnątrz gałęzi `if response.status_code == 200`, więc
jego obecność faktycznie coś znaczy: Yahoo odpowiedziało i odpowiedziało
poprawnie.

---

## 2. Czego te cztery linie nie mówią

Trzech rzeczy, i każda z nich jest ważniejsza niż to, co linie mówią.

**Ile dni było nowych.** Producent trzyma pamięć w `companies/CBF.WA.txt`
i dwóch podobnych plikach. Z Yahoo przychodzą trzy lata notowań za każdym
razem, ale do Kafki idą wyłącznie dni, których w pamięci jeszcze nie było.
W zwykły dzień giełdowy to jeden dzień na spółkę. Po weekendzie zero.
Po tygodniu przerwy pięć. Z logu nie widać której sytuacji.

**Ile wiadomości broker faktycznie potwierdził.** Od 8 września Producent
zapisuje pamięć dopiero po potwierdzeniu każdej wiadomości. Gdy broker
odmówi, pamięć zostaje nietknięta, a wpis o błędzie idzie przez
`logging.error` do `companies/errors.log`. To **nie jest** ten plik, który
czytamy wieczorem. Wieczorem czytamy `companies/errors.txt`, bo tam `cron`
przekierowuje wypisy. Cztery obecne linie wyglądają tak samo w dniu udanym
i w dniu, w którym broker odrzucił wszystko.

**Czy pamięć została zapisana.** To jest ta sama informacja co wyżej,
widziana od strony skutków. Jeśli pamięć nie została zapisana, jutro
Producent wyśle te dni jeszcze raz.

Dziś jedynym śladem awarii w pliku, który czytamy, jest `Odebrano 0
wiadomości` od Konsumenta zamiast `Odebrano 3`. To sygnał pośredni i
działa tylko wtedy, gdy padnie wszystko naraz. Gdy padnie jedna spółka
z trzech, zobaczymy `Odebrano 2` i nie dowiemy się, która.

---

## 3. Po co to zmieniamy

Żeby w pliku, który i tak czytamy co wieczór, stała odpowiedź na jedno
pytanie: **czy dzisiejsze dane dojechały do Kafki, dla wszystkich trzech
spółek.**

To nie jest sygnał awarii w sensie powiadomienia. Nikt nas nie obudzi.
To jest zamiana czterech linii, które zawsze wyglądają tak samo, na trzy,
które wyglądają inaczej, gdy coś poszło źle. Prawdziwy sygnał awarii to
osobny krok, ósmy w kolejności z przeglądu.

---

## 4. Co ma wypisywać — propozycja

Jedna linia na spółkę, po zakończeniu całej pętli, nie w jej trakcie.
Plus jedna linia startowa na początku.

Dzień zwykły, wszystko poszło:

```
=== Producent start: 2026-09-12 16:00:04 ===
CBF.WA: nowych 1, wysłanych 1, pamięć zapisana
XTB.WA: nowych 1, wysłanych 1, pamięć zapisana
SNT.WA: nowych 1, wysłanych 1, pamięć zapisana
```

Weekend albo drugi bieg tego samego dnia:

```
CBF.WA: nowych 0, wysłanych 0, pamięć zapisana
```

Broker nie odpowiada:

```
CBF.WA: nowych 1, wysłanych 0, pamięć nietknięta
```

Broker padł w połowie spółki, przy nadrabianiu zaległości:

```
CBF.WA: nowych 5, wysłanych 3, pamięć nietknięta
```

Yahoo nie odpowiedziało albo odpowiedziało błędem:

```
CBF.WA: nie pobrano danych
```

**Zasada czytania jednym spojrzeniem:** dwie pierwsze liczby mają być
równe. Gdy się różnią, coś nie dojechało. Gdy druga jest zerem przy
niezerowej pierwszej, nie dojechało nic.

### Dlaczego „pamięć nietknięta" przy trzech wysłanych z pięciu to nie błąd

Te trzy wiadomości naprawdę leżą w Kafce. Pamięć jednak nie zostaje
zapisana, bo zapisujemy ją tylko wtedy, gdy poszło **wszystko**. Nazajutrz
Producent wyśle wszystkie pięć dni od nowa i trzy z nich będą powtórką.
To jest bezpieczne: Silver usuwa duplikaty po parze dzień plus spółka,
a kompakcja 1 października i tak zostawi po jednym wierszu. Lepiej wysłać
dwa razy niż zgubić raz. Warto, żeby to stało w notatce, bo przy czytaniu
logu „nietknięta" obok niezerowej liczby wysłanych wygląda na sprzeczność.

---

## 5. Kształt na innych danych

Najważniejsza zmiana nie dotyczy treści linii, tylko **momentu**, w którym
się je wypisuje. Dziś adres Yahoo wypisuje się w środku obsługi spółki.
Jeśli spółka wypadnie wcześniej, nie wypisze się nic i spółka zniknie
z logu bez śladu.

Rozwiązanie: zbierać wyniki do listy, a wypisać po pętli. Wtedy każda
pozycja dostaje linię zawsze, także ta, która się nie udała.

Lodziarnia z trzema smakami. Wanilia się udała, czekolady nie policzono,
pistacji nie udało się wydać.

**Wejście — kod:**

```python
smaki = ["wanilia", "czekolada", "pistacja"]
podsumowanie = []

for smak in smaki:
    podsumowanie.append(f"{smak}: nie policzono")   # wartość domyślna
    if smak == "czekolada":
        continue                                     # licznika nie ma, zostaje domyślna
    nowe = 5
    wydane = 5 if smak == "wanilia" else 0
    stan = "zapisany" if nowe == wydane else "nietknięty"
    podsumowanie[-1] = f"{smak}: nowych {nowe}, wydanych {wydane}, stan {stan}"

for linia in podsumowanie:
    print(linia)
```

**Wyjście — to, co pojawi się na ekranie:**

```
wanilia: nowych 5, wydanych 5, stan zapisany
czekolada: nie policzono
pistacja: nowych 5, wydanych 0, stan nietknięty
```

Trzy nowe rzeczy w tym kształcie, każda po kolei.

`podsumowanie = []` tworzy pustą listę. Zbieramy do niej linie zamiast
wypisywać je od razu.

`.append(...)` dokłada element na koniec listy. Robimy to **jako
pierwszą rzecz w pętli**, z wartością domyślną mówiącą „nie udało się".
Dzięki temu każda pozycja ma linię, zanim cokolwiek może pójść źle.

`podsumowanie[-1] = ...` nadpisuje **ostatni** element listy. Minus jeden
to indeks liczony od końca. Gdy wszystko się uda, zamieniamy wartość
domyślną na prawdziwą. Gdy nie, domyślna zostaje i widać ją w wyjściu.

`continue` przerywa bieżący obrót pętli i przechodzi do następnego.
Tu udaje spółkę, której nie udało się pobrać.

To samo dałoby się zrobić słownikiem zamiast listą. Lista wystarczy, bo
kolejność spółek w `ticker` i tak jest stała i chcemy ją zachować.

---

## 6. Decyzje do podjęcia przed kodem

Cztery. Przy każdej moja rekomendacja i powód, ale wybiera Gracjan.

> **Rozstrzygnięte 11 września.** Gracjan przyjął wszystkie cztery
> rekomendacje: linia startu z datą i godziną zamiast ścieżki, dwie
> liczby plus stan pamięci, bez linii z sumą, linia zawsze — także gdy
> nic nowego nie ma. Skutek dla długości bloku w logu: bez zmian,
> cztery linie za cztery.

### Decyzja 1 — co z linią ścieżki

Dziś pierwszą linią bloku jest ścieżka do skryptu. Wczoraj miała
konkretne zadanie: udowodnić, że przekierowanie do pliku łapie Producenta,
a nie tylko Konsumenta. Udowodniła i to zadanie się skończyło.

- **Zostawić jak jest.** Zero pracy, zero ryzyka, ale linia nic już nie
  wnosi.
- **Zamienić na linię startu z datą i godziną.** Zyskujemy znacznik
  początku bloku w pliku, który rośnie bez końca i nie ma dziś żadnego
  podziału na dni. Dziś, żeby znaleźć wczorajszy bieg, trzeba wiedzieć,
  ile linii ma blok. Po zmianie wystarczy `grep` po dacie.
- **Usunąć.** Blok krótszy o linię, ale bez znacznika początku.

**Rekomendacja: zamienić na linię startu z datą i godziną.** Kosztuje
tyle samo linii co obecna ścieżka, a daje coś, czego dziś nie ma.

**Pułapka do tej decyzji:** `datetime.now()` na EC2 zwraca czas
uniwersalny, bo taka jest strefa tej maszyny. W linii startu stanie więc
`16:00`, a nie `18:00`, mimo że bieg jest o osiemnastej polskiej. To nie
jest błąd, ale trzeba o tym wiedzieć przy czytaniu, i zmieni się samo
w dniu, w którym zrobimy `CRON_TZ`.

### Decyzja 2 — co liczymy

- **Dwie liczby i stan pamięci** — nowych, wysłanych, zapisana lub
  nietknięta.
- **Trzy liczby** — dodatkowo ile dni w ogóle przyszło z Yahoo.

**Rekomendacja: dwie liczby i stan.** Liczba dni z Yahoo to zawsze mniej
więcej tyle samo, około 750, i nic nie mówi. Trzecia liczba, która nigdy
się nie zmienia, uczy oko, żeby przestać patrzeć na całą linię.

### Decyzja 3 — czy dokładać linię z sumą

- **Bez sumy.** Trzy linie, każda czytelna.
- **Z sumą**, na przykład `Razem: nowych 3, wysłanych 3`.

**Rekomendacja: bez sumy, na razie.** Przy trzech spółkach suma powtarza
to, co widać. Wróćmy do niej, gdy spółek będzie więcej niż pięć.

### Decyzja 4 — czy wypisywać linię, gdy nie ma nic nowego

- **Tak, zawsze.**
- **Nie, milczeć.**

**Rekomendacja: tak, zawsze.** Brak linii jest nie do odróżnienia od
sytuacji, w której skrypt w ogóle się nie uruchomił. To jest dokładnie ten
rodzaj ciszy, przez który powstała wrześniowa lista wad.

---

## 7. Co może pójść źle

**Broker martwy od początku.** `producer` jest wtedy ustawiony na `None`
i pętla wysyłki w ogóle nie rusza. Podsumowanie ma pokazać niezerową
liczbę nowych i zero wysłanych dla każdej spółki. To jest największy zysk
z całej zmiany: dziś ta sytuacja nie zostawia w `errors.txt` żadnego
śladu poza `Odebrano 0` od Konsumenta.

**Broker pada w trakcie.** Licznik wysłanych zatrzymuje się w połowie.
Podsumowanie ma pokazać liczby różne, a nie przerwać się w połowie linii.

**Nie ma nowych dni.** Weekend, święto, drugi bieg tego samego dnia.
Zero nowych i zero wysłanych to sukces, nie awaria. Linia musi pokazywać
**obie** liczby, bo samo „wysłano 0" byłoby nieczytelne. Uwaga dodatkowa:
w tym przypadku pamięć i tak zostaje przepisana tą samą treścią, bo pętla
wysyłki się nie wykonuje i flaga zostaje prawdziwa. Napis „pamięć
zapisana" jest wtedy zgodny z prawdą, choć plik się nie zmienia.

**Yahoo nie odpowiada albo zwraca błąd.** Spółka nigdy nie dochodzi do
miejsca, w którym liczymy nowe dni. Dlatego domyślna linia musi powstać
**przed** pobieraniem, a nie po. Inaczej spółka zniknie z podsumowania
i trzeba by liczyć linie, żeby to zauważyć.

**Limit czasu w pobieraniu zadziała.** Od wczoraj `requests.get` ma
`timeout = (10, 30)`. Przy zerwanym połączeniu spółka wpada w ten sam
`except` co powyżej i dostaje linię „nie pobrano danych".

**Dochodzi czwarta spółka.** W kodzie nie może stać nigdzie liczba trzy.
Pętla po `ticker` i długość listy z podsumowaniem załatwiają to same.
Zmieni się natomiast długość bloku w logu i trzeba będzie przeliczyć
przewidywania na ten wieczór.

**Zmienia się długość bloku w `errors.txt`.** To nie jest awaria, ale
psuje sprawdzenie, jeśli się o tym zapomni. Liczbę linii trzeba policzyć
**przed** pierwszym biegiem z nową wersją, tak jak dziś.

**Podsumowanie może kłamać.** Licznik wolno zwiększać wyłącznie
**po** potwierdzeniu wiadomości przez brokera, czyli po tym, jak
`.get(timeout=10)` wróci bez wyjątku. Zwiększany przed wysłaniem liczyłby
zamiary, a nie fakty, i to byłaby gorsza wada niż ta, którą naprawiamy.

**Polskie znaki.** Plik `errors.txt` już dziś zawiera „Odebrano 3
wiadomości" i wyświetla się poprawnie, więc nowe linie z „pamięć" i
„wysłanych" też będą dobre. Sprawdzimy to mimochodem przy pierwszym
biegu.

---

## 8. Jak to sprawdzimy

Dwa testy. Pierwszy pokazuje, że podsumowanie **widzi awarię**. Drugi, że
**nie przeszkadza** w zwykłym dniu. Sam pierwszy albo sam drugi niczego by
nie dowiódł.

### Test 1 — lokalnie, z martwym brokerem

Ten test można zrobić od razu po napisaniu kodu, bez EC2.

Lokalna pamięć Producenta kończy się na **1 września 2026** i każdy z
trzech plików ma **762 wiersze**. Policzone dzisiaj, nie wzięte z notatek.

Dni giełdowych od 2 do 11 września jest osiem: 2, 3, 4, 7, 8, 9, 10 i 11.
Piąty i szósty to weekend. Świąt w tym oknie nie ma.

**Przewidywane wyjście:**

```
CBF.WA: nowych 8, wysłanych 0, pamięć nietknięta
XTB.WA: nowych 8, wysłanych 0, pamięć nietknięta
SNT.WA: nowych 8, wysłanych 0, pamięć nietknięta
```

**Przewidywany stan plików po teście:** dalej po 762 wiersze, bez zmian.
To jest druga połowa dowodu i trzeba ją policzyć osobno.

Jeśli w liniach stanie siedem zamiast ośmiu, znaczy to, że Yahoo nie
zwróciło jeszcze świecy za dzień bieżący. To nie jest błąd podsumowania.
Jeśli stanie cokolwiek innego, zatrzymujemy się i patrzymy dlaczego.

Adres martwego brokera bierzemy ten sam co wczoraj, czyli `127.0.0.1:9092`,
przez zmienną `KAFKA_BOOTSTRAP`.

### Wynik testu 1 — wykonany 11 września o 17:45, zdany

Wyjście na ekranie:

```
=== Godzina pomiaru Producenta: 2026-09-11 17:45:09 ===
CBF.WA: nowych dni: 7, wysłane: 0, stan: nietknięte
XTB.WA: nowych dni: 7, wysłane: 0, stan: nietknięte
SNT.WA: nowych dni: 7, wysłane: 0, stan: nietknięte
```

Trzy sprawdzenia, trzy trafione.

**Pamięć nietknięta.** Pliki spółek dalej po 762 wiersze, mimo że skrypt
znalazł siedem nowych dni. Naprawa z 8 września działa, a podsumowanie
jej nie obeszło.

**`errors.log` urósł o cztery**, z 50 na 54, zgodnie z przewidywaniem.
Trzy z tych linii pisze biblioteka `kafka`, jedna nasz kod.

**Podsumowanie wypisało trzy linie**, po jednej na spółkę, i każda niesie
obie liczby oraz stan pamięci.

### Dlaczego siedem, a nie osiem

Przewidywałem osiem dni, wyszło siedem, i to nie jest błąd kodu. Dowód
jest niezależny: 10 września wieczorem pliki spółek na EC2 miały 769
wierszy, lokalne mają 762. Różnica wynosi siedem, a pamięć EC2 sięga
10 września włącznie. Skrypt znalazł więc dokładnie dni od 2 do 10
września.

Wniosek: **11 września o 17:45, czyli czterdzieści pięć minut po
zamknięciu GPW, Yahoo nie oddawało jeszcze świecy za ten dzień**
w postaci nadającej się do użycia, albo oddawało ją z pustą ceną
zamknięcia, którą kod pomija warunkiem `c is not None`.

To jest obserwacja o samym źródle danych, nie o podsumowaniu, ale ma
konsekwencje dla pory biegu i trafia stąd do przeglądu. Bieg `cron`
wypada o 18:00 czasu polskiego, czyli piętnaście minut po tym teście.
Wieczór 11 września rozstrzygnie, czy ten kwadrans wystarcza.

**Uwaga do liczenia:** `errors.log` przy martwym brokerze urośnie o
**cztery** linie na bieg, nie o jedną. Trzy z nich pisze sama biblioteka
`kafka`, bo `logging.basicConfig` ustawia zapis do pliku dla wszystkiego,
co w tym programie zgłasza błąd, nie tylko dla naszego kodu. Widać to
w lokalnym `errors.log` z 10 września.

### Test 2 — na EC2, zwykłym biegiem `cron`

Tu jest sedno i powód, dla którego ta zmiana czekała od wczoraj.

**Czego nie wolno zrobić:** uruchomić Producenta lokalnie z żywym
brokerem. Lokalna pamięć kończy się 1 września, więc poszłoby do Kafki
osiem dni razy trzy spółki, czyli dwadzieścia cztery wiadomości.
Wieczorny Konsument wypisałby `Odebrano 27` zamiast `Odebrano 3` i
zepsułby każde sprawdzenie tego dnia.

**Co zrobić zamiast tego:** wgrać kod na EC2 przez `git pull` i pozwolić
zadziałać zwykłemu biegowi o 18:00. Na EC2 pamięć jest bieżąca, więc
nowy dzień jest dokładnie jeden na spółkę. Żadnego zalewu.

**Przewidywane wyjście w `errors.txt`:**

```
CBF.WA: nowych 1, wysłanych 1, pamięć zapisana
XTB.WA: nowych 1, wysłanych 1, pamięć zapisana
SNT.WA: nowych 1, wysłanych 1, pamięć zapisana
```

oraz, niżej w tym samym bloku, niezmienione `Odebrano 3 wiadomości`.

**Przewidywana długość bloku:** bez zmian wobec dziś, jeśli przyjmiemy
rekomendację z decyzji 1 i 3. Znika jedna linia ścieżki i trzy adresy
Yahoo, przychodzi jedna linia startu i trzy linie spółek. Cztery za
cztery. Jeśli którakolwiek decyzja pójdzie inaczej, liczbę trzeba
przeliczyć przed biegiem.

**Czego test 2 nie udowodni:** ścieżki awaryjnej. Broker na EC2 działa,
więc zobaczymy tylko linie sukcesu. Ścieżkę awaryjną pokrywa test 1.

### Warunek terminu

Testu 2 nie robimy w dniu, w którym inny bieg ma coś potwierdzać. Dziś
wieczorem potwierdzamy sprzątanie kodu, więc najwcześniejszy możliwy
termin to następna sesja.

---

## 9. Co to zepsuje za miesiąc

**Liczba linii w bloku przestanie się zgadzać ze starymi notatkami.**
Wpisy dziennika z 9, 10 i 11 września mówią o czterech liniach Producenta
i o adresach Yahoo. Po zmianie te opisy będą historią, nie stanem.
Przegląd trzeba zaktualizować w tej samej sesji, w której kod trafi na
EC2.

**Zniknie jedyne miejsce, w którym widać adres zapytania do Yahoo.**
Dziś, gdyby zakres `range=3y` albo interwał kiedyś się zmieniły, widać by
to było w logu. Po zmianie nie. Adres stoi jednak w kodzie i nikt go nie
zmienia w locie, więc uznaję to za koszt do przyjęcia. Warto o tym
pamiętać przy debugowaniu pobierania.

**Kompakcja 1 października nic tu nie zmienia.** Sprawdzone w kodzie:
`compaction.py` czyta Athenę i pisze do S3, a folderu `companies`
nie dotyka w żadnym miejscu. Pamięć Producenta i podsumowanie są od niej
niezależne.

**`CRON_TZ` zmieni godzinę w linii startu.** Dziś stanęłoby tam `16:00`,
po zmianie strefy `18:00`. To jest oczekiwane i będzie pierwszym widocznym
dowodem, że strefa weszła.

---

## 10. Czego ta zmiana nie naprawia

Piszę to osobno, żeby nie uznać jej za większą, niż jest.

- **Nie powiadamia.** Trzeba nadal otworzyć plik i przeczytać.
- **Nie naprawia podwójnego logu.** `logging.error` dalej pisze do
  `errors.log`, którego wieczorem nie czytamy. Podsumowanie zmniejsza
  szkodę, bo stawia liczby w tym drugim pliku, ale nie zamyka wady.
- **Nie naprawia ceny z trwającej sesji.** Producent uruchomiony przed
  17:00 nadal zapisze bieżącą cenę jako kurs zamknięcia. Podsumowanie
  policzy taki dzień jako poprawnie wysłany, bo z jego punktu widzenia
  był.
- **Nie zmienia niczego w Konsumencie, Silverze ani Goldzie.**

---

## Powiązane notatki

- [[Przeglad-2026-09-08-co-nie-gra]] — punkt 2.1, źródło tej pozycji
- [[Notatka-2026-09-10-sprzatanie-kodu]] — tam ta zmiana została zdjęta
  z zakresu i dlaczego
- [[Slownik]] — `flaga`, `append`, indeks ujemny, `continue`
