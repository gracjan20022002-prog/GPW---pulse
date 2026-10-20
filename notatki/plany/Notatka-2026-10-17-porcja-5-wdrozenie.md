# Porcja 5, wt. 20.10: wdrożenie napraw 1 i 2 na EC2 — kroki i przewidywania

Przygotowane 17.10 (sobota), na prośbę Gracjana, na pon. 19.10. **Przeliczone 19.10 na wt. 20.10**:
okno 19.10 minęło bez biegu. Zmieniły się daty i liczby, doszedł krok A8 (pamięć ma 19.10 przed
ręcznym biegiem). Przewidywania są zapisane **przed** biegiem.
Godziny podaję po polsku i w UTC. EC2 (`date`, log, `ls`, `aws s3 ls`) chodzi w UTC, a do 25.10
UTC = polski − 2 h. Wszystkie komendy wykonuje Gracjan; Claude porównuje wyniki z tym plikiem.
Instrukcja kodu: [[Notatka-2026-10-13-jak-napisac-naprawy-1-i-2]], część 7, punkt 5.
**Zatwierdzone przez Gracjana 17.10 bez zmian.** Przeliczenie na 20.10 zatwierdzone 19.10.

---

## 1. Nad czym pracujemy

Naprawy 1 i 2 są na laptopie i na GitHubie (porcje 1–4, commit `5fa44fc` z 17.10 i późniejsza
dokumentacja). EC2 chodzi jeszcze na `5676575`, czyli bez nich. We wtorek 20.10:

1. `git pull` na EC2, żeby `cron` o 18:00 użył nowego kodu.
2. Jeden ręczny bieg Producenta z udawanym „dziś” = poniedziałek 19.10. Wtorkowa świeca jest
   wtedy dla Producenta „nie dzisiejsza”, więc ma zostać **wstrzymana**: nie pójdzie do Kafki
   ani do pamięci. To jedyny sprawdzian wstrzymania na prawdziwym Yahoo i prawdziwej Kafce.
3. Zwykły `cron` o 18:00 z prawdziwym „dziś” = 20.10. Świecy nie ma w pamięci, więc ją wyśle.
4. Kontrola po 18:32 i ręczny sprawdzian alarmu `wstrzymane` na EC2 (bez zgłoszenia u stróża).

**Warunek:** bieg 19.10 normalny (sprawdzony 19.10: log kończy się na linii 1503, pamięć ma
19.10) i do wtorku nic nie dopisało się do logu.

**Różnica względem poniedziałku:** udawane „dziś” to teraz dzień giełdowy (19.10), a nie
niedziela. Gdyby pamięci brakowało 19.10, ręczny bieg wysłałby 19.10 do Kafki drugi raz. Dlatego
krok A8 sprawdza pamięć przed biegiem.

---

## 2. Plan dnia (wt. 20.10)

| Polski | UTC (EC2) | Co |
|---|---|---|
| najpóźniej do 17:45, lepiej wcześniej | do 15:45 | Porcja A: `git pull` i sprawdzenia |
| 17:55:00–17:57:59 | 15:55:00–15:57:59 | Porcja B: ręczny bieg Producenta |
| 18:00, 18:10, 18:30 | 16:00, 16:10, 16:30 | `cron` — **od 17:58 do 18:32 nic nie uruchamiamy** |
| po 18:32 | po 16:32 | Porcja C: kontrola i sprawdzian alarmu |

## 3. Przewidywania w skrócie

| Co | Ręczny bieg 17:5X | `cron` 18:00 |
|---|---|---|
| linia spółki | `nowych dni: 1, wysłane: 0, stan: zapisane, wstrzymane: 1 (ostatnie: 2026-10-20 …)` | `nowych dni: 1, wysłane: 1, stan: zapisane` |
| do Kafki | nic | 3 wiadomości, zakładka 2417 → **2420** |
| pamięć spółek | bez 20.10, ostatni dzień 19.10 (796 linii) | z 20.10, **797** linii |
| `errors.txt` | bez zmian, **1503** linie (wynik idzie do osobnego pliku) | blok **1504–1531**, 28 linii |
| kontrola | — | `Kontrola: Dane 2391 wierszy`, `Kontrola: OK`, stróż **#36** |

---

## 4. Porcja A — do 17:45 polskiego (15:45 UTC)

