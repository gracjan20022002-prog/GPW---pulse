from config import ticker
def sprawdz_blok(blok, spolki, dzis):
    bledy = []
    if f"Data pomiaru Producenta: {dzis}" not in blok:
        bledy.append(f"Brak pomiaru producenta z {dzis}")
    zapisane = [linia.split(":")[0] for linia in blok.splitlines() if "stan: zapisane" in linia]
    for spolka in spolki:
        if spolka not in zapisane:
            bledy.append(f"{spolka}: brak 'stan: zapisane'")
    if "Odebrano" not in blok:
        bledy.append("Konsument nie ukończył zadania: Brak linii 'Odebrano'")
    ile = blok.count("S3: wysłano")
    if ile != 2:
        bledy.append(f"S3: wysłano {ile} razy")
    if "Traceback" in blok:
        bledy.append("Wystąpił błąd: Traceback")
    return bledy
def wytnij_blok(tekst):
    linie = tekst.splitlines()
    start = None
    for i in range(len(linie)):
        if linie[i].startswith("=== Data pomiaru Producenta"):
            start = i
    if start is None:
        return ""
    dzisiejsze = [linia for linia in linie[start:] if not linia.startswith("Kontrola:")]
    return "\n".join(dzisiejsze)