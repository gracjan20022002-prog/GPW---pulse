# Notatka projektowa — `CRON_TZ` i godziny biegów jednym ruchem

Napisana 13 września 2026, **przed zmianą**, zgodnie z zasadą numer 10
z `CLAUDE.md`. Kolejność: Gracjan czyta, zatwierdza albo zmienia decyzje
z części 8, dopiero potem ruszamy `crontab`.

**Status: zatwierdzona i wykonana 13 września.** Gracjan zatwierdził
wszystkie cztery decyzje z części 8 zgodnie z rekomendacją, około 14:40.
Harmonogram wgrany o 15:03 czasu polskiego.

**Sprawdzone 14 września.**
- Wieczorny bieg z 13 września: linia 462, `16:00:02`, `errors.txt` 482,
  blok 21.
- Bieg w dzień giełdowy 14 września: linia 483, `16:00:02`, `errors.txt`
  506, blok 24. Blok jest o jedną linię dłuższy niż w części 10, bo przed
  biegiem na EC2 trafił nowy Gold.

To jeszcze nie jest „zrobione". Brakuje pierwszego biegu po zmianie czasu
(26 października) i sygnału o awarii.

### Wykonanie, 13 września

Godziny w nawiasach po polsku, poza nawiasami tak, jak wypisała maszyna.

| Krok | Wynik | Zgodne z przewidywaniem |
|---|---|---|
| kopie w katalogu domowym | `crontab-kopia-0909.txt` (642 bajty) i `crontab-nowy.txt` z 9 września (633 bajty); żadnego pliku z `0913` | tak |
| kopia dzisiejszego harmonogramu | `crontab -l` o 12:47:14 UTC (14:47), w dzienniku systemowym wpis `LIST` | tak |
| nazwa strefy, **przed** wgraniem | `13:03 UTC` i `15:03 CEST` | tak |
| `diff` kopii z nowym plikiem | osiem linii, znak w znak jak w symulacji; porównane `diff`-em, nie na oko | tak |
| wgranie | bez wypisu; w dzienniku `REPLACE` o 13:03:53 UTC (15:03:53) | tak |
| porównanie maszyny z plikiem | `diff ~/crontab-nowy-0913.txt <(crontab -l)` bez wypisu | tak |
| wczytanie przez `cron` | w dzienniku `RELOAD (/var/spool/cron/ec2-user)` o 13:04:01 UTC, osiem sekund po `REPLACE`, przy pierwszej pełnej minucie | tak |

Rozmiary kopii z 9 września zgadzają się z tamtą edycją. 642 − 633 = 9
bajtów: zniknął znak końca linii i początek `2 16 * * * ` (12 znaków),
doszło ` ; ` (3 znaki).

### Uzupełnienie po zatwierdzeniu — dlaczego potrzebny był wpis `RELOAD`

Tego w pierwszej wersji notatki nie było. Latem 18:00 polskiego i 16:00
UTC to ta sama chwila. Gdyby `cron` nie wczytał nowego pliku, dzisiejszy
bieg odbyłby się starym harmonogramem o tej samej porze i linia startu też
pokazałaby `16:00:0X`. Sam wieczorny odczyt nie odróżniłby więc sukcesu od
sytuacji, w której nic się nie zmieniło.

Dlatego po wgraniu doszedł odczyt dziennika systemowego:
`sudo journalctl --since "30min ago" --no-pager | grep -i cron`. Słowa
`REPLACE` (zapisuje je komenda `crontab`) i `RELOAD` (zapisuje je sam
`cron`) sprawdzone przed odczytem w kodzie źródłowym cronie:
`src/crontab.c` i `src/database.c`.

**Wniosek dla części 10:** `RELOAD` po wgraniu **razem z** `16:00:0X`
wieczorem dowodzi, że działa nowy harmonogram i że strefa jest czytana.
Każde z nich osobno — nie.

**Trzeci przyrząd na wieczór.** Ten sam dziennik zapisuje start każdego
zadania jako `CROND[…]: (użytkownik) CMD (…)`. Widać to było na
cogodzinnym zadaniu systemu o 13:01:01 UTC. Wieczorem pokaże godzinę
startu naszych skryptów zapisaną przez sam `cron`, niezależnie od zegara
w Producencie i od czasu zmiany pliku.

Dotyczy jednej rzeczy na EC2: harmonogramu `cron` użytkownika `ec2-user`.
Kodu Pythona nie dotyka.

Skąd się to wzięło: przegląd z 8 września, punkt 2.10; prośba Gracjana
z 10 września; rozmowa z 12 września o zmianie czasu 25 października;
decyzja Gracjana z 13 września, żeby zrobić to dziś, w niedzielę.

---

## 1. Co jest dziś

`crontab -l` odczytany na EC2 13 września około 14:20. Porównany
`diff`-em z tekstem zapisanym w dzienniku 9 września: **identyczny**.
Trzy linie:

```
KAFKA_BOOTSTRAP=localhost:9094
0 16 * * * …data_ingestion.py … ; …kafka_consumer.py …
10 16 * * * …silver.py … && …gold.py …
```

EC2 chodzi w czasie uniwersalnym, UTC (sprawdzone 10 września przez
`timedatectl`). Cron czyta więc `0 16` jako 16:00 UTC. Ile to jest po
polsku, zależy od pory roku:

- **CEST** to polski czas letni, dwie godziny przed UTC.
- **CET** to polski czas zimowy, godzina przed UTC.

| Okres | Producent i Konsument | Silver i Gold | Harmonogram Windows |
|---|---|---|---|
| do 24.10.2026, czas letni | 18:00 polskiego | 18:10 polskiego | 18:10 polskiego |
| od 25.10.2026, czas zimowy | **17:00** polskiego | **17:10** polskiego | 18:10 polskiego |

Harmonogram Windows zostaje na 18:10 przez cały rok, bo Windows chodzi
po polsku.

---

## 2. Co się stanie 25 października, jeśli nic nie zrobimy

Od poniedziałku 26 października Producent ruszy o 17:00 polskiego, czyli
w chwili zamknięcia sesji na GPW. Dwa nasze pomiary mówią, że to zła
chwila:

- **8 września o 16:43** Yahoo oddało świecę za bieżący dzień z ceną
  z trwającej sesji. CBF `194.5` zostało zapisane jako zamknięcie
  (przegląd, punkt 2.1).
- **11 września o 17:45** Yahoo nie oddało jeszcze użytecznej świecy za
  ten dzień. O 18:00 już ją miało (przegląd, punkt 2.1).

**Czego nie wiemy:** co Yahoo oddaje dokładnie o 17:00. Oba możliwe
warianty są złe.

- **Świeca z ceną sprzed ogłoszenia kursu zamknięcia.** Producent zapisze
  ją jako zamknięcie i oznaczy dzień jako wysłany. Poprawiona cena nigdy
  nie dotrze do S3, bo korekty Yahoo do S3 nie docierają (przegląd 2.1).
  Wynik byłby codziennie trochę nieprawdziwy, bez śladu w logu.
  Podsumowanie Producenta pokazałoby wtedy normalne `nowych dni: 1`.
- **Brak świecy.** Producent nie znajdzie nowego dnia, Konsument odbierze
  zero, Silver policzy wieczór bez dzisiejszej sesji. Nazajutrz dojdzie
  wczorajsza świeca. Wynik byłby codziennie o dobę do tyłu. Tu przynajmniej
  podsumowanie pokazałoby `nowych dni: 0` w dzień giełdowy.

**Sprostowanie do rozmowy z 12 września.** Napisałem wtedy, że o 17:00
świecy „tym bardziej nie będzie". To było za pewne. Pomiar z 8 września
pokazuje, że w trakcie sesji świeca jest, tylko z nieostateczną ceną.

Do tego maszyny rozjadą się o godzinę: EC2 policzy o 17:10, Windows
o 18:10.

---

## 3. Trzy możliwości

Te same, które padły 12 września.

**Możliwość 1: `CRON_TZ=Europe/Warsaw` i godziny z 16 na 18, jednym
ruchem.** Bieg zostaje na 18:00 i 18:10 polskiego przez cały rok.

**Możliwość 2: ręczna zmiana godzin dwa razy w roku.** Z 16 na 17 przed
25 października, z 17 na 16 przed 28 marca 2027, i tak bez końca. Nic
nowego w harmonogramie, ale wszystko zależy od pamiętania. Jedna
zapomniana data to cichy tydzień.

**Możliwość 3: bieg dużo później w UTC**, na przykład 19:00 UTC, czyli
21:00 latem i 20:00 zimą. Poszerza zapas u Yahoo z kwadransa do godzin.
Ale Harmonogram Windows o 18:10 liczyłby **przed** EC2 i codziennie
wrzucał do gita wynik o dobę stary. Ma sens dopiero po wyłączeniu
Harmonogramu, czyli po szóstym kroku z kolejności napraw.

**Rekomendacja: możliwość 1.** Jedyna, która nie wymaga pamiętania i nie
psuje zgrania z Windowsem.

---

## 4. Co zmieniamy

Nowy harmonogram, cztery linie. Tekst poniżej nie jest przepisany ręcznie:
wyszedł z symulacji na kopii dzisiejszego `crontab`, tą samą procedurą,
która jest w części 7.

```
CRON_TZ=Europe/Warsaw
KAFKA_BOOTSTRAP=localhost:9094
0 18 * * * /home/ec2-user/GPW---pulse/venv/bin/python /home/ec2-user/GPW---pulse/kod/data_ingestion.py >> /home/ec2-user/GPW---pulse/companies/errors.txt 2>&1 ; /home/ec2-user/GPW---pulse/venv/bin/python /home/ec2-user/GPW---pulse/kod/kafka_consumer.py >> /home/ec2-user/GPW---pulse/companies/errors.txt 2>&1
10 18 * * * /home/ec2-user/GPW---pulse/venv/bin/python /home/ec2-user/GPW---pulse/kod/silver.py >> /home/ec2-user/GPW---pulse/companies/errors.txt 2>&1 && /home/ec2-user/GPW---pulse/venv/bin/python /home/ec2-user/GPW---pulse/kod/gold.py >> /home/ec2-user/GPW---pulse/companies/errors.txt 2>&1
```

Trzy różnice wobec dziś: nowa pierwsza linia i dwie godziny z `16` na
`18`. Minuty, ścieżki, `;`, `&&` i przekierowania bez zmian.

---

## 5. Jak `CRON_TZ` działa — sprawdzone w kodzie źródłowym

Wszystkie trzy fakty przeczytałem 13 września w kodzie źródłowym cronie,
w najnowszej wersji z repozytorium. **Na EC2 jest wersja 1.5.7, której
dokładnie nie czytałem.** Obsługa `CRON_TZ` w tym kodzie jest stara, ale
to poszlaka, nie dowód. Dowodem będzie bieg.

### Fakt 1 — strefa działa tylko wewnątrz `cron`, nie w skryptach

Co minutę cron ustawia na chwilę strefę z `CRON_TZ`, sprawdza, czy już
pora uruchomić zadanie, i przywraca poprzednią strefę (plik `src/cron.c`).
Kod, który buduje zmienne dla uruchamianego skryptu, strefy nie dokłada
(`src/security.c`). Python w skrypcie bierze więc godzinę z zegara
systemu, a ten jest w UTC.

Skutki:

- **Linia startu Producenta dalej pokazuje UTC.** Dla biegu o 18:00
  polskiego latem stanie tam `16:00:0X`, zimą `17:00:0X`.
