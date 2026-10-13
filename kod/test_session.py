from datetime import datetime, date
from zoneinfo import ZoneInfo
from session import dzien_do_pominiecia, STREFA, podziel_daty
UTC = ZoneInfo("UTC")
def test_wtorek_przed_progiem():
    assert dzien_do_pominiecia(datetime(2026, 10, 6, 16, 30, tzinfo=STREFA)) == date(2026, 10, 6)
def test_wtorek_po_progu():
    assert dzien_do_pominiecia(datetime(2026, 10, 6, 18, 0, tzinfo=STREFA)) is None
def test_dokladny_prog():
    assert dzien_do_pominiecia(datetime(2026, 10, 6, 17, 55, tzinfo=STREFA)) is None
def test_minuta_przed():
    assert dzien_do_pominiecia(datetime(2026, 10, 6, 17, 54, tzinfo=STREFA)) == date(2026, 10, 6)
def test_utc_lato_przed():
    assert dzien_do_pominiecia(datetime(2026, 10, 6, 15, 54, tzinfo=UTC)) == date(2026, 10, 6)
def test_utc_lato_po():
    assert dzien_do_pominiecia(datetime(2026, 10, 6, 15, 55, tzinfo=UTC)) is None
def test_zima_przed():
    assert dzien_do_pominiecia(datetime(2026, 10, 26, 16, 00, tzinfo=UTC)) == date(2026, 10, 26)
def test_zima_po():
    assert dzien_do_pominiecia(datetime(2026, 10, 26, 16, 55, tzinfo=UTC)) is None

def test_pl_po_polnocy():
    assert dzien_do_pominiecia(datetime(2026, 10, 6, 23, 30, tzinfo=UTC)) == date(2026, 10, 7)
def test_sobota_rano():
    assert dzien_do_pominiecia(datetime(2026, 10, 10, 10, 00, tzinfo=STREFA)) == date(2026, 10, 10)

def test_podzial_zwykly_dzien():
    assert podziel_daty({"2026-10-13"}, "2026-10-13", False) == (["2026-10-13"], [])
def test_podzial_weekend():
    assert podziel_daty(set(), "2026-10-10", False) == ([], [])
def test_podzial_zalegly_i_dzis():
    assert podziel_daty({"2026-10-12", "2026-10-13"}, "2026-10-13", False) == (["2026-10-13"], ["2026-10-12"])
def test_podzial_tylko_zalegly():
    assert podziel_daty({"2026-10-09"}, "2026-10-10", False) == ([], ["2026-10-09"])
def test_podzial_zalegle_po_kolei():
    assert podziel_daty({"2026-10-09", "2026-10-07", "2026-10-08"}, "2026-10-10", False) == ([], ["2026-10-07", "2026-10-08", "2026-10-09"])
def test_podzial_nadrob():
    assert podziel_daty({"2026-10-12", "2026-10-13"}, "2026-10-13", True) == (["2026-10-12", "2026-10-13"], [])
def test_podzial_nadrob_pusto():
    assert podziel_daty(set(), "2026-10-13", True) == ([], [])
def test_podzial_przyszla_data():
    assert podziel_daty({"2026-10-14"}, "2026-10-13", False) == ([], ["2026-10-14"])

