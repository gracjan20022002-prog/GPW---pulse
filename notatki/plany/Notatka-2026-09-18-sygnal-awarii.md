# Notatka 18.09 — sygnał awarii

**Stan: zatwierdzona w całości przez Gracjana 18.09; wdrożona 21.09.** Decyzje 1(a), 2(a),
3(a), 4 i 5 zgodnie z rekomendacją. **Postęp:** 18.09 konto u stróża, `kod/control.py`
z funkcjami `sprawdz_blok` i `wytnij_blok`, 11 testów na prawdziwym bloku z 18.09; 19.09 część
główna skryptu, zmiana logu w Producencie i kod na EC2, testy 2–3 z prawdziwym stróżem;
**21.09** linia `30 18` w `crontab`, test ciszy i pierwszy bieg z `cron` (wyniki w części „Jak
sprawdzimy"). Punkt 8 kolejki napraw z przeglądu 08.09 („Sygnał awarii"), wzięty przed
punktami 6 i 7 decyzją Gracjana z 18.09.

## Sedno w trzech zdaniach

Dziś awarię widać tylko wtedy, gdy ktoś wejdzie przez SSH i przeczyta
`errors.txt`, a treść błędów Producenta w ogóle tam nie trafia. Proponuję
odwrócić pytanie: zamiast szukać w logu śladów porażki, co wieczór szukamy
**dowodu sukcesu** i tylko przy komplecie EC2 wysyła zewnętrznemu stróżowi
krótkie „bieg udany”. Jeśli do 19:00 stróż nic nie dostanie — z dowolnego
powodu, także gdy EC2 leży — wysyła Ci e-mail.

## Przykład na innych danych: piekarnia

Piekarz piecze w nocy trzy rodzaje pieczywa i o 6:00 zawozi je do sklepu.
Właściciel śpi. Umowa: po dostawie piekarz przechodzi listę kontrolną i **tylko
przy komplecie** wysyła SMS „komplet”; przy braku wysyła „brak: …”. Telefon
właściciela ma budzik — jeśli do 6:30 nie przyjdzie „komplet”, dzwoni.

| Poranek | Co się stało | Co dostaje właściciel |
|---|---|---|
| wtorek | wszystko dobrze | SMS „komplet”, budzik milczy |
| środa | spalone rogale | SMS „brak: rogale” → alarm od razu |
| czwartek | piekarz zaspał | nic → budzik o 6:30 |
| piątek | padł telefon piekarza | nic → budzik o 6:30 |

Czwartek i piątek to sedno. Umowa „dzwoń, jak coś pójdzie źle” nie złapałaby
żadnego z nich, bo ten, kto miał dzwonić, sam nie działa.

## Przykład → projekt

| Piekarnia | Projekt |
|---|---|
| piekarz | EC2 z `cron` |
| lista kontrolna | nowy krótki skrypt kontrolny, `cron` o 18:30 polskiego |
| „trzy rodzaje upieczone” | `stan: zapisane` tyle razy, ile spółek w `config.py` |
| „dostawa odebrana” | linia `Odebrano … wiadomości` |
| „towar w sklepie” | 2 × `S3: wysłano` |
| „nic spalonego” | zero `Traceback` w dzisiejszym bloku |
| SMS „komplet” / „brak: …” | zgłoszenie do stróża: „udany” albo „awaria + powód” |
| budzik o 6:30 | stróż: brak zgłoszenia do 19:00 → e-mail |

Każdy z czterech warunków pojawia się w logu **tylko wtedy, gdy krok się
udał**. Przy martwym brokerze Producent wypisuje `nietknięte`, przy błędzie
Yahoo `Brak odczytu` — liczba `zapisane` się nie zgadza. Ostrzeżenia
(`kafka-python`, `boto3`, `pandas`) nie przeszkadzają, bo nie szukamy złych
słów. W weekend reguła działa tak samo: `nowych dni: 0` też kończy się
`stan: zapisane` (sprawdzone 12.09), a Gold i tak wysyła oba pliki.

## Co łapie, czego nie łapie

| Awaria | Dziś | Po zmianie |
|---|---|---|
| Producent: broker albo Yahoo nie odpowiada | tylko w `errors.log`, którego nikt nie czyta | e-mail z powodem |
| Konsument, Silver albo Gold pada | `Traceback` w `errors.txt`, jeśli ktoś zajrzy | e-mail z powodem |
| `cron` nie ruszył, EC2 leży, brak sieci | cisza | e-mail po 19:00 |
| sam skrypt kontrolny ma błąd | — | e-mail po 19:00 |