- **Czas zmiany plików w `ls -l` dalej w UTC.**
- **Daty w pamięci Producenta liczą się jak dziś.** `datetime.fromtimestamp`
  patrzy na zegar systemu, więc klucze w `companies/*.txt` się nie
  zmienią. To ważne, bo zmiana kluczy wywołała zalew 1 września.

**Sprostowanie do notatki z 11 września** (część 9 i pułapka przy
decyzji 1): stoi tam, że po `CRON_TZ` linia startu przejdzie na `18:00`.
To nieprawda.

### Fakt 2 — zmienna działa tylko na linie pod nią

Cron czyta plik od góry. Każde zadanie dostaje zmienne zebrane do chwili,
w której cron doszedł do jego linii (`src/user.c`). `CRON_TZ` wpisane pod
zadaniem nie działałoby na nie. Dlatego ta linia idzie **na samą górę**.

### Fakt 3 — cron nie sprawdza nazwy strefy

Ani `crontab plik` przy wgrywaniu (`src/crontab.c`), ani cron przy
wczytywaniu (`src/entry.c`). Literówka typu `Europe/Warszawa` przejdzie
bez słowa. Co wtedy zrobi biblioteka systemowa przy liczeniu godziny,
jej dokumentacja nie mówi, a ja tego nie sprawdzałem. Dlatego nazwę
sprawdzamy osobną komendą przed wgraniem (część 7, krok 2).

---

## 6. Kształt na innych danych

Piekarnia w Nowym Jorku ma harmonogram pieca. Wszystkie wyjścia poniżej
pochodzą z prawdziwego uruchomienia na kopii, nie z głowy.

**Wejście, plik `plan.txt`:**

```
PIEC=elektryczny
0 5 * * * /home/piekarz/chleb.sh
10 5 * * * /home/piekarz/bulki.sh
```

Chcemy trzech rzeczy: strefy nowojorskiej na górze, chleba z 5:00 na
7:00 i bułek z 5:10 na 8:10.

**Komendy:**

```
cp plan.txt kopia.txt
echo 'CRON_TZ=America/New_York' > nowy.txt
sed -e 's/^0 5 /0 7 /' -e 's/^10 5 /10 8 /' kopia.txt >> nowy.txt
diff kopia.txt nowy.txt
```

Po kolei:

- `echo 'tekst' > nowy.txt` tworzy plik z jedną linią. Pojedynczy `>`
  zaczyna plik od zera.
- `sed` czyta plik linia po linii i wypisuje go ze zmianami. **Samego
  czytanego pliku nie zmienia.** Reguła `s/stare/nowe/` zamienia w każdej
  linii pierwszy napis `stare` na `nowe`; litera `s` pochodzi od
  angielskiego *substitute*, czyli „podstaw".
- `-e` dokłada kolejną regułę. Obie reguły działają po kolei na każdej
  linii.
- `^` na początku wzorca znaczy „tylko na samym początku linii".
- `>>` dopisuje wynik `sed` pod linię ze strefą.

**Wyjście, plik `nowy.txt`:**

```
CRON_TZ=America/New_York
PIEC=elektryczny
0 7 * * * /home/piekarz/chleb.sh
10 8 * * * /home/piekarz/bulki.sh
```

**Wyjście `diff`:**

```
0a1
> CRON_TZ=America/New_York
2,3c3,4
< 0 5 * * * /home/piekarz/chleb.sh
< 10 5 * * * /home/piekarz/bulki.sh
---
> 0 7 * * * /home/piekarz/chleb.sh
> 10 8 * * * /home/piekarz/bulki.sh
```

`0a1` czytamy: „za linią 0 pierwszego pliku, czyli na samym początku,
dodano (*add*) linię 1 drugiego". `2,3c3,4`: „linie 2–3 pierwszego
zmieniły się (*change*) w linie 3–4 drugiego". Numery przesunęły się
o jeden, bo na górze doszła linia.

### Pułapka bez `^`

