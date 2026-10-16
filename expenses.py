
from collections import defaultdict


def get_next_id(expenses):
    """Return the next unused ID for a new expense."""
    return max((e["id"] for e in expenses), default=0) + 1


def add_expense(expenses, amount, category, description, date):
    """Create a new expense, add it to the list and return it."""
    new_id = get_next_id(expenses)

    new_expense = {
        "id": new_id,
        "amount": amount,
        "category": category,
        "description": description,
        "date": date,
    }

    expenses.append(new_expense)
    return new_expense


def delete_expense(expenses, expense_id):
    """Remove the expense with the given ID and return True, or False if not found."""
    for expense in expenses:
        if expense["id"] == expense_id:
            expenses.remove(expense)
            return True
    return False


def get_expenses_newest_first(expenses):
  return sorted(expenses, key=lambda x: (x["date"], x["id"]), reverse=True)


def get_category_totals(expenses):
    category_totals = defaultdict(float)
    for expense in expenses:
        category = expense["category"]
        amount = expense["amount"]
        category_totals[category] += amount
    return dict(category_totals)

