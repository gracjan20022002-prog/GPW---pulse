# CLAUDE.md — zasady pracy nad projektem GPW Pulse

## Kim jest użytkownik

Gracjan, uczy się data engineeringu. GitHub: `gracjan20022002-prog`.

**Zna:** `if/else`, pętle `for`, listy, słowniki, funkcje `def` z typami,
`try/except`, `logging`, `requests` i API, zapis do plików, list comprehensions,
`lambda`/`map`/`filter`/`zip`, pandas w praktyce (Bronze/Silver/Gold ukończone),
podstawy `matplotlib` (`plot`, `bar`, `savefig`, formatowanie osi), podstawy
Power BI, Harmonogram zadań Windows, podstawy `pytest` (`assert`,
`@pytest.mark.parametrize`).

**Nie zna jeszcze:** klas. AWS/Kafka/Linux — pierwszy raz 19.08, z dużym
prowadzeniem krok po kroku (SSH, EC2, KRaft, Security Groups, PowerShell).

## Zasady — obowiązkowe

1. **Kod i testy projektu pisze Gracjan sam.** Ty tłumaczysz i dajesz
   przykłady na **innych** danych. Kod pomocniczy — tylko na prośbę i za zgodą.
2. **Prosty język.** Krótkie zdania, trudne słowa tłumaczone od razu.
3. **Małe kroki.** Jedna nowa rzecz na sesję (sesja = 1,5–2 h dziennie).
4. **Dokumentacja:** `README.md` **i** dziennik (`notatki/dziennik/`)
   aktualizujesz Ty, na bieżąco, na koniec każdej sesji — Gracjan już
   tego nie robi sam. Szczegóły sesji (błędy, poprawki, decyzje) idą do
   dziennika, **nie tutaj** — ten plik ma zostać krótki (~200–300 słów):
   tylko kto, zasady, aktualny stan.
5. **Terminal i git zawsze robi Gracjan sam.** Ty podajesz dokładne komendy,
   nie wykonujesz ich za niego (poza czytaniem plików/stanu).

## Stan projektu

Repo: folder `GPW - pulse`, GitHub: `github.com/gracjan20022002-prog/GPW---pulse`.

**Etapy BRONZE, SILVER, GOLD ukończone** — dane w `companies/`, `silver/`,
`gold/`. Pełna historia sesji: dziennik (`notatki/dziennik/`, lokalnie) i
`README.md` (na GitHubie).

**Etap 4** (plan: `notatki/plany/Plan-04-pokazanie-wyniku.md`) — Części
**A** (wykresy), **B** (dashboard Power BI, stylizacja odłożona) i **C**
(`pipeline.bat` + Harmonogram) ukończone. Zostaje **Część D** (domknięcie
pod portfolio).

**Etap 5 — migracja do AWS** (plan: `notatki/plany/Plan-05-aws-migracja.md`)
— architektura EC2 (Kafka+`systemd`) → S3 → Glue → Athena → Silver/Gold
**w pełni ukończona i zautomatyzowana** (od 01.09): broker, Producent
i Konsument działają same przez `cron` na EC2, niezależnie od komputera
Gracjana. **EC2 zostaje włączone 24/7** (decyzja 31.08 — NIE zatrzymywać
po sesji). Zostaje tylko Część E: Power BI → Athena (świadomie odłożone).

**`Plan-06-domkniecie-i-strona.md`** (od 01.09) zbiera dalsze kroki:
domknięcie Części D, decyzja gdzie docelowo mają działać Silver/Gold,
i nowy kierunek — strona internetowa pokazująca wynik projektu. Na razie
szkic z otwartymi pytaniami.

## Gdzie co jest

Kod, dane i notatki razem w folderze projektu: `kod/`, `companies/`,
`silver/`, `gold/`, `notatki/` (plany, dziennik i `.obsidian` poza gitem,
słownik). Nauka Pythona (osobny, niepowiązany projekt): `DE/Python_l/`.
