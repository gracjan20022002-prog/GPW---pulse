# Notatka projektowa — zakładka przesuwa się przed zapisem do S3

Stan: **zatwierdzona przez Gracjana 17 września 2026**, cztery decyzje niżej.
Napisana tego samego dnia, przed biegiem o 18:00.

### Kolejność prac, ustalona 17 września

1. Bieg o 18:00 i sprawdzenia o 18:15 — domknięcie naprawy „wynik Golda do
   S3 i Atheny", niezwiązane z tą notatką.
2. Test utraty na żywo, **po** udanym biegu.
3. Zmiana w `kafka_consumer.py`: `enable_auto_commit=False` **i**
   `consumer.close()` w jednym kroku. Kod pisze Gracjan.
4. Wdrożenie na EC2 po trzech powyższych.

### Wykonanie — test utraty, 17 września wieczorem

Zrobiony na EC2 po udanym biegu o 18:00, wariantem B i D z rozmowy:
zakładka cofnięta o trzy pozycje narzędziem Kafki, zapis do S3 odcięty
zmienną `AWS_ENDPOINT_URL_S3=http://localhost:1` (nic nie wychodzi na
zewnątrz, nic w AWS nie jest ruszane). **Cztery przewidywania na cztery.**

| Co | Przewidywanie | Wynik |
|---|---|---|
| plan cofnięcia (`--dry-run`) | `NEW-OFFSET 2348` | `2348` |
| stan przed biegiem | `2348  2351  3` | zgodnie |
| bieg Konsumenta | `Traceback`, brak `Odebrano` | `EndpointConnectionError`, brak `Odebrano` |
| zakładka po awarii | `2351` | `2351  2351  0` |

**Utrata potwierdzona na żywo.** Trzy wiadomości uznane za przeczytane,
zero plików w S3. Podejrzenie z 14 września jest od tej chwili faktem
zaobserwowanym, nie tylko wyczytanym z kodu.

Trzy obserwacje ponad przewidywania:

1. Wyjątek wyleciał z `put_object`, nie z `boto3.client("s3")` — klient
   powstaje bez łączenia się z siecią, więc awaria przychodzi dopiero przy
   zapisie, **za** pętlą. Dlatego automat zawsze zdąży pierwszy.
2. Padło na pierwszej spółce; dwie pozostałe nie zostały nawet spróbowane.
   Przy awarii po drugiej spółce część plików by przeszła, a zakładka i tak
   przeskoczyłaby na koniec — dziura w środku dnia, niewidoczna w logu.
3. Test nie zostawił bałaganu: zakładka wróciła na 2351, czyli tam, gdzie
   stała przed nim, bo porzucone wiadomości były już w S3 z biegu o 18:00.

**Przydatne na przyszłość:** `--reset-offsets` w Kafce 4.3.1 wymaga grupy bez
aktywnych członków, a `--dry-run` jest **domyślny** — bez `--execute`
narzędzie niczego nie zmienia. `--shift-by` przyjmuje wartości ujemne.

### Wykonanie — zmiana i dwa testy po niej, 17 września wieczorem

Kod napisał Gracjan: `enable_auto_commit=False` w konstruktorze (linia 12,
pod `auto_offset_reset`) i `consumer.close()` jako ostatnia linia pliku, za
`commit()` i za `print`. Commit `033107f`, wypchnięty na GitHub, wdrożony na
EC2 z rytuałem z zasady 14.

| Test | Co sprawdza | Przewidywanie | Wynik |
|---|---|---|---|
| **A** — zapis do S3 odcięty | zakładka **nie** rusza się | `2348  2351  3` | zgodnie |
| **B** — bieg zwykły | zakładka rusza, `close()` porządkuje | `2351  2351  0` + `no active members` od razu | zgodnie, `Odebrano 3 wiadomości` |

**Testy potwierdzają się nawzajem.** Test B odebrał trzy wiadomości, co było
możliwe tylko dzięki temu, że test A nie ruszył zakładki. Przed naprawą
wypisałby `Odebrano 0`.

**Czego jeszcze nie ma:** biegu z `cron`. Oba testy były ręczne, choć na tej
samej maszynie, tym samym Pythonem i tym samym brokerem. Pierwszym biegiem
automatycznym z nowym kodem będzie piątek 18 września o 18:00 — wtedy warunek
„działa na prawdziwej drodze danych" będzie spełniony w całości. Do tej pory
naprawa jest wdrożona i sprawdzona, ale nie przez `cron`.

**Warunek głośnej awarii pozostaje niespełniony**, tak jak przy każdej innej
pozycji w kolejce napraw.

**Koszt, zapłacony świadomie:** trzy powtórki w `live/` z testu B. Silver je
odsieje, kompakcja 1 października wypisze o trzy pliki więcej.

