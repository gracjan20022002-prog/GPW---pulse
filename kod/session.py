from datetime import datetime, time
from zoneinfo import ZoneInfo
STREFA = ZoneInfo("Europe/Warsaw")
PROG = time(17, 55)
def dzien_do_pominiecia(teraz: datetime):
    polska = teraz.astimezone(STREFA)
    if polska.time() < PROG:
        return polska.date()
    return None
