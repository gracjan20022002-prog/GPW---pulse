# Etap 5 — Migracja do AWS (Kafka → S3 → Athena)

Data utworzenia: 2026-08-19

---

## Skąd ten kierunek

`Plan-ogolny.md` miał od początku, na liście „co dalej po miesiącu",
punkt: „Databricks — przeniesienie tego samego do chmury". To był luźny
pomysł, bez konkretnej architektury — coś do rozważenia „kiedyś później".

19.08 Gracjan obejrzał na YouTube *Stock Market Kafka Real Time Data
Engineering Project* (kanał Darshil Parmar) i zdecydował, że to on
wyznacza dalszy, konkretny kierunek: zamiast Databricks, dane mają
wędrować z lokalnego komputera przez EC2 aż do AWS Athena. Ten plan
zastępuje ten luźny punkt konkretną architekturą.

Film obejrzany nie bezpośrednio (brak dostępnej transkrypcji), tylko przez
oficjalne repozytorium GitHub autora, podane w opisie filmu jako materiały
źródłowe — README z listą technologii, kod Producenta/Konsumenta Kafki
i dokładne komendy setupu.

---

## Co pokazuje materiał źródłowy — wnioski

Architektura, w uproszczeniu:

```
Dane źródłowe → Producent Kafki (Python) → Kafka (broker na EC2)
→ Konsument Kafki (Python) → S3 → Glue Crawler → Glue Catalog → Athena (SQL)
```

- **Producent** — skrypt Python (biblioteka `kafka-python`), łączy się
  z brokerem Kafki i wysyła każdy rekord jako wiadomość (w materiale
  źródłowym: JSON) na wybrany „topic" (nazwany kanał w Kafce).
- **Konsument** — osobny skrypt Python, subskrybuje ten sam topic,
  i dla każdej odebranej wiadomości zapisuje ją jako plik do S3 (przez
  bibliotekę `s3fs`).
- **S3** — magazyn plików w chmurze AWS (jak dysk, tylko w internecie).
  Tu pełni rolę „surowych danych" — dokładny odpowiednik Twojego Bronze.
- **Glue Crawler** — narzędzie AWS, które samo ogląda pliki w S3
  i zgaduje, jakie mają kolumny i typy danych — bez ręcznego pisania
  schematu.
- **Glue Catalog** — miejsce, gdzie Crawler zapisuje wykryty schemat, żeby
  inne narzędzia (Athena) wiedziały, jak czytać te pliki jako tabelę.