## Sedno w trzech zdaniach

Biblioteka `kafka-python` sama zapisuje zakładkę grupy co pięć sekund i robi
to **w trakcie** pętli odbierającej wiadomości, czyli **przed** tym, jak
Konsument zapisze cokolwiek do S3. Nasze `consumer.commit()` na końcu
skryptu nie jest więc pierwszym zapisem zakładki, tylko ostatnim — i niczego
nie chroni. Chcemy wyłączyć ten automat jednym ustawieniem, żeby zakładka
przesuwała się **tylko** po udanym zapisie do S3.

## Co jest dziś

Konsument tworzy się bez ustawienia `enable_auto_commit`, więc obowiązuje
domyślne `True` z odstępem 5000 milisekund. Pętla `for wiadomosc in consumer`
kończy się dopiero po pięciu sekundach ciszy (`consumer_timeout_ms=5000`),
a zapis do S3 stoi **za** pętlą. Automat ma więc pewność, że zdąży przed
zapisem.

Skutek: awaria zapisu do S3 nie odkłada danych na później — kasuje je.
Producent ich nie wyśle drugi raz, bo ma własną pamięć w `companies/*.txt`
i widzi ten dzień jako wysłany.

**To nie jest teoria.** Podejrzenie zapisano 14 września jako niesprawdzone;
17 września potwierdzone w kodzie biblioteki (dowody niżej). Nie zostało
zaobserwowane na żywo — to osobny test, opisany w części „Jak sprawdzimy".

## Kształt na innych danych

Lodziarnia zbiera zamówienia z kolejki i przepisuje je do zeszytu na dysku.
Konsument wygląda tak samo jak nasz, z jedną linią więcej:

```python
konsument = KafkaConsumer(
    bootstrap_servers=["localhost:9092"],
    group_id="lodziarnia",
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    consumer_timeout_ms=5000
)
zamowienia = []
for w in konsument:
    zamowienia.append(w.value)
with open("zeszyt.txt", "a", encoding="utf-8") as plik:
    for z in zamowienia:
        plik.write(str(z) + "\n")
konsument.commit()
```

**Wejście.** W kolejce trzy karteczki, zakładka grupy `lodziarnia` stoi
na `10`:

```
{"smak": "czekolada", "galki": 2}
{"smak": "sorbet", "galki": 1}
{"smak": "wafel", "galki": 3}
```

**Wyjście, gdy zapis się udaje.** Zawartość `zeszyt.txt`:

```
{'smak': 'czekolada', 'galki': 2}
{'smak': 'sorbet', 'galki': 1}
{'smak': 'wafel', 'galki': 3}
```

Zakładka: `13  13  0`.

**Wyjście, gdy zapis zawiedzie** — dysk pełny, brak uprawnień do pliku:

```
Traceback (most recent call last):
  ...
OSError: [Errno 28] No space left on device
```

`zeszyt.txt` bez zmian, zakładka **dalej `10`**. Nazajutrz te same trzy
karteczki przychodzą ponownie i dostają drugą szansę.

**Bez linii `enable_auto_commit=False`** drugi przypadek kończy się inaczej:
zeszyt pusty, zakładka `13`. Karteczki przepadły na zawsze.

### Przykład → projekt

| Przykład | Nasz projekt |
|---|---|
| `zeszyt.txt` | folder `live/spolka=…/` w S3 |
| `plik.write(...)` | `s3.put_object(...)` |
| dysk pełny | S3 nie odpowiada, wygasłe uprawnienia, brak sieci |
| `group_id="lodziarnia"` | `group_id='gpw_consumer'` |
| trzy karteczki | trzy wiadomości, po jednej na spółkę |
| zakładka `10` na `13` | zakładka grupy, dziś 2348 |

## Dwa nowe pojęcia

- **Dostarczenie co najwyżej raz** — wiadomość albo dojdzie, albo przepadnie,
  ale nigdy się nie zdubluje. Tak zachowuje się Konsument dziś.
- **Dostarczenie co najmniej raz** — wiadomość dojdzie na pewno, ale może
  dojść dwa razy. To wybieramy, wyłączając automat.

Trzeciej możliwości — „dokładnie raz" — w tym kształcie nie ma i nie jest
potrzebna, bo Silver odsiewa powtórki.

## Dowód z kodu biblioteki

Wszystko przeczytane 17 września w `kafka-python 3.0.11` zainstalowanej
w `.venv` na laptopie. **Ta sama wersja stoi w obu spisach wymagań**,
lokalnym i EC2, więc EC2 zachowuje się tak samo.

1. `kafka/consumer/group.py`, domyślne ustawienia: `enable_auto_commit`
   równa się `True`, `auto_commit_interval_ms` równa się 5000.
