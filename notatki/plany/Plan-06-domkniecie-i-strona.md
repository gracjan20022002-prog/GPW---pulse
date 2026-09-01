# Plan-06 — Domknięcie starych wątków i strona internetowa

Data utworzenia: 2026-09-01

---

## Skąd ten plan

Sesja 01.09 skończyła Część F Etapu 5 (`cron` na EC2, F3+F4) — całe
zbieranie danych działa teraz samo, bez udziału Gracjana. Przy okazji
rozmowy „co dalej" wyszło kilka osobnych wątków naraz: stare zaległości
(Część D Etapu 4, Część E Etapu 5), nowy pomysł na porządki w nazewnictwie,
pytanie o to, gdzie powinny mieszkać Silver/Gold, i duży, nowy kierunek —
strona internetowa. Ten plik zbiera je wszystkie w jednym miejscu, żeby nie
zgubić żadnego.

**Ten plan jest żywy**, tak jak Plan-04 i Plan-05 — część wątków (1, 2, 5)
jest już dobrze zdefiniowana, część (3, 4) to na razie szkic z otwartymi
pytaniami, dopisywany w miarę postępu.

---

## Sześć wątków, różny stopień gotowości

| # | Wątek | Status |
|---|---|---|
| 1 | Domknięcie Etapu 4, Część D (README, wnioski, porządki) | opisane w Plan-04, nietknięte |
| 2 | Spójność projektu — nazewnictwo, porządki w plikach | nowy dziś, gotowy do zrobienia |
| 3 | Dokąd trafiają Silver/Gold (zostają lokalnie? EC2? S3?) | decyzja do podjęcia, osobna sesja |
| 4 | **Etap 6 — strona internetowa** | wstępny szkic, duży, nowy obszar |
| 5 | Etap 5, Część E — Power BI → Athena | świadomie odłożone (dziś: „jeszcze trochę") |
| 6 | Dalsza mapa (więcej spółek, ESPI, AI) | już w `Plan-ogolny.md`, później |

---

## Wątek 1 — Domknięcie Etapu 4 (Część D)

Pełny opis w [[Plan-04-pokazanie-wyniku]], sekcja „Część D". Trzy sesje,
żadna jeszcze nieodbyta:

- **D1** — rozbudowa górnej części `README.md` pod kątem pracodawcy, jeden
  zapisany wykres jako obrazek.
- **D2** — `notatki/Wnioski.md` (nowy plik — sprawdzone 01.09, jeszcze nie
  istnieje): kilka zdań po ludzku, które wnioski płyną z danych.
- **D3** — przegląd `kod/` (zbędne `print()`, nazewnictwo — patrz Wątek 2
  niżej), finalny commit+push.

---

## Wątek 2 — Spójność: nazewnictwo i porządki

Dziś w `kod/` mieszają się dwa style nazw:

- Ze spacjami i wielką literą: `Data ingestion.py`, `Data ingestion 2.py`,
  `gold 1.py`, `silver 1.py`, `pyathena silver test.py`
- `snake_case`, bez spacji: `kafka_consumer.py`, `config.py`, `wykresy.py`,
  `ranking.py`, `pipeline.py`, `test_plikow.py`

**Uwaga na koszt zmiany, zanim zaczniecie:** `Data ingestion 2.py` to
akurat ten plik, którego nazwę dziś bardzo dokładnie wpisaliście do
`crontab` na EC2 (z cudzysłowem wokół spacji) i do `pipeline.bat`. Zmiana
tej jednej nazwy oznacza wejście z powrotem w oba te miejsca i poprawienie
ścieżki — nie jest to duże, ale to prawdziwa, dodatkowa robota, nie tylko
„zmień nazwę pliku". Pliki bez zewnętrznych odniesień (np. `pyathena
silver test.py` — czysto referencyjny) są bezpieczniejsze do ruszenia
najpierw.

**Zakres do ustalenia w sesji:** ujednolicić na `snake_case` (np.
`data_ingestion.py`, `data_ingestion_2.py` albo lepsza nazwa,
`gold_1.py`→`gold.py`, `silver_1.py`→`silver.py`), zaktualizować wszystkie
miejsca, które odwołują się do starych nazw: `pipeline.bat`, `crontab` na
EC2, ewentualnie Harmonogram Windows (jeśli wskazuje bezpośrednio na plik,
nie tylko na `pipeline.bat`).

---

## Wątek 3 — Dokąd trafiają Silver i Gold

Pytanie z dzisiejszej rozmowy: „przenieść silver/gold na S3?" Zanim
zdecydujemy, jedno rozróżnienie: **S3 przechowuje dane, nie uruchamia
kodu.** To dwa osobne pytania, które łatwo zlać w jedno:

1. **Gdzie fizycznie działa kod** `silver 1.py`/`gold 1.py` — dziś lokalnie
   (Windows, Harmonogram). Mogłyby zamiast tego działać na EC2 (jak
   Producent/Konsument, przez `cron`) — wtedy nie potrzebują Twojego
   komputera w ogóle.
2. **Gdzie ląduje wynik** — dziś lokalne pliki (`silver/clean_data.csv`,
   `gold/*.csv`). Gold mógłby zamiast tego zapisywać do S3 (nowa
   tabela/partycja w Glue/Athena) — wtedy wynik jest osiągalny z zewnątrz
   (np. przez przyszłą stronę), niezależnie od tego, gdzie fizycznie
   liczony.

Te dwie rzeczy można zmieniać osobno albo razem. Argument za którymkolwiek
(albo obiema) wynika wprost z Wątku 4: strona z wykresami „aktualizującymi
się codziennie" potrzebuje, żeby dane były zarówno **świeże bez Ciebie**
(punkt 1), jak i **osiągalne skądś indziej niż Twój dysk** (punkt 2).

Koszt: kolejna instalacja (`pandas` w `venv` na EC2, jeśli pkt 1), a
`t3.micro` już raz padł przez brak pamięci przy mniejszym obciążeniu niż
broker + 2 skrypty + pandas naraz — do przemyślenia razem z pamięcią/swapem.

**Decyzja odłożona na osobną sesję** — nie dziś, zgodnie z zasadą „jedna
nowa rzecz na sesję" (dzisiejsza już zajęta: `cron`).

---

## Wątek 4 — Etap 6: strona internetowa

Pomysł z 01.09, na razie **szkic, nie plan sesji**. Cel, własnymi słowami
Gracjana: strona (niekoniecznie pod publicznym adresem — wystarczy dostęp
przez prywatny link/plik) z ładnym overlayem najważniejszych informacji,
wykresami z Power BI aktualizującymi się codziennie, zakładkami dla
poszczególnych spółek, i słownikiem giełdowym (rozbudowa tego, co już
istnieje w `notatki/Slownik.md` — 445 linii na 01.09, więc nie od zera).

**Otwarte pytania, do rozstrzygnięcia, zanim zacznie się projektowanie:**

1. **Co znaczy „prywatna" strona, technicznie?** Power BI „Publish to
   web" robi stronę faktycznie **publiczną** dla każdego z linkiem — to
   nie to samo, co strona chroniona hasłem/logowaniem. Trzeba wybrać
   konkretny mechanizm, zanim zacznie się cokolwiek budować.
2. **Jaki stos technologiczny?** To zupełnie nowy obszar (HTML/CSS/JS,
   hosting) — dotąd nietknięty w tym projekcie, podobnie nowy jak AWS był
   19.08.
3. **Jak wykresy trafiają na stronę?** Zależy od odpowiedzi na pytanie 1 —
   osadzony Power BI, czy własne wykresy rysowane z danych w Athenie.
4. **Zależność od Wątku 3** — codzienna aktualizacja strony wymaga, żeby
   dane były świeże bez udziału Gracjana (patrz wyżej).

**Realistyczna skala:** to nie dodatek na koniec projektu — to osobny
etap, wielkości porównywalnej do całego Etapu 5 (tygodnie, nie dni), bo
obejmuje kompletnie nowy zestaw umiejętności. Kolejność sesji dopiszemy
dopiero, gdy padną odpowiedzi na pytania 1–3 — tak jak Etap 5 zaczynał się
od jednego zdania i rozrósł się w miarę pracy.

---

## Wątek 5 — Etap 5, Część E: Power BI → Athena

Ostatni kawałek Etapu 5 z 31.08, świadomie odłożony — dziś ponownie: „jeszcze
trochę". Zostaje jako otwarty punkt, bez konkretnej sesji. Warto go
rozważyć **razem** z Wątkiem 4 (strona) przy okazji — jeśli strona ma
pokazywać wykresy, konektor Power BI→Athena może się przydać w obu miejscach
naraz.

---

## Wątek 6 — Dalsza mapa (z `Plan-ogolny.md`, nieco starsza)

Zapisane dawno, wciąż aktualne, kolejność orientacyjna:

1. Więcej spółek (3→30) — tylko zmiana w pliku ustawień, nietknięte.
2. Codzienna automatyzacja — **zrobione 01.09** (Część F).
3. Testy sprawdzające dane — częściowo już jest (`test_plikow.py`).
4. Raporty giełdowe ESPI (web scraping) — nietknięte, trudne.
5. AI do rozpoznawania typu/kategorii raportu — **to jest dokładnie to**,
   o czym Gracjan wspomniał 01.09 („dzienny automatyczny import informacji
   o spółkach i dopasowywanie kategorii przez agentów AI") — ten sam
   pomysł, teraz doprecyzowany. Zanotowane, zdecydowanie nie teraz —
   naturalnie pasuje **po** Wątku 4 (strona), bo potrzebuje miejsca, gdzie
   te informacje ktoś zobaczy.

---

## Co robimy dziś konkretnie

Patrz też rozmowa w dzienniku — rekomendacja: **Wątek 2 (spójność
nazewnictwa)**, nie Wątek 3 (Silver/Gold). Powód: Wątek 3 to nowa decyzja
architektoniczna zasługująca na osobną, wypoczętą sesję, a dzisiejsza
„jedna nowa rzecz" (`cron`) już się wydarzyła. Nazewnictwo jest mniejsze,
bezpieczniejsze, i dobrze domyka dzisiejszy dzień — z zastrzeżeniem
z Wątku 2 o koszcie zmiany nazw, których `crontab` już dziś się nauczył.

---

## Czego NIE robimy teraz

- ❌ Projektowanie całej strony naraz (overlay + zakładki + słownik +
  wykresy) — najpierw odpowiedzi na otwarte pytania z Wątku 4.
- ❌ Przenoszenie Silver/Gold gdziekolwiek dziś — osobna sesja.
- ❌ ESPI, AI-kategoryzacja — dalsza mapa, nie teraz.
- ❌ Rezygnacja z lokalnego Harmonogramu, dopóki nowe rozwiązanie (jeśli
  powstanie) nie jest sprawdzone.

---

## Powiązane notatki

- [[Plan-ogolny]] — punkty 1, 4, 5 z „Co dalej po miesiącu" to Wątek 6 tutaj
- [[Plan-04-pokazanie-wyniku]] — pełny opis Części D (Wątek 1)
- [[Plan-05-aws-migracja]] — cała architektura AWS, Część F zrobiona 01.09
- [[Slownik]] — tu trafi słownictwo giełdowe na stronę (Wątek 4)
