#!/usr/bin/env python3
# mini_expense.py - very small beginner-friendly expense tracker

import csv                 # CSV read/write
import json                # JSON save
from datetime import datetime
from collections import defaultdict

CSV_FILE = "mini_expenses.csv"
JSON_FILE = "mini_expenses.json"
DATE_FORMAT = "%Y-%m-%d"   # expected date format

# Load existing entries from CSV (if file exists), else return empty list
def load_csv(path):
    try:
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return [
                {"date": r["date"], "category": r["category"], "amount": float(r["amount"]), "description": r["description"]}
                for r in reader
            ]
    except FileNotFoundError:
        return []

# Save entries to CSV
def save_csv(entries, path):
    with open(path, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["date","category","amount","description"])
        writer.writeheader()
        for e in entries:
            writer.writerow({"date": e["date"], "category": e["category"], "amount": f"{e['amount']:.2f}", "description": e["description"]})

# Save entries to JSON
def save_json(entries, path):
    with open(path, "w", encoding='utf-8') as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

# Add new entry after simple validation
def add_entry(entries):
    d = input("Date(YYYY-MM-DD): ").strip()
    # simple date check
    try:
        datetime.strptime(d, DATE_FORMAT)
    except Exception:
        print("Invalid date format. Use YYYY-MM-DD.")
        return
    cat = input("Category: ").strip() or "Misc"
    amt_s = input("Amount (number): ").strip()
    try:
        amt = float(amt_s)
    except Exception:
        print("Invalid amount.")
        return
    desc = input("Description (optional): ").strip()
    entries.append({"date": d, "category": cat, "amount": amt, "description": desc})
    print("Added.")

# Print all entries
def list_entries(entries):
    if not entries:
        print("No entries.")
        return
    print(f"{'Date':10} | {'Category':10} | {'Amount':8} | Description")
    print("-"*55)
    for e in sorted(entries, key=lambda x: x["date"]):
        print(f"{e['date']:10} | {e['category'][:10]:10} | {e['amount']:8.2f} | {e['description']}")


# Totals by day
# Replace the old totals_by_day with these two functions

def totals_by_day(entries):
    """
    Compute totals per day and return a dict where
    key = 'YYYY-MM-DD' and value = sum(amounts).
    This function does NOT print; it only returns data (good for tests).
    """
    totals = defaultdict(float)
    for e in entries:
        # ensure amount is float (in case it was string)
        totals[e["date"]] += float(e["amount"])
    return dict(totals)


def print_totals_by_day(entries):
    """
    Print totals by day using totals_by_day().
    Separate function so tests can use totals_by_day() directly.
    """
    totals = totals_by_day(entries)
    if not totals:
        print("No data.")
        return
    print("Totals by day:")
    for day in sorted(totals):
        print(f"{day} : {totals[day]:.2f}")

# Simple menu loop
def main():
    entries = load_csv(CSV_FILE)
    while True:
        print("\nMenu: 1) Add  2) List  3) Totals by day  4) Save & Exit")
        choice = input("Choose (1-4): ").strip()
        if choice == "1":
            add_entry(entries)
        elif choice == "2":
            list_entries(entries)
        elif choice == "3":
            print_totals_by_day(entries)
        elif choice == "4":
            save_csv(entries, CSV_FILE)
            save_json(entries, JSON_FILE)
            print(f"Saved to {CSV_FILE} and {JSON_FILE}. Bye!")
            break
        else:
            print("Choose 1,2,3 or 4.")

if __name__ == "__main__":
    main()