Te same reguły bez daszka:

```
sed -e 's/0 5 /0 7 /' -e 's/10 5 /10 8 /' plan.txt
```

Wyjście:

```
PIEC=elektryczny
0 7 * * * /home/piekarz/chleb.sh
10 7 * * * /home/piekarz/bulki.sh
```

Bułki wylądowały na 7:10 zamiast na 8:10. Napis `0 5 ` siedzi w środku
`10 5 `, więc pierwsza reguła trafiła w obie linie, a druga nie miała już
czego zamienić. Żadnego błędu na ekranie.

W naszym `crontab` obie godziny przesuwają się o tyle samo, więc bez `^`
wynik wyszedłby przypadkiem dobry. Sprawdziłem to na kopii. Nie opieramy
się na przypadku.

---

## 7. Jak to zrobimy

Rytuał z 9 września: kopia, której nie ruszamy, praca na drugim pliku,
`diff` przed wgraniem, nigdy `crontab -e`. Numerowane kroki z etykietami
maszyn dostaniesz osobno, po zatwierdzeniu notatki. Tu tylko kształt:

1. `crontab -l > ~/crontab-kopia-0913.txt` — kopia dzisiejszego stanu.
   Nowa nazwa. Kopia z 9 września zostaje nietknięta.
2. `TZ=Europe/Warsaw date` — sprawdzenie nazwy strefy. Zapis
   `NAZWA=wartość komenda` ustawia zmienną **tylko dla tej jednej
   komendy**. Ma wyjść bieżąca godzina polska i skrót `CEST`.
3. `echo 'CRON_TZ=Europe/Warsaw' > ~/crontab-nowy-0913.txt` — nowy plik
   z linią strefy.
4. `sed -e 's/^0 16 /0 18 /' -e 's/^10 16 /10 18 /' ~/crontab-kopia-0913.txt >> ~/crontab-nowy-0913.txt`
   — dopisanie reszty ze zmienionymi godzinami.
5. `diff ~/crontab-kopia-0913.txt ~/crontab-nowy-0913.txt` — wynik
   porównujemy z przewidywaniem z części 10.
6. `wc -l ~/crontab-kopia-0913.txt ~/crontab-nowy-0913.txt` — ma być 3 i 4.
7. `crontab ~/crontab-nowy-0913.txt` — wgranie.
8. `diff ~/crontab-nowy-0913.txt <(crontab -l)` — maszyna ma dokładnie to,
   co w pliku. Brak wypisu.

**Powrót:** `crontab ~/crontab-kopia-0913.txt`, w sekundę.

**Termin wgrania: dziś przed 17:55.** Nie między 17:55 a 18:15.

Sprawdzone przed napisaniem, na kopii: wzorzec `^0 16 ` trafia w dokładnie
jedną linię, `^10 16 ` w dokładnie jedną, a napis ` 16 ` nie występuje
nigdzie poza tymi dwiema.

---

## 8. Decyzje do podjęcia

### Decyzja 1 — godziny

- **18:00 i 18:10 polskiego, jak dziś.**
- **Przy okazji później**, na przykład 18:30 i 18:40, żeby poszerzyć
  kwadrans zapasu u Yahoo. Koszt: Harmonogram Windows o 18:10 liczyłby
  przed EC2 i wrzucał do gita wynik o dobę stary, chyba że równocześnie
  przestawimy Harmonogram. To druga maszyna i druga zmiana naraz.

**Rekomendacja: 18:00 i 18:10.** Dzisiejsza zmiana ma ruszyć jedną
rzecz, żeby jeden bieg mógł ją sprawdzić. Szerszy zapas to osobna decyzja,
najlepiej przy wyłączaniu Harmonogramu.

### Decyzja 2 — czym zbudować nowy plik

- **`sed`, jak w części 7.** Ścieżek nikt nie przepisuje, a procedurę da
  się przećwiczyć na piekarni.
