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
| **B** | Producent: nowe, bieżące ceny → Kafka. Historia → S3 bezpośrednio | 🔶 w toku: mechanizm i backfill historii do S3 gotowe; wysyłanie nowych dat jeszcze nie wpisane do kodu |
| **C** | Konsument: nowy skrypt, czyta z Kafki, zapisuje bieżące dane do S3 (większe, rzadsze pliki) | nierozpoczęte |
| **D** | Glue Crawler + Athena: automatyczny schemat i zapytania SQL na S3 | nierozpoczęte |
| **E** | Podłączenie Silver/Gold/Power BI do nowego źródła (S3/Athena) | nierozpoczęte |
| **F** | `cron` na EC2 — Producent uruchamia się sam, codziennie, niezależnie od komputera Gracjana | nierozpoczęte |

Jak w Etapie 4 — ta tabela to punkt startowy, nie sztywny plan. Szczegóły
(konkretne sesje, ściągi na nowe narzędzia) dopiszemy, gdy dojdziemy do
każdej części po kolei.

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
- ❌ Zostawianie instancji EC2 uruchomionej bez potrzeby — zatrzymywać
  (Stop, nie Terminate) po każdej sesji, żeby nie zużywać niepotrzebnie
  godzin free tier.

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