- **Athena** — pozwala pisać zwykłe zapytania SQL bezpośrednio na plikach
  w S3, bez uruchamiania żadnej bazy danych. Płacisz tylko za ilość
  faktycznie przeskanowanych danych w zapytaniu, nie za czas działania
  serwera (bo żadnego serwera nie ma — w pełni „serverless").

**Ważna różnica względem tego, co już zbudowane:** materiał źródłowy
(z 2022) używa Kafki z **ZooKeeperem** — starszym, bardziej złożonym
sposobem koordynacji klastra. Broker postawiony 19.08 na EC2 używa
**KRaft** — nowszego trybu, który ZooKeepera nie potrzebuje wcale. Dla
kodu Producenta/Konsumenta w Pythonie nie ma to znaczenia (nie widzą
różnicy, łączą się tak samo) — więc dzisiejsza praca nie tylko się przyda,
ale jest już o krok do przodu względem samego tutorialu.

---

## Jak to się przekłada na GPW Pulse

Bronze/Silver/Gold zostają tym, czym są — trzy kroki oczyszczania danych,
ta sama logika. Zmienia się **gdzie** dane mieszkają i **jak** trafiają
z internetu do pierwszego kroku:

| Dziś (lokalnie) | Docelowo (AWS) |
|---|---|
| `Data ingestion 2.py` pobiera ceny i zapisuje do `companies/*.txt` | Ten sam skrypt pobiera ceny; **historia** leci raz, bezpośrednio do S3, **nowe, bieżące dni** — jako wiadomości Kafki (Producent) |
| — | Nowy skrypt (Konsument) czyta z Kafki, zapisuje bieżące dane do S3 |
| `companies/*.txt` = surowe dane (Bronze) | S3 = surowe dane (Bronze) |
| `silver 1.py` czyta lokalny plik | `silver 1.py` czyta z S3 (albo z Athena przez SQL — do ustalenia po drodze) |
| `gold 1.py` liczy w pandas | zostaje w pandas, LUB część liczenia przenosi się do zapytań SQL w Athenie — do ustalenia po drodze |
| Power BI czyta lokalne `gold/*.csv` | Power BI łączy się bezpośrednio z Athena (ma gotowy konektor) |

Broker Kafki postawiony 19.08 na EC2 to właśnie środkowy element tej
architektury — już gotowy, już potwierdzony jako działający z zewnątrz.

**Aktualizacja 20.08 — historia i bieżące dane rozdzielone.** Pierwotny
pomysł (wszystko przez Kafkę, wiadomość po wiadomości, tak jak
w materiale źródłowym) doprecyzowany po propozycji Gracjana: **historia**
(dane już zebrane lokalnie, ~751 dni × 3 spółki) idzie **raz, bezpośrednio
do S3** (`boto3.upload_file`, bez Kafki) — dla jednorazowego transferu
gotowych danych Kafka niczego nie dodaje. Kafka obsługuje tylko to, co
faktycznie jest strumieniem: codzienne nowe ceny, jedna (czasem więcej,
przy doganianiu zaległości) wiadomość dziennie. Dodatkowy powód: zapisanie
każdej wiadomości jako osobnego pliku w S3 (dosłowny wzorzec z materiału
źródłowego) z czasem tworzy tysiące malutkich plików — źle się to skanuje
przez Athenę. Konsument (Część C) będzie zapisywał rzadziej, ale większymi
partiami.

---

## Stan na start — już zrobione (19.08)

Cała sesja 19.08 poszła w budowę pierwszego klocka: **Kafka z KRaft na
EC2, dostępna z zewnątrz.** Po drodze pokonane, jedno po drugim: brak
pamięci przy starcie JVM, zajęty port po procesie-sierocie po zerwanej
sesji SSH, limit długości linii poleceń w windowsowych skryptach `.bat`,
konflikt starej i nowej wersji Javy, nieznaleziony plik konfiguracyjny
log4j2, składnia PowerShell — i najważniejsze pojęciowo: różnica między
`listeners` a `advertised.listeners`, oraz to, że EC2 nie ma własnego
publicznego IP fizycznie na karcie sieciowej (hairpin NAT). Szczegóły:
dziennik 19.08.

Na końcu: prawdziwy klient Kafki, uruchomiony lokalnie na Windowsie,
połączył się przez internet z brokerem na EC2 i stworzył topic —
potwierdzone działanie od początku do końca.

**Uwaga na przyszłość:** instancja EC2 jest teraz zatrzymana. Przy
kolejnym starcie publiczny IP się zmieni (brak Elastic IP) —
`advertised.listeners` i reguła Security Group będą wymagały aktualizacji
przed dalszą pracą.

### Dzień 2 (20.08) — odzyskanie po restarcie, drugi listener, pierwszy Producent, S3

Instancja EC2 była zatrzymana od końca poprzedniej sesji — start ujawnił
nową pułapkę: `log.dirs` domyślnie wskazywał na `/tmp`, a `/tmp` na Amazon
Linux czyści się przy starcie systemu. Cały storage z 19.08 zniknął.
Naprawione: `log.dirs` przeniesiony poza `/tmp` (`/home/ec2-user/kafka-logs`),
storage sformatowany od nowa, `advertised.listeners` zaktualizowany na
nowy publiczny IP.

Doszedł **drugi listener** (`INTERNAL`, port 9094, reklamowany jako
`localhost`) — potrzebny, bo klienci uruchomieni **na tej samej
instancji co broker** trafiają na ten sam hairpin NAT co klienci
zewnętrzni próbujący łączyć się przez `localhost`. Teraz działają
równolegle: `9092` (publiczny IP, dla klientów z zewnątrz) i `9094`
(`localhost`, dla klientów na EC2).

Napisany i przetestowany pierwszy prawdziwy Producent w Pythonie
(`kafka-python`, lokalnie w `.venv`) — wiadomość testowa dotarła do
konsumenta na EC2. Utworzony bucket S3, użytkownik IAM
(`AmazonS3FullAccess`, nie `AdministratorAccess`), skonfigurowane AWS CLI
z kluczami poza repozytorium. Historia cen (`companies/*.txt`) wysłana do
S3 przez `boto3` — pierwsze prawdziwe dane GPW Pulse w chmurze.

Szczegóły: dziennik 20.08.

---

## Struktura etapu — wstępny szkic (plan żywy, jak Etap 4)

| Część | Co | Status |
|---|---|---|
| **A** | Kafka z KRaft na EC2, dostępna z zewnątrz i lokalnie (dwa listenery) | ✅ zrobione 19–20.08 |
| **B** | Producent: nowe, bieżące ceny → Kafka. Historia → S3 bezpośrednio | ✅ zrobione — historia wgrana raz 20.08, automatyczny codzienny upload do `bronze/` wyłączony 24.08 (zostaje zamrożoną historią, zgodnie z pierwotnym planem) |
| **C** | Konsument: nowy skrypt, czyta z Kafki, zapisuje bieżące dane do S3 (większe, rzadsze pliki) | ✅ zrobione 21.08 |
| **D** | Glue Crawler + Athena: automatyczny schemat i zapytania SQL na S3 | ✅ zrobione 24.08 — obie tabele (`bronze`, `live`), partycjonowane po `spolka` |
| **E** | Podłączenie Silver/Gold/Power BI do nowego źródła (S3/Athena) | ✅ zrobione 31.08: `silver 1.py` przerobiony na wzór szkicu `pyathena silver.py` (zapytanie SQL łączące `bronze`+`live`), przetestowany osobno i przez cały `pipeline.bat`. Zostaje jeszcze podłączenie Power BI — odłożone na osobną sesję |
| **F** | `cron`/`systemd` na EC2 — broker, Producent i Konsument działają same, codziennie, niezależnie od komputera Gracjana | 🔶 w toku: F1 (broker jako `systemd`) i F2 (Producent+Konsument na EC2, rola IAM) zrobione i przetestowane end-to-end 31.08. Zostaje F3 (`cron`) i F4 (wyłączenie lokalnego Producenta z `pipeline.bat`) — patrz „Część F — rozpiska" niżej |

Jak w Etapie 4 — ta tabela to punkt startowy, nie sztywny plan. Szczegóły
(konkretne sesje, ściągi na nowe narzędzia) dopiszemy, gdy dojdziemy do
każdej części po kolei.

---

## Część F — rozpiska

**Cel:** cały łańcuch zbierania danych (broker, Producent, Konsument) działa
sam na EC2 — bez ręcznego SSH na start, bez zależności od tego, czy
komputer Gracjana jest akurat włączony.

### F1 — Broker jako usługa `systemd` ✅ zrobione i przetestowane 31.08

Zweryfikowane dwa razy: po zwykłym `daemon-reload`+`start`, i (ważniejsze)
po wymuszonym Stop+Start całej instancji w trakcie tej samej sesji (powód:
osobny problem z pamięcią, patrz niżej) — broker wstał sam, bez żadnej
ręcznej interwencji, za oba razy.

Dziś broker startuje się ręcznie: SSH na EC2, `export KAFKA_HEAP_OPTS=...`,
potem `bin/kafka-server-start.sh config/server.properties` — i to za
każdym razem od nowa, bo zmienna środowiskowa nie przeżywa nowej sesji SSH
([[project-etap5-ec2-networking]]).

`systemd` to mechanizm Linuksa do zarządzania usługami działającymi
w tle — start, stop, restart, i (to najważniejsze tutaj) automatyczny
start razem z systemem, bez żadnej interwencji. Kroki:

1. Plik jednostki `kafka.service` w `/etc/systemd/system/`, który:
   - uruchamia `bin/kafka-server-start.sh config/server.properties` jako
     `ec2-user`,
   - ustawia `KAFKA_HEAP_OPTS` przez `Environment=...` w samym pliku —
     koniec z ręcznym `export` co sesję,
   - ma `Restart=on-failure`, żeby sam się podniósł, gdyby padł.
2. `sudo systemctl enable kafka` — broker odpala się sam przy każdym
   starcie instancji.
3. `systemctl start/stop/status kafka` — do ręcznego sterowania
   i sprawdzania, czy żyje.

### F2 — Producent i Konsument przeniesione na EC2 ✅ zrobione i przetestowane end-to-end 31.08

Potwierdzone realną wiadomością (testową, bo akurat żadna nowa data z Yahoo
nie czekała) przechodzącą całą drogę: Producent → Kafka (`localhost:9094`)
→ Konsument → zapis w S3 przez rolę IAM, bez żadnych kluczy na dysku.

Po drodze cztery rzeczy, które nie poszły za pierwszym razem — zapamiętać
na przyszłość:
- **`requests` też trzeba zainstalować** w `venv` na EC2, nie tylko
  `kafka-python`/`boto3` — potrzebuje go Producent (zapytania do Yahoo
  Finance), łatwo o tym zapomnieć, bo to jedyny z trójki skryptów, który
  tego używa.
- **`git clone` tworzy folder tam, gdzie akurat jesteś** — pierwsza próba
  wylądowała w `~/kafka_2.13-4.3.1/GPW---pulse` (bo to nawykowe pierwsze
  „cd" po SSH), nie w `~/GPW---pulse`. Po przeniesieniu (`mv`) `venv`
  trzeba było zbudować od nowa — plik `venv/bin/activate` (i `pip`
  w środku) ma zaszytą na sztywno pełną ścieżkę z miejsca, gdzie powstał,
  i przeniesienie folderu go cicho psuje.
- **`git commit` to nie to samo co `git push`** — commit na Windowsie
  zaktualizował tylko lokalną historię; dopóki nie poszedł `git push`,
  `git pull` na EC2 uparcie ściągał starą wersję kodu, mimo poprawnie
  ustawionej zmiennej `KAFKA_BOOTSTRAP` — myląca sytuacja, dopóki nie
  porównano pliku na GitHubie z lokalnym.
- **Osobny, niezwiązany problem odkryty po drodze: brak pamięci.** Broker
  Kafki + oba skrypty Pythona naraz na małej instancji (913 MB RAM) to
  sporo jak na tak mało pamięci — a swap dodany 19.08 nigdy nie przetrwał
  restartu (nie był w `/etc/fstab`), więc zniknął i SSH przestało
  odpowiadać. Naprawione trwale — pełny opis w [[project-etap5-ec2-networking]].

Oba skrypty (`Data ingestion 2.py`, `kafka_consumer.py`) muszą fizycznie
znaleźć się na EC2:

1. Python + `pip install kafka-python boto3` w osobnym `venv` na EC2
   (Amazon Linux nie ma tego domyślnie) — `pandas` niepotrzebny, bo Silver
   i Gold zostają lokalnie.
2. Kod na EC2 — najprościej `git clone` całego repo z GitHuba na instancję;
   przy zmianach — `git pull`.
3. Adres brokera w obu skryptach zmienia się na `localhost:9094` (listener
   `INTERNAL`, gotowy od 20.08) — łączą się teraz lokalnie na tej samej
   maszynie, nie przez internet i publiczny IP.
4. Dostęp do S3 dla `boto3` w Konsumencie — **nie** kopiować kluczy
   dostępowych na dysk EC2. Właściwy sposób: **IAM Role** przypięta do
   instancji (rola uprawnień, którą EC2 „nosi na sobie" — `boto3` korzysta
   z niej automatycznie, bez żadnego pliku z kluczami). Trzeba sprawdzić,
   czy instancja już taką rolę ma.

### F3 — `cron` dla obu skryptów

Gdy oba działają ręcznie z poziomu EC2 (przez SSH), dopisać wpisy
w `crontab -e` (jako `ec2-user`), żeby odpalały się same, codziennie,
Producent przed Konsumentem.

Uwaga: `cron` ma bardzo ubogie środowisko (nie wczytuje `.bashrc`) — w każdej
linijce potrzebna **pełna ścieżka** do Pythona z `venv`, dokładnie tak, jak
`pipeline.bat` robi to dziś na Windowsie.

### F4 — Lokalny `pipeline.bat`: co dalej z nim

Skoro Producent działa już na EC2, lokalny `pipeline.bat` powinien
przestać go uruchamiać — inaczej dwaj niezależni Producenci (Windows i EC2)
pobieraliby i wysyłali te same dane osobno. Docelowo `pipeline.bat` zostaje
z dwiema liniami: `silver 1.py` i `gold 1.py` (obie już czytają z Athena,
nie potrzebują lokalnego Producenta).

### Do przemyślenia — zanim/w trakcie roboty

1. ~~EC2 24/7 czy dalej Stop/Start?~~ **Rozstrzygnięte 31.08: EC2 zostaje
   włączone 24/7.** Instancja to `t3.micro`; Gracjan ma jeszcze ~173 dni
   darmowego okresu, limit 750h/miesiąc i tak pokrywa ciągłą pracę jednej
   instancji. Zasada niżej („Czego NIE robimy" — zatrzymywać EC2 po sesji)
   jest przez to nieaktualna.
2. **Skąd Producent na EC2 będzie wiedział, które daty już wysłał?** Dziś
   porównuje z lokalnym plikiem `companies/{tick}.txt`
   ([[project-etap5-pipeline-gap]] ma więcej o tym, jak te pliki są dziś
   używane). Na EC2 najprościej zrobić to samo — osobna, własna kopia na
   EC2, niezależna od Twojej na Windowsie. Prostsze na start, można
   zmienić później.
3. **Jak kod trafia na EC2 i zostaje aktualny?** Ręczny `git clone`
   + `git pull` przy każdej zmianie wystarczy na ten projekt — nie trzeba
   niczego bardziej rozbudowanego (żadnego CI/CD).
4. ~~IAM Role dla EC2~~ **Zrobione 31.08** — `GPWTrackerEC2Role`
   (`AmazonS3FullAccess`) stworzona i przypięta, zapis do S3 z EC2
   potwierdzony działający.
5. **Jak zobaczysz błąd, jeśli coś padnie na EC2?** Lokalnie masz
   `companies/errors.log` na wyciągnięcie ręki (tak jak dzisiaj, przy
   naprawie Harmonogramu). Na EC2 ten sam log siedzi na zdalnym dysku —
   trzeba będzie zerknąć przez SSH, albo później pomyśleć o czymś, co da
   znać samo. Nie blokuje startu Części F.

Nowe pojęcia tej części (`systemd`, IAM Role/instance profile) — dopisać
do [[Slownik]].

---

## Czego NIE robimy (na razie)

- ❌ ZooKeeper — zostajemy przy KRaft, nowocześniejszym i już działającym.
- ❌ Przenoszenie całego pipeline'u naraz — krok po kroku, jedna część na
  raz, tak jak dotychczas w projekcie.
- ❌ Rezygnacja z lokalnej wersji na razie — dopóki AWS nie zastąpi jej
  w pełni i sprawdzonie, lokalny pipeline (Harmonogram + `pipeline.bat`)
  zostaje jako działające zabezpieczenie.
- ❌ Więcej niż trzy spółki, dane szybsze niż raz na sekundę/minutę — poza
  zakresem, tak jak dotychczas.
- ~~❌ Zostawianie instancji EC2 uruchomionej bez potrzeby~~ **Nieaktualne
  od 31.08** — decyzja zmieniona, EC2 zostaje włączone 24/7 (patrz punkt 1
  w „Do przemyślenia" wyżej), właśnie po to, żeby Część F mogła działać
  bez udziału Gracjana.

---

## Uczciwa rozmowa o czasie

To duża zmiana architektury, nie dodatek na weekend. Sam pierwszy krok
(Kafka na EC2) zajął całą sesję 19.08, głównie na rozwiązywaniu
nieoczekiwanych problemów infrastruktury — normalne przy pierwszym
kontakcie z AWS, Linuksem i Javą naraz. Realistycznie: podobny rytm jak
Etap 4, czyli **kilka tygodni**, nie dni — każda kolejna część (Producent,
Konsument, Glue, Athena, podłączenie reszty) to osobna porcja nowych
narzędzi do poznania.

---

## Powiązane notatki

- [[Plan-ogolny]] — pierwotnie: Databricks jako „kiedyś, później". Ten
  plan to konkretyzacja tamtego punktu, tyle że w AWS, nie Databricks.
- [[Plan-04-pokazanie-wyniku]] — Część D (domknięcie pod portfolio) wciąż
  w kolejce, niezależnie od tego etapu.
- [[Slownik]] — pojęcia z sesji 19–20.08 (Kafka, KRaft, broker, topic,
  producent/konsument, EC2, Security Group, S3, IAM, daemon, cron)
  dopisane 20.08. Zostają jeszcze: Glue Crawler, Glue Catalog, Athena —
  dopiszemy przy Części D.