- **`nano` na kopii.** Znane z ćwiczenia 9 września. Trzeba jednak ręcznie
  dopisać linię i zmienić dwie cyfry w liniach długich na trzysta znaków.
  `diff` i tak złapałby pomyłkę.

**Rekomendacja: `sed`.** Robi dokładnie to, co jest zapisane, i to samo
za każdym razem.

### Decyzja 3 — sprawdzenie nazwy strefy przed wgraniem

- **Tak, `TZ=Europe/Warsaw date`.**
- **Nie.** Liczymy na `diff` i na wieczorny bieg.

**Rekomendacja: tak.** Kosztuje jedną komendę, a cron sam literówki nie
zgłosi (fakt 3). `diff` pokaże literówkę tylko temu, kto ją zauważy.

### Decyzja 4 — kiedy wgrać

- **Dziś przed 17:55.** Dzisiejszy bieg jest dowodem przy zerowej
  stawce, bo w niedzielę GPW nie handluje.
- **Dziś po biegu, około 18:20.** Pierwszym biegiem pod nową strefą byłby
  wtedy poniedziałek, dzień giełdowy. Ten sam bieg potwierdzałby
  jednocześnie strefę i Producenta, a przy pomyłce strefy zapisałby cenę
  z trwającej sesji.

**Rekomendacja: przed 17:55.**

---

## 9. Co może pójść źle

**Strefa weszła, godziny nie** (pułapka z przeglądu 2.10). Bieg o 16:00
polskiego, czyli 14:00 UTC. W dzień giełdowy to cena z trwającej sesji
zapisana jako zamknięcie. *Zabezpieczenie:* jeden plik i jedno
`crontab plik`; `diff` przed wgraniem musi pokazać i `0a1`, i `2,3c3,4`.
*Wykrycie po fakcie:* linia startu `14:00:0X`.

**Godziny weszły, strefa nie.** Najłatwiej o to przez pojedynczy `>`
zamiast `>>` w kroku z `sed`, który nadpisałby linię strefy. Bieg o 18:00
UTC, czyli 20:00 polskiego. Danym to nie szkodzi, ale Harmonogram Windows
o 18:10 policzyłby przed EC2. *Zabezpieczenie:* `diff` bez `0a1`
i `wc -l` z trójką zamiast czwórki, więc zatrzymujemy się przed wgraniem.
*Wykrycie po fakcie:* o 18:15 w logu nie ma nowego bloku, a o 20:00
pojawia się blok z `18:00:0X`.

**Literówka w nazwie strefy.** Cron ją przyjmie. Skutku nie znamy.
*Zabezpieczenie:* krok 2 z części 7. *Wykrycie po fakcie:* w linii startu
cokolwiek innego niż `16:00:0X`.

**`CRON_TZ` pod zadaniami.** Nie działałoby na nie (fakt 2).
*Zabezpieczenie:* `echo` tworzy plik z tą linią jako pierwszą, a `diff`
pokazuje `0a1`, czyli dopisek na samym początku.

**Krok z `sed` uruchomiony dwa razy.** W nowym pliku byłyby dwa komplety
zadań i cron uruchomiłby Producenta, Konsumenta, Silvera i Golda po dwa
razy naraz. *Zabezpieczenie:* `wc -l` pokaże 6 zamiast 4, a `diff`
cztery linie z `>` zamiast dwóch. Wtedy zaczynamy od kroku 3, bo
pojedynczy `>` czyści plik.

**Powrót złą kopią.** `~/crontab-kopia-0909.txt` to harmonogram sprzed
edycji 9 września, jeszcze z osobną linią `2 16` dla Konsumenta. Wgranie
jej cofnęłoby nas o cztery dni. Powrót do stanu sprzed dziś to wyłącznie
`~/crontab-kopia-0913.txt`.

**Wgranie w okolicy 18:00.** Nie dałoby się stwierdzić, który harmonogram
obsłużył dzisiejszy bieg, i sprawdzenie straciłoby sens. *Zabezpieczenie:*
wgrać przed 17:55.

