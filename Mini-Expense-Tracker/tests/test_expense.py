# tests/test_expenses.py
import os
from mini_expense import totals_by_day, save_csv, load_csv

def test_totals_by_day_simple():
    entries = [
        {"date":"2025-10-22","category":"Food","amount":100.0,"description":""},
        {"date":"2025-10-22","category":"Transport","amount":50.0,"description":""},
        {"date":"2025-10-23","category":"Groceries","amount":200.0,"description":""},
    ]
    totals = totals_by_day(entries)
    assert totals["2025-10-22"] == 150.0
    assert totals["2025-10-23"] == 200.0

def test_save_and_load(tmp_path):
    # create a temporary file path
    p = tmp_path / "tmp.csv"
    # prepare entries (no interactive calls)
    entries = [{"date":"2025-10-24","category":"Food","amount":120.5,"description":"tea"}]
    # save and load
    save_csv(entries, str(p))
    loaded = load_csv(str(p))
    # cleanup check: one entry with expected date exists
    assert any(e["date"] == "2025-10-24" and abs(e["amount"] - 120.5) < 1e-6 for e in loaded)