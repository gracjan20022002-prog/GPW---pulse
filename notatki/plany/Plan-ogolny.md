# Plan ogólny — cały projekt na jednej stronie

Data utworzenia: 2026-07-21

---

## O czym jest ten projekt

Chcemy zbudować program, który **sam pobiera dane o spółkach z giełdy,
porządkuje je i wyciąga z nich wnioski.**

Na końcu ma powstać coś, co pokażesz pracodawcy i powiesz: „to zbudowałem ja,
i umiem wytłumaczyć każdą linijkę".

---

## Uczciwa rozmowa o czasie

Powiedziałeś: około miesiąca, 2 godziny dziennie. To daje mniej więcej **60 godzin**.

Pierwotny projekt (30 spółek, raporty giełdowe, sztuczna inteligencja, wyszukiwarka
po znaczeniu tekstu) to praca na **pół roku** dla kogoś, kto ma już doświadczenie.
W 60 godzin się nie zmieści i nie chcę Cię okłamywać.

**Co zmieści się w miesiąc:** kompletny, działający, mały projekt.
Od pobrania danych do wykresu. Wszystko Twoje, wszystko rozumiesz.

To jest **lepsze portfolio** niż duży projekt skończony w 40%.
Pracodawca woli zobaczyć coś małego, co działa, niż coś dużego, co się nie uruchamia.

Duże rzeczy (raporty giełdowe, AI) dokładamy w miesiącu drugim i trzecim.

---

## Mapa: pięć etapów

Wyobraź sobie fabrykę. Surowiec wjeżdża brudny, wyjeżdża gotowy produkt.

```
   INTERNET                TWÓJ KOMPUTER                     TY
      │
      ▼
 ┌──────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐
 │  BRONZE  │ ───► │  SILVER  │ ───► │   GOLD   │ ───► │  WYKRES  │
 │  surowe  │      │  czyste  │      │ policzone│      │  raport  │
 └──────────┘      └──────────┘      └──────────┘      └──────────┘
```

### Etap 0 — Przygotowanie (2–3 dni)

Ustawiamy komputer do pracy. Instalujemy to, czego brakuje.
Uczysz się, czym jest **środowisko wirtualne** i po co się je robi.
Zakładamy nowe, puste repozytorium na GitHubie.

*Efekt: umiesz jednym ruchem zacząć pracę i zapisać ją na GitHubie.*

### Etap 1 — BRONZE: pobieranie danych (około tygodnia)

Piszesz program, który pobiera ceny akcji **trzech spółek** i zapisuje je na dysk.
Bez zmian, bez poprawiania — dokładnie tak, jak przyszły.

Umiesz już 70% tego, co tu potrzebne: `requests`, `try/except`, `logging`,
zapis do pliku. To rozbudowa Twojej lekcji „Python 4" i „Python 5".

*Efekt: masz na dysku pliki z prawdziwymi danymi giełdowymi.*

### Etap 2 — SILVER: czyszczenie (około tygodnia)

Surowe dane są brzydkie. Daty jako tekst, liczby z przecinkami, puste miejsca,
te same dane dwa razy. Piszesz program, który to prostuje.

Tu poznajesz **pandas** — bibliotekę do pracy z tabelami. To będzie
najtrudniejszy, ale najbardziej przydatny etap całego projektu.

*Efekt: jedna czysta tabela, z której da się liczyć.*

### Etap 3 — GOLD: liczenie (4–5 dni)

Z czystych danych liczysz rzeczy, które kogoś interesują.
Na przykład: o ile procent zmieniła się cena, która spółka rosła najszybciej,
w którym miesiącu było najwięcej wahań.

*Efekt: tabela z gotowymi odpowiedziami, nie z surowymi liczbami.*

### Etap 4 — Pokazanie wyniku (3 dni ~~— nieaktualne~~, patrz niżej)

Wykres i krótki opis. Plus porządny plik `README` na GitHubie —
to pierwsza rzecz, którą zobaczy pracodawca.

*Efekt: projekt, który da się pokazać.*

**Aktualizacja 2026-08-10:** zakres tego etapu rozszerzony na prośbę
Gracjana — wykresy w Pythonie i Power BI, wstęp do automatyzacji, ogólna
rozbudowa pod portfolio. Realistyczny czas: ok. 3 tygodnie, nie 3 dni.
Szczegóły: [[Plan-04-pokazanie-wyniku]].

---

## Co dalej, po miesiącu

Kolejność, w jakiej będziemy dokładać, gdy poczujesz się pewnie:

1. więcej spółek (z 3 na 30) — to tylko zmiana w pliku ustawień
2. automatyczne uruchamianie codziennie
3. testy sprawdzające, czy dane są sensowne
4. raporty giełdowe ESPI (trudne: trzeba czytać strony internetowe)
5. sztuczna inteligencja do rozpoznawania typu raportu
6. ~~Databricks~~ — **Aktualizacja 2026-08-19:** zamiast Databricks,
   konkretny kierunek: migracja do AWS (Kafka → S3 → Glue → Athena),
   zainspirowana tutorialem o danych giełdowych. Już rozpoczęta —
   szczegóły: [[Plan-05-aws-migracja]].

---

## Zasada, którą się kierujemy

**Każdy etap ma działać, zanim zaczniemy następny.**

Widzę, że masz repozytorium `sql_data_warehouse_project` z samym plikiem README —
zaczęte i porzucone. To bardzo częste i nie jest powodem do wstydu, ale chcę,
żeby tym razem było inaczej.

Dlatego po każdym etapie masz mieć coś, co **realnie działa i co widać**.
Nawet jeśli jest małe.

---

## Powiązane notatki

- [[Plan-01-bronze]] — szczegóły pierwszego etapu
- [[Codzienna-rutyna]] — jak zacząć pracę każdego dnia
- [[Stare-repo-co-to-bylo]] — wyjaśnienie plików ze starego projektu
