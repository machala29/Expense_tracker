import json

file_path = "data/expenses.json"


def load_expenses():
    """Read expenses from the JSON file and return them as a list."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_expenses(expenses):
    """Write the list of expenses to the json file"""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=4, ensure_ascii=False)