**Zerwane połączenie SSH w trakcie.** Nic się nie zmienia aż do
`crontab plik`, a ten podmienia harmonogram w całości albo wcale.

**Dzień zmiany czasu** (25 października i 28 marca). Zegar przestawia się
w nocy, między drugą a trzecią, a nasze biegi są o 18:00. Nie powinno
więc być ani podwójnego, ani zgubionego biegu. To wniosek z godzin, nie
sprawdzony biegiem.

**Broker nie odpowiada, Atena zwraca pół tabeli, dochodzi czwarta
spółka, skrypt się wywraca.** Ta zmiana tego nie dotyczy: przesuwa
wyłącznie chwilę uruchomienia, a skrypty zostają te same.

---

## 10. Jak sprawdzimy

### Przed wgraniem

Krok 2: bieżąca godzina polska i `CEST`.

Krok 5, **dokładne przewidywane wyjście `diff`**, wzięte z symulacji na
kopii:

```
0a1
> CRON_TZ=Europe/Warsaw
2,3c3,4
< 0 16 * * * /home/ec2-user/GPW---pulse/venv/bin/python /home/ec2-user/GPW---pulse/kod/data_ingestion.py >> /home/ec2-user/GPW---pulse/companies/errors.txt 2>&1 ; /home/ec2-user/GPW---pulse/venv/bin/python /home/ec2-user/GPW---pulse/kod/kafka_consumer.py >> /home/ec2-user/GPW---pulse/companies/errors.txt 2>&1
< 10 16 * * * /home/ec2-user/GPW---pulse/venv/bin/python /home/ec2-user/GPW---pulse/kod/silver.py >> /home/ec2-user/GPW---pulse/companies/errors.txt 2>&1 && /home/ec2-user/GPW---pulse/venv/bin/python /home/ec2-user/GPW---pulse/kod/gold.py >> /home/ec2-user/GPW---pulse/companies/errors.txt 2>&1
---
> 0 18 * * * /home/ec2-user/GPW---pulse/venv/bin/python /home/ec2-user/GPW---pulse/kod/data_ingestion.py >> /home/ec2-user/GPW---pulse/companies/errors.txt 2>&1 ; /home/ec2-user/GPW---pulse/venv/bin/python /home/ec2-user/GPW---pulse/kod/kafka_consumer.py >> /home/ec2-user/GPW---pulse/companies/errors.txt 2>&1
> 10 18 * * * /home/ec2-user/GPW---pulse/venv/bin/python /home/ec2-user/GPW---pulse/kod/silver.py >> /home/ec2-user/GPW---pulse/companies/errors.txt 2>&1 && /home/ec2-user/GPW---pulse/venv/bin/python /home/ec2-user/GPW---pulse/kod/gold.py >> /home/ec2-user/GPW---pulse/companies/errors.txt 2>&1
```

Krok 6: `3` i `4`, razem `7 total`.

### Zaraz po wgraniu

Krok 8: brak wypisu.

### Dziś po 18:15

Stan wyjściowy to odczyt z 13 września około 14:20: `errors.txt` 461,
`errors.log` 8, pliki spółek po 770, grupa Kafki 2339.

| Co | Przewidywanie |
|---|---|
| `grep -n "Data pomiaru Producenta" companies/errors.txt` | dwie linie; nowa: `462:=== Data pomiaru Producenta: 2026-09-13 16:00:0X ===` |
| `errors.txt` | 482 linie |
| długość nowego bloku | 21 linii, bo znowu zero wiadomości |
| `ls -l --time-style=full-iso companies/errors.txt` | `2026-09-13 16:10:…` i `+0000` |
| `errors.log` | 8 |
| pliki spółek | po 770 |
| grupa Kafki | `2339  2339  0` |

**Jak czytać linię startu:**