**Nie łapie** (świadomie, pierwsza wersja):
- złych danych przy udanym biegu — Athena zwraca pół tabeli, Yahoo poprawia
  ceny wstecz, cena z trwającej sesji;
- braku świecy o 18:00 w dzień giełdowy — wygląda jak sobota, sam się naprawia
  dzień później;
- lokalnego Harmonogramu i kompakcji — obie na laptopie, poza `cron`.

## Decyzje — Twoje

1. **Kto pilnuje.** (a) zewnętrzny stróż, np. healthchecks.io — plan darmowy:
   20 zadań, 100 wpisów historii na zadanie (sprawdzone 18.09 na ich stronie),
   konto zakładasz sam. (b) e-mail z AWS SNS wysyłany przez EC2 — SNS tylko
   doręcza to, co dostanie, i na nic nie czeka, więc **nie łapie czwartku ani
   piątku**: gdy EC2 albo skrypt kontrolny nie działa, nikt nic nie wysyła,
   a pusta skrzynka wygląda jak zwykły wieczór. (c) SNS + CloudWatch (usługa
   AWS, która umie alarmować przy ciszy) — wszystko w AWS, łapie to samo co
   (a), ale to dwie nowe usługi i więcej uprawnień; szczegółów nie sprawdziłem.
   Rekomendacja: **(a)**.
2. **Co znaczy „bieg udany”.** (a) dowód sukcesu, cztery warunki wyżej.
   (b) szukanie złych słów (`Traceback`, `ERROR`). Rekomendacja: **(a)** —
   Producent kończy się normalnie nawet przy martwym brokerze (w kodzie nie ma
   `sys.exit`, błędy brokera i Yahoo są łapane i odkładane do `errors.log`).
3. **Jeden log czy dwa.** (a) Producent pisze błędy tam, gdzie reszta, czyli do
   `errors.txt`. (b) zostają dwa pliki. Wykrywanie działa w obu; różnica: czy
   treść błędu Producenta będzie w bloku. Rekomendacja: **(a)**, ale można
   odłożyć bez szkody dla wykrywania.
4. **Gdzie leży adres zgłoszenia.** Działa jak hasło — kto go zna, może zgłosić
   „udany bieg”. Rekomendacja: w `crontab`, jak `GOLD_DO_S3`, **nigdy w gicie**.
5. **Godziny.** Skrypt kontrolny o 18:30 polskiego, alarm po 30 minutach ciszy.
   Harmonogram stróża w strefie `Europe/Warsaw`, nie w UTC serwera — nasz
   `crontab` liczy godziny po polsku przez `CRON_TZ`, a stróż musi liczyć tak
   samo (ich FAQ: inna strefa = alarmy o złej godzinie).

## Co może pójść źle

- Skrypt kontrolny ma błąd → nic nie wyśle → stróż alarmuje. Awaria skryptu kontrolnego też jest
  głośna — główny powód decyzji 1(a).
- Zmiana czasu 25.10 → fałszywy alarm, jeśli harmonogram stróża będzie w UTC.
- Gold jeszcze liczy o 18:30 → fałszywe „brak”. Dziś kończy przed 18:15.
- Bieg dwa razy → skrypt kontrolny czyta tylko ostatni blok, dwa zgłoszenia nie szkodzą.
- Skrypt kontrolny uruchomiony drugi raz tego samego dnia (np. ręczny test po
  biegu z `cron`) widzi w bloku własną linię z poprzedniego razu. Jego
  komunikaty zawierają szukane słowa (`Odebrano`, `stan: zapisane`,
  `S3: wysłano`), więc bez odsiewu uznałby awarię za komplet. Zauważone 18.09
  przy przeglądzie funkcji; przy wycinaniu bloku odsiewamy linie skryptu
  kontrolnego i dokładamy na to test.
- Polskie litery w treści zgłoszenia „awaria + powód” → na EC2
  `UnicodeEncodeError`, na laptopie nie. EC2 ma `urllib3==1.26.20`, który
  oddaje tekst do `http.client`, a ten koduje go jako latin-1 (sprawdzone 18.09
  w kodzie obu bibliotek); laptop ma `urllib3==2.7.0`, który koduje UTF-8.
  Test na laptopie tego nie pokaże. Treść wysyłamy jako `.encode("utf-8")`.