2. `kafka/coordinator/consumer.py`, wewnątrz `poll()`: wywołanie
   `_maybe_auto_commit_offsets_async()`. Zapis zachodzi więc w trakcie pętli
   po wiadomościach, nie po niej.
3. Ten sam plik, zegar automatu: przy dołączeniu do grupy nastawiany na
   „teraz plus pięć sekund", po każdym zapisie nastawiany ponownie.
4. **Trzecie miejsce zapisu:** `close()` woła
   `_maybe_auto_commit_offsets_sync`, a ta sprawdza ten sam przełącznik.
   Znaczy to, że przy włączonym automacie dopisanie `consumer.close()`
   dodałoby czwarty ukryty zapis zakładki, a po wyłączeniu automatu
   `close()` jest nieszkodliwy.

Punkt 4 wiąże tę notatkę z drugim drobiazgiem z 14 września (Konsument bez
`close()`, broker widzi martwego członka grupy). **Kolejność ma znaczenie:
najpierw wyłączyć automat, potem dopisywać `close()`.**

## Co zmieniamy

Jedno ustawienie w konstruktorze Konsumenta: `enable_auto_commit=False`.
Nic więcej — `consumer.commit()` na końcu skryptu już jest napisane i po tej
zmianie staje się jedynym zapisem zakładki.

Kod pisze Gracjan. Notatka nie podaje numeru linii ani gotowej linijki; to
idzie do kroków po zatwierdzeniu.

## Co może pójść źle

- **Powtórki w `live/`.** Gdy `commit()` nie wykona się, nazajutrz przyjdą
  te same wiadomości i wylądują w S3 po raz drugi.
- **Powtórka częściowa.** Gdy `put_object` uda się dla CBF, a padnie dla SNT,
  `commit()` nie wykona się wcale i nazajutrz powtórzą się wszystkie trzy
  spółki, nie tylko SNT.
- **Awaria samego `commit()`.** Broker może nie odpowiedzieć na zapis
  zakładki; wtedy `Traceback` idzie do `errors.txt`, a bieg zostawia dane
  w S3 i nieprzesuniętą zakładkę — czyli powtórkę nazajutrz.
- **Kompakcja 1 października wypisze więcej usuniętych plików**, o tyle, ile
  powtórek zdążyło powstać.
- **Zmiana wymaga wdrożenia na EC2**, czyli kolejnego `git pull` z rytuałem
  z zasady 14. Sam kod na laptopie niczego nie naprawia.
- **Zależność, którą trzeba znać:** bezpieczeństwo tej zmiany stoi na
  odsiewaniu powtórek w Silverze. Gdyby ktoś je usunął, duplikaty zaczęłyby
  po cichu zawyżać dane.

### Dlaczego powtórki są bezpieczne — dwie warstwy, nie jedna

Silver ma dwa niezależne sita:

1. **`UNION` w zapytaniu do Atheny** (nie `UNION ALL`) — sam SQL usuwa
   wiersze identyczne we wszystkich trzech kolumnach.
2. **`drop_duplicates` po dniu i spółce** — usuwa też takie powtórki,
   w których cena się różni, zostawiając pierwszą.

Powtórka identyczna ginie więc dwukrotnie. **Mamy na to dowód z 14
września:** test zakładki wrzucił do `live/` trzy pliki powtórek, a Silver
policzył tyle samo wierszy co przed testem, z tą samą sumą kontrolną pliku.

Uwaga na przyszłość: gdy powtórka ma **inną** cenę niż pierwotny wpis
(korekta u Yahoo), sito numer 2 zostawia jedną z dwóch i nie mówi, którą.
To istniejąca wada z przeglądu, nie skutek tej zmiany.

## Jak sprawdzimy

### Przed zmianą — utrata na żywo

Test na EC2, z ręcznego biegu, nie z `cron`:

1. Odczyt zakładki grupy przed biegiem.
2. Ręczny bieg Konsumenta z celowo zepsutym zapisem do S3, na przykład
   z nieistniejącą nazwą kubełka podaną przez zmienną środowiskową.
3. Oczekiwane: `Traceback`, brak nowych plików w `live/`, a zakładka
   **przesunięta** mimo braku zapisu.

Ten test dowodzi utraty. Bez niego mamy dowód z kodu, ale nie z maszyny.

**Uwaga:** test przesuwa zakładkę, czyli świadomie porzuca wiadomości. Robić
go **tylko** wtedy, gdy w topicu nie ma nic, czego nie ma jeszcze w S3 —
najbezpieczniej zaraz po udanym biegu o 18:00.

### Po zmianie — że naprawa działa

1. Ten sam test z zepsutym zapisem. Oczekiwane: `Traceback`, brak nowych
   plików, a zakładka **stoi w miejscu**.