| Co widać o 18:15 | Co to znaczy | Co robimy |
|---|---|---|
| nowy blok, `16:00:0X` | strefa i godziny weszły | nic, zostaje |
| nowy blok, `14:00:0X` | strefa weszła, godziny nie | powrót kopią z 13.09 przed jutrem |
| brak nowego bloku | strefa nie działa (bieg przyjdzie o 20:00) albo cron nie ruszył | powrót kopią z 13.09, sprawdzenie o 20:15 |

### Poniedziałek, 14 września

Pierwszy bieg pod nową strefą w dzień giełdowy i zarazem sprawdzenie
Producenta w dzień giełdowy. Jeśli do tej chwili nic innego nie trafi na
EC2:

- linia startu `2026-09-14 16:00:0X`;
- trzy razy `nowych dni: 1, wysłane: 1, stan: zapisane`;
- `Odebrano 3 wiadomości`, a przed nim wraca ostrzeżenie `boto3`;
- blok 23 linie, `errors.txt` 505, pliki spółek po 771, grupa 2342.

### Pierwszy prawdziwy sprawdzian zmiany czasu

Poniedziałek 26 października. Linia startu ma pokazać `17:00:0X`.

---

## 11. Co to zepsuje za miesiąc

**Od 25 października log pokaże `17:00:0X` i `17:10` przy biegu o 18:00
polskiego. To jest poprawne.** Kto przeczyta log bez tej wiedzy, uzna, że
bieg przesunął się na 17:00, i zacznie naprawiać coś, co działa. To
zdanie musi stać w `CLAUDE.md`.

**Zapisy „16:00 UTC" i „16:10 UTC" w `CLAUDE.md`, przeglądzie i pamięci
staną się historią.** Opis „`cron` uruchamia codziennie o 16:00 UTC"
trzeba zamienić na „o 18:00 czasu polskiego, przez cały rok".

**Każda przyszła linia w tym `crontab` będzie czytana po polsku**, bo
`CRON_TZ` stoi nad nią. Gdyby kiedyś kompakcja trafiła do `cron`, jej
godzinę piszemy po polsku.

**Dwie strefy w jednej rozmowie.** Harmonogram po polsku, a log,
`ls -l`, narzędzia Kafki i dziennik samego `cron` w UTC. Przy każdej
godzinie trzeba mówić, w której strefie jest podana.

**Kopia z 9 września przestaje być „ostatnim dobrym stanem".** Tę rolę
przejmuje kopia z 13 września.

---

## 12. Czego ta zmiana nie naprawia

- **Kwadrans zapasu u Yahoo zostaje kwadransem.** `CRON_TZ` pilnuje, żeby
  go nie stracić po 25 października, ale go nie poszerza (decyzja 1).
- **Producent uruchomiony ręcznie przed 17:00** dalej zapisze cenę
  z trwającej sesji jako zamknięcie (przegląd 2.1, punkt czerwony).
- **Nic nie sygnalizuje awarii.** Spóźniony albo nieudany bieg dalej widać
  tylko przez czytanie logu. To krok ósmy z kolejności napraw.
- **Dwie maszyny dalej liczą to samo.** Harmonogram Windows zostaje.

---

## Powiązane notatki

- [[Przeglad-2026-09-08-co-nie-gra]] — punkt 2.10 (zmiana czasu i
  pułapka) i punkt 2.1 (cena z trwającej sesji, kwadrans zapasu)
- [[Notatka-2026-09-11-podsumowanie-w-producencie]] — do sprostowania
  zdanie o linii startu po `CRON_TZ`
- dziennik z 9 września — pełny tekst `crontab` i rytuał edycji z kopią
  i `diff`
- [[Slownik]] — są już `CRON_TZ`, `crontab`, `diff`, `grep`, `head`,
  `tail`; do dopisania: `sed 's/…/…/'`, `^` we wzorcu, `-e`, adresy `0a1`
  i `2,3c3,4` w `diff`, `NAZWA=wartość komenda`, CEST i CET