1. **PRZEŁĄCZENIE [lokalny PowerShell, nowe okno, venv nieistotne]**: folder z kluczem. Wiersz
   kończy się na `aws ec2 key>`.
```
cd "C:\Users\gracj\OneDrive\Dokumenty\DE\GPW - pulse\aws\aws ec2 key"
```
2. **PRZEŁĄCZENIE [lokalny PowerShell, venv nieistotne]**: połączenie z EC2. Ma być wiersz
   `[ec2-user@ip-… ~]$`.
```
ssh -i "gpw-tracker-key.pem" ec2-user@13.63.105.190
```
3. **[EC2, przez SSH]**: folder projektu. Wiersz kończy się na `GPW---pulse]$`.
```
cd ~/GPW---pulse
```
4. **[EC2, przez SSH]**: `Tue Oct 20 …`, UTC, przed 15:45.
```
date
```
5. **[EC2, przez SSH]**: stary kod. Ma wyjść `5676575 …`.
```
git log -1 --oneline
```
6. **[EC2, przez SSH]**: ma nie wyjść nic.
```
git status --short
```
7. **[EC2, przez SSH]**: koniec poniedziałkowego bloku. Ma wyjść **`1503 companies/errors.txt`**.
   Inna liczba = po kontroli 19.10 coś dopisało się do logu; stop, najpierw sprawdzić co, dopiero
   potem `git pull`.
```
wc -l companies/errors.txt
```
8. **[EC2, przez SSH]**: pamięć ma poniedziałek. Przy każdej spółce (nagłówek
   `==> companies/….WA.txt <==`) ostatnia linia z 19.10, tak jak 19.10 po biegu:
   `2026-10-19 17:00:00, 194.3000030517578` (CBF), `…, 342.3999938964844` (SNT),
   `…, 141.47999572753906` (XTB). Brak 19.10 = stop przed porcją B.
```
tail -n 1 companies/*.WA.txt
```
9. **[EC2, przez SSH]**: adres brokera w `crontab`. Ma wyjść jedna linia
   `KAFKA_BOOTSTRAP=localhost:9094`. Bez niej nowy Producent i Konsument o 18:00 skończą się
   komunikatem `Brak zmiennej …`. Na ekran idzie tylko ta linia — **całego `crontab` nie
   wklejać** (adres stróża).
```
crontab -l | grep KAFKA
```
10. **[EC2, przez SSH]**: pobranie nowego kodu. Ma wyjść `Updating 5676575..<hash>`, `Fast-forward`,
    na liście m.in. `kod/control.py`, `kod/data_ingestion.py`, `kod/kafka_consumer.py`,
    `kod/session.py`, a na końcu `N files changed, …`. Liczbę N poda Claude we wtorek, po
    commicie dokumentacji (do `5fa44fc`: 21 plików, `3392 insertions(+), 946 deletions(-)`;
    dojdzie dokumentacja z 17 i 19.10).
```
git pull
```
11. **[EC2, przez SSH]**: ma wyjść ten sam hash co `git log -1` na laptopie.
```
git log -1 --oneline
```
12. **[EC2, przez SSH]**: ma nie wyjść nic.
```
git status --short
```
13. **[EC2, przez SSH]**: zapasowy adres brokera zniknął z kodu. Ma nie wyjść nic.
```
grep -rn "13.63.105.190" kod/
```
14. **[EC2, przez SSH]**: mają wyjść 4 linie: `kod/data_ingestion.py:17:BOOTSTRAP =
    os.environ.get("KAFKA_BOOTSTRAP")`, `kod/data_ingestion.py:19:    sys.exit(…)`,
    `kod/kafka_consumer.py:8:BOOTSTRAP = …` i `kod/kafka_consumer.py:10:    sys.exit(…)`.
```
grep -n "KAFKA_BOOTSTRAP" kod/data_ingestion.py kod/kafka_consumer.py
```
15. **[EC2, przez SSH]**: składnia na Pythonie 3.14.6. Ma nie wyjść nic. (EC2 nie ma `pytest`;
    testy: `38 passed` na laptopie 17.10.)
```
venv314/bin/python -m py_compile kod/data_ingestion.py kod/kafka_consumer.py kod/control.py kod/session.py
```
16. **[EC2, przez SSH]**: nowy `control.py` na poniedziałkowym bloku, bez `>>` i bez stróża. Mają
    wyjść: 2 linie ostrzeżenia `pandas` z `kod/path.py:32`, `Kontrola: Dane 2388 wierszy`,
    `Kontrola: OK`, `Kontrola: brak adresu stróża`.
```
KONTROLA_DATA=2026-10-19 venv314/bin/python kod/control.py
```
17. **[EC2, przez SSH]**: ręczna kontrola nic nie dopisała. Ma wyjść **`1503`**.
```
wc -l companies/errors.txt
```

Okno SSH zostaje otwarte. Do 17:55 nic więcej.

---

## 5. Porcja B — 17:55:00–17:57:59 polskiego (15:55–15:57 UTC)

1. **PRZEŁĄCZENIE [EC2, przez SSH]**: to samo okno, wiersz kończy się na `GPW---pulse]$`. Jeśli
   połączenie się zerwało: nowe okno PowerShella i te same trzy komendy co w porcji A —
   `cd "…\aws\aws ec2 key"`, `ssh -i "gpw-tracker-key.pem" ec2-user@13.63.105.190`,
   `cd ~/GPW---pulse`.
2. **[EC2, przez SSH]**: godzina. Ma być od `15:55:00` do `15:57:59` UTC. Wcześniej — poczekać
   i powtórzyć. **`15:58` albo później — porcję B pominąć**, dalej dopiero porcja C po 18:32.
```
date
```
3. **[EC2, przez SSH]**: ręczny bieg z udawanym „dziś” = **wczoraj, `2026-10-19`** (nie
   dzisiejsza data). Wynik do pliku w katalogu domowym, nie do `errors.txt`. Na ekranie nic,
   wiersz wraca po kilku sekundach.
```
PRODUCENT_DATA=2026-10-19 KAFKA_BOOTSTRAP=localhost:9094 venv314/bin/python kod/data_ingestion.py > /home/ec2-user/porcja5.txt 2>&1
```
4. **[EC2, przez SSH]**: wynik. Mają wyjść 4 linie: `=== Data pomiaru Producenta: 2026-10-20
   15:5X:XX ===` (prawdziwa godzina UTC, nie udawana data) i po kolei CBF, XTB, SNT z `nowych dni:
   1, wysłane: 0, stan: zapisane, wstrzymane: 1 (ostatnie: 2026-10-20 <cena>)`. Cena = wtorkowe
   zamknięcie u Yahoo, zaokrąglone do 2 miejsc, z kropką (np. `194.3`). Warianty:
   - Yahoo nie ma jeszcze 20.10 → `nowych dni: 0, wysłane: 0, stan: zapisane` bez dopisku (nic
     się nie psuje, ale wstrzymania nie widać);
   - `wysłane: 1` → pamięci brakowało 19.10 (A8 to wyklucza); stop, wkleić.
```
cat /home/ec2-user/porcja5.txt
```
5. **[EC2, przez SSH]**: wtorku nie ma w pamięci. Przy każdej spółce (nagłówek
   `==> companies/….WA.txt <==`) ostatnia linia `2026-10-19 17:00:00, …`.
```
tail -n 1 companies/*.WA.txt
```
6. **[EC2, przez SSH]**: log nietknięty. Ma wyjść **`1503`**.
```
wc -l companies/errors.txt
```

Od teraz do 18:32 nic nie uruchamiamy. O 18:00 `cron` sam wyśle 20.10.

---

## 6. Porcja C — po 18:32 polskiego (16:32 UTC)

1. **PRZEŁĄCZENIE [EC2, przez SSH]**: to samo okno, wiersz `GPW---pulse]$` (po zerwaniu — te
   same trzy komendy co w porcji B, krok 1).
2. **[EC2, przez SSH]**: po `16:32` UTC.
```
date
```
3. **[EC2, przez SSH]**: dwie ostatnie linie startu: `1476:` z `2026-10-19 16:00:0X` i
   **`1504:`** z `2026-10-20 16:00:0X`.
```
grep -n "=== Data pomiaru" companies/errors.txt | tail -n 2
```
4. **[EC2, przez SSH]**: ma wyjść **`1531`**.
```
wc -l companies/errors.txt
```
5. **[EC2, przez SSH]**: blok 28 linii, jak w każdy dzień giełdowy: start; 3 × `nowych dni: 1,
   wysłane: 1, stan: zapisane` **bez** `wstrzymane`; 2 × `value_deserializer`; `Odebrano 3
   wiadomości`; 2 × `pandas` z `silver.py`; 2 × `(2391, 3)` bez `PythonDeprecationWarning`;
   tabela Golda, `Pełna liczba … 117, Prawidłowa … 111`, ranking w 6 liniach; 2 × `S3:
   wysłano`; 2 × `pandas` z `kod/path.py:32`; `Kontrola: Dane 2391 wierszy`; `Kontrola: OK`.
```
tail -n 28 companies/errors.txt
```
6. **[EC2, przez SSH]**: ma nie wyjść nic. Nowe słowo w szukaniu: `wstrzymane`.
```
grep -n -E "Traceback|Error|ERROR|nietknięte|wstrzymane" companies/errors.txt
```
7. **[EC2, przez SSH]**: 3 × **797**, `total` **2391**.
```
wc -l companies/*.WA.txt
```
8. **[EC2, przez SSH]**: **8**, bez zmian.
```
wc -l companies/errors.log
```
9. **[EC2, przez SSH]**: `CURRENT-OFFSET` = `LOG-END-OFFSET` = **2420**, `LAG 0`.
```
~/kafka_2.13-4.3.1/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9094 --describe --group gpw_consumer
```
10. **[EC2, przez SSH]**: dwa pliki `2026-10-20 16:10`; `dane_dzienne.csv` ok. 160100–160150 B
    (19.10: 159927 B, +177–219 B na dzień giełdowy), `ranking.csv` 330–370 B.
```
aws s3 ls s3://gpw-tracker-bucket/gold/ --recursive
```
11. **[EC2, przez SSH]**: w każdym folderze `.gitkeep` i pliki `.csv`.
```
ls -a silver gold
```
12. **[EC2, przez SSH]**: ma nie wyjść nic.
```
git status --short
```
13. **[EC2, przez SSH]**: pamięć 05–20.10 (12 dni). Stan Yahoo z 19.10 18:00: 05–06.10 dalej
    z ceną z 02.10 (201,0 / 341,6 / 138,56); 07–16.10 równe GPW (CBF 199,2 / 196,0 / 200,0 /
    200,0 / 198,0 / 198,2 / 197,4 / 197,5; SNT 342,2 / 342,8 / 344,0 / 355,0 / 347,6 / 338,4 /
    346,8 / 348,8; XTB 135,0 / 137,0 / 139,72 / 135,9 / 135,84 / 136,5 / 140,1 / 147,82); 19.10
    194,3 / 342,4 / 141,48. Zmiany u Yahoo tylko zapisujemy — nie wpływają na porcję. 20.10 = cena
    z kroku B4. Pamięć ma ceny z długim ogonem (np. `199.1999969482422` = 199,20).
```
tail -n 12 companies/*.WA.txt
```
14. **[EC2, przez SSH]**: sprawdzian alarmu na wyniku ręcznego biegu (tylko jeśli w kroku B4 był
    dopisek `wstrzymane`). Bez `>>`, bez stróża. Mają wyjść: 2 linie `pandas` z `kod/path.py:32`,
    `Kontrola: Dane 2391 wierszy`, **`Kontrola: AWARIA - CBF.WA: wstrzymane dni; XTB.WA:
    wstrzymane dni; SNT.WA: wstrzymane dni; Konsument nie ukończył zadania: Brak linii
    'Odebrano'; S3: wysłano 0 razy`**, `Kontrola: brak adresu stróża`. Dwa ostatnie błędy są
    oczekiwane: plik ma tylko linie Producenta.
```
KONTROLA_LOG=/home/ec2-user/porcja5.txt KONTROLA_DATA=2026-10-20 venv314/bin/python kod/control.py
```
15. **[EC2, przez SSH]**: log nietknięty. Ma wyjść **`1531`**.
```
wc -l companies/errors.txt
```
16. **[przeglądarka]** stróż: `Up`, zgłoszenie **#36** ok. 18:30, `GET` z `13.63.105.190`, bez
    `DOWN` na Interii. Zrzut bez pola z adresem zgłoszenia.
17. **[Claude, przeglądarka]** archiwum GPW z 20.10 (po ok. 19:00): cena 20.10 z kroku B4 i C13.

---

## 7. Co może pójść źle