2. Zwykły bieg, bez psucia. Oczekiwane: pliki w `live/`, zakładka
   przesunięta, `Odebrano N wiadomości`.
3. Silver po powtórce: liczba wierszy bez zmian.

### Liczba linii w logu

Zmiana nie dodaje ani nie ujmuje żadnej linii wypisu, więc normalny blok
zostaje taki jak dziś. Gdyby się zmienił, znaczyłoby to, że zmieniło się coś
jeszcze.

## Decyzje — podjęte 17 września

1. **Wyłączamy automat.** Ciche gubienie danych zamienione na okazjonalne
   powtórki, które Silver i tak odsiewa.
2. **Test utraty na żywo robimy, po udanym biegu o 18:00** — wtedy topic jest
   już przepisany do S3 i porzucenie wiadomości niczego nie kosztuje.
3. **`consumer.close()` idzie w tej samej zmianie**, wbrew propozycji z tej
   notatki. Powód: jedno wdrożenie na EC2 zamiast dwóch, czyli jedno okno
   ryzyka zamiast dwóch. Koszt opisany niżej.
4. **Wdrożenie na EC2 po trzech powyższych.**

### Co wynika z decyzji 3

Obie zmiany są jednolinijkowe i niezależne, a `close()` przy wyłączonym
automacie jest nieszkodliwy — sprawdza ten sam przełącznik i nic nie
commituje. Ryzyko jest więc małe, ale bieg testowy po zmianie musi dowieść
**dwóch** rzeczy naraz, nie jednej:

- zakładka **nie** przesuwa się, gdy zapis do S3 zawiedzie;
- grupa `gpw_consumer` **nie** ma martwego członka zaraz po zakończeniu biegu
  (to sprawdza `close()`; 14 września wyszło odwrotnie — członek wisiał na
  liście wbrew przewidywaniu Claude'a).

Gdyby coś poszło nie tak, trzeba będzie rozdzielić zmiany, żeby ustalić którą.

**Poprawka po napisaniu kodu, 17 września wieczorem.** Powyższe „bieg testowy
musi dowieść dwóch rzeczy naraz" jest nie do wykonania jednym biegiem.
`consumer.close()` stoi w ostatniej linii, a `put_object` wcześniej — więc
przy zepsutym zapisie program pada, zanim dojdzie do `close()`. Sprawdzenia
trzeba rozdzielić:

- **bieg z zepsutym zapisem** sprawdza tylko zakładkę (ma zostać w miejscu);
  wiszący członek grupy jest w tym biegu **oczekiwany**, bo `close()` się nie
  wykonuje;
- **bieg udany** sprawdza `close()` — grupa ma pokazać `no active members`
  od razu po zakończeniu, bez czekania kilkunastu sekund.

Wniosek ogólniejszy, wart zapamiętania: `close()` porządkuje połączenie
wyłącznie na ścieżce, która się udaje. Pełne rozwiązanie wymagałoby `finally`,
czyli nowej konstrukcji w kodzie. Korzyść byłaby znikoma — wiszący członek
nie gubi danych, tylko blokuje na moment operacje wymagające nieaktywnej
grupy, jak `--reset-offsets`. Świadomie odłożone.

## Co to zepsuje za miesiąc

Nic w kodzie. Za miesiąc może za to zdziwić `Usunięto N plików` przy
kompakcji — liczba będzie wyższa od liczby dni, jeśli w międzyczasie powstały
powtórki. To nie awaria.

Druga rzecz: po tej zmianie nieudany bieg przestaje być niewidoczny
w danych, ale nadal jest niewidoczny dla człowieka. Powtórka nazajutrz
naprawi dane sama i nikt się nie dowie, że coś się nie udało.

## Czego ta zmiana nie naprawia

- **Awaria zostaje cicha.** `Traceback` idzie do `errors.txt`, którego nikt
  nie czyta. To punkt 8 kolejki napraw.
- **Nie naprawia okna na kurs zamknięcia u Yahoo** ani ceny z trwającej
  sesji przy biegu przed 17:00.
- **Nie naprawia korekt cen**, które nie docierają do S3.
- **Nie dotyczy Producenta** — on ma własne zabezpieczenie od 8 września,
  zapis pamięci wyłącznie po potwierdzeniu brokera.

## Powiązane notatki

- `Notatka-2026-09-14-test-zakladki.md` — stamtąd pochodzi podejrzenie
  i dowód, że powtórki nie psują Silvera.
- `Przeglad-2026-09-08-co-nie-gra.md` — źródło prawdy o wadach i kolejności
  napraw; ta notatka dotyczy wady dopisanej 14 września.
- `Notatka-2026-09-15-wynik-golda-do-s3.md` — naprawa domykana dzisiaj,
  niezależna od tej.