- Czwarta spółka → liczba `zapisane` brana z `config.py`, nie wpisana na sztywno.
- Adres zgłoszenia trafi do gita → każdy może „udawać” udane biegi.
- Stróż ma przerwę → w tym czasie alarmów nie ma. Obsługa to jedna osoba i sami
  piszą, że przerwy wielogodzinne, nawet wielodniowe, są możliwe. Ryzyko
  przyjęte, jedyne spoza naszej kontroli.
- Stróż zmienia warunki planu darmowego → kod jest otwarty (licencja BSD),
  w ostateczności własna kopia albo inny stróż.
- Rok bez logowania na konto stróża → e-mail z ostrzeżeniem, po 30 dniach konto
  skasowane. Zgłoszenia z EC2 nie liczą się jako aktywność.
- Codzienny alarm o tę samą znaną wadę → przestajesz czytać. Sprawdzone 18.09:
  stróż pisze przy zmianie stanu (padło / wróciło); przypomnienia co godzinę
  lub co dzień tylko po włączeniu.

## Jak sprawdzimy

Przy każdym teście wynik zapisany **przed** uruchomieniem. **Wyniki (dopisane 21.09):**

1. Laptop, `pytest`, bez sieci: funkcje skryptu kontrolnego na sztucznych blokach —
   dzień giełdowy, sobota, `nietknięte`, `Traceback`, brak `S3: wysłano`. **Zaliczone**
   (18.09 jedenaście testów, `11 passed` wklejone 19.09).
2. EC2, ręcznie, na prawdziwym `errors.txt` → stróż pokazuje „udany". **Zaliczone 19.09**
   (`Kontrola: OK`, kod 0, wpis `#2 OK`, `GET` z `13.63.105.190`).
3. EC2, wymuszona awaria → e-mail z powodem. **Zaliczone 19.09**, awaria wymuszona złą datą
   (nie kopią logu): `Kontrola: AWARIA - Brak pomiaru producenta z 2026-09-19`, wpis `#1
   Failure` (POST, 2351 bajtów = 57 + 2294, policzone przed odczytem), mail `DOWN`
   z treścią i całym blokiem, polskie litery bez krzaków.
4. Cisza — nic nie wysyłamy → e-mail po okresie ciszy. **Zaliczone 19.09 wieczorem,
   potwierdzone 21.09 zrzutem maila:** `Status Changed to Down at Sat, 19 Sep 2026 19:00:00
   +0200` — czas polski, więc strefa `Europe/Warsaw` działa.
5. Pierwszy bieg z `cron` o 18:30 → „udany". **Zaliczone 21.09:** linia `30 18` wgrana
   16:53 polskiego, bieg o 18:30:02, start w linii 663, `wc -l` 691, ostatnia linia
   `Kontrola: OK`, stróż `#3 OK` (`down → up`), mail `UP` („downtime lasted 1 day, 23
   hours"). Dopiero teraz warunek (d) z definicji „zrobione" jest spełniony; zastrzeżenia
   w CLAUDE.md (jeden bieg, awaria pokazana tylko wymuszona, strefa dopiero 25.10).

## Co to zepsuje za miesiąc

- Blok w `errors.txt` urósł o jedną linię (wynik skryptu kontrolnego; **potwierdzone 21.09**): **29** w dzień
  giełdowy, **27** bez nowych wiadomości. Wszystkie przewidywania od
  wdrożenia — z nową liczbą.
- Przy decyzji 3(a) `errors.log` przestaje rosnąć, a w dni z błędem Producenta
  blok urośnie o linie `ERROR`.
- 25.10 — pierwszy bieg po zmianie czasu, pierwszy prawdziwy sprawdzian strefy
  u stróża.
- Punkt 6 kolejki (wyłączenie Harmonogramu) niczego tu nie rusza — skrypt kontrolny
  patrzy tylko na EC2.

## Powiązane notatki

- [[Przeglad-2026-09-08-co-nie-gra]] — 2.7 „Nikt się nie dowie” i „Log jest
  podwójny”, Część 5 punkt 8
- [[Notatka-2026-09-17-zakladka-przed-zapisem]]
- [[Notatka-2026-09-13-strefa-czasowa-cron]]