| Sytuacja | Co zobaczymy | Co robimy |
|---|---|---|
| A7 ≠ 1503 | po kontroli 19.10 coś dopisało się do logu | stop, wkleić `tail`; decyzja o `git pull` po rozmowie |
| A8 bez 19.10 | ostatnia linia z 16.10 albo wcześniejsza | stop przed porcją B: ręczny bieg wysłałby 19.10 drugi raz |
| `git pull` nie przewija (`error: Your local changes…`) | błąd zamiast `Fast-forward` | stop, wkleić; **nigdy `git stash`** |
| błąd w A15 albo A16 | tekst błędu, `Traceback` albo `AWARIA` | stop przed 17:55, wkleić; powrót do starego kodu tylko po rozmowie (`git reset --hard 5676575` — EC2 nie ma własnych zmian, `companies/`, `silver/`, `gold/` zostają) |
| B3 bez `KAFKA_BOOTSTRAP` | w pliku `Brak zmiennej …` | nic się nie stało; powtórzyć, jeśli `date` < 15:58 |
| B3 przed 15:55 UTC | `nowych dni: 0`, `dziś pominięte (przed 17:55)` | nic się nie stało; sprawdzian niewykonany |
| B3 z dzisiejszą datą (`2026-10-20`) | `wysłane: 1` | 20.10 poszedł już ręcznie; o 18:00 `nowych dni: 0, wysłane: 0`, `Odebrano 3`; dane dobre, sprawdzian stracony |
| B3 przeciąga się do 18:00 | dwa Producenty piszą pamięć naraz | dlatego start najpóźniej 15:57; jeśli pamięć straci 20.10, w środę przyjdzie alarm `wstrzymane` → nadrobienie po porównaniu z GPW |
| bieg `cron` z nowym kodem pada | `Traceback`, `AWARIA`, mail od stróża | niczego nie powtarzać, wkleić; 20.10 wróci w środę jako wstrzymany → `NADROB=1` po porównaniu z GPW |
| Yahoo nie ma 20.10 o 17:56 | `nowych dni: 0` w B4 | sprawdzian powtórzyć innego dnia giełdowego |

---

## 8. Co porcja 5 zamknie, a czego nie

Po zgodnym wyniku naprawy 1 i 2 spełnią warunki „zrobione” (zasada 9): prawdziwa droga (bieg `cron`
na nowym kodzie i wstrzymanie na prawdziwym Yahoo i Kafce), liczby z tego pliku, głośna awaria
(alarm `wstrzymane` sprawdzony na EC2 w C14), wdrożenie na EC2 — zostanie opis w dokumentacji.

Czego porcja 5 nie sprawdzi:
- **nadrabiania `NADROB=1` na EC2** — tylko kopia z udawanym Yahoo i Kafką (16.10); pierwszy raz
  naprawdę przy pierwszej awarii;
- **zgłoszenia `/fail` z dopiskiem `wstrzymane`** — C14 idzie bez stróża; sama droga `/fail`
  sprawdzona 06.10;
- **Konsumenta bez zmiennej na EC2** — tylko laptop (17.10); w `crontab` zmienna jest (A9).

---

## 9. Wynik (wt. 20.10) — zgodny z przewidywaniami

- **Porcja A (14:56 UTC):** wszystkie 17 kroków co do liczby; `git pull` `5676575..5fa44fc`,
  `21 files changed, 3392 insertions(+), 946 deletions(-)`; A16 `Kontrola: Dane 2388 wierszy`, `OK`.
- **Porcja B:** pierwsze podejście o 14:59:24 UTC, godzinę przed oknem (kroki podane za wcześnie) —
  `dziś pominięte (przed 17:55)`, nic się nie zepsuło. Drugie o **15:55:27 UTC**: 3 × `nowych dni: 1,
  wysłane: 0, stan: zapisane, wstrzymane: 1 (ostatnie: 2026-10-20 …)` — CBF 196.0, XTB 137.56,
  SNT 349.6; pamięć do 19.10, log 1503.
- **Porcja C (16:38 UTC):** blok 1504–1531 (28 linii), 3 × `wysłane: 1` bez `wstrzymane`,
  `Odebrano 3`, `(2391, 3)`, ranking 393,785298 / 262,572490 / 159,259264, `Kontrola: OK`; pamięć
  3 × 797; zakładka 2420; S3 160131 B (+204 B) i 350 B; C14 `AWARIA - CBF.WA: wstrzymane dni; …`
  co do słowa; stróż #36 `GET`, OK.
- Ostrzeżenie Konsumenta ma teraz numer linii `kafka_consumer.py:11` (było `:8`) — trzy nowe linie
  nad nim. Liczba linii bloku bez zmian.
