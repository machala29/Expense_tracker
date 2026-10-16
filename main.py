import expenses
import storage
from re import I
from typing import Text
from datetime import datetime




def show_menu():
    """Print the menu options."""
    print("\n--- Expense Tracker ---")
    print("1. Add expense")
    print("2. View all expenses")
    print("3. Summary by category")
    print("4. Delete an expense")
    print("5. Exit")



def get_amount():
  while True:
    Text = input("Price ($): "). strip()
    try:
      amount = float(Text)
    except ValueError:
      print("Please enter a valid number")
      continue
    if amount <= 0:
      print("Amount must be greater than zero")
      continue
    return amount




def get_text(prompt):
    """Ask for text and keep asking until it is not empty."""
    while True:
        text = input(prompt).strip()
        if not text:
            print("Please enter a value, it cannot be empty.")
            continue
        return text



def get_date():
  while True:
    text = input("Date ? "). strip()
    if text == "":
      return datetime.today().strftime("%Y-%m-%d")
    try:
      parsed = datetime.strptime(text, "%Y-%m-%d")
    except ValueError:
      print("Please enter a valid date")
      continue
    return parsed.strftime("%Y-%m-%d")


def handle_add(data):
  amount = get_amount()
  category = get_text("Category: ")
  description = get_text("Description: ")
  date = get_date()
  expenses.add_expense(data, amount, category, description, date)
  storage.save_expenses(data)
  print("Expense added successfully!")


def handle_view(data):
    """Print all expenses in a table, newest first."""
    if not data:
        print("No expenses yet.")
        return

    sorted_list = expenses.get_expenses_newest_first(data)
    headers = ["ID", "Date", "Category", "Description", "Amount"]
    header_format = "{:<6} {:<12} {:<14} {:<22} {:>14}"

    print(header_format.format(*headers))
    print("-" * 72)
    for expense in sorted_list:
        row = [
            str(expense["id"]),
            expense["date"],
            expense["category"],
            expense["description"],
            f"${expense['amount']:,.2f}",
        ]
        print(header_format.format(*row))



def handle_summary(data):
    """Print the total spent in each category, then the overall total."""
    if not data:
        print("No expenses yet.")
        return

    totals = expenses.get_category_totals(data)

    print("Summary by category")
    print("-" * 32)
    for category, total in totals.items():
        print(f"{category:<16}${total:>14,.2f}")
    print("-" * 32)
    print(f"{'TOTAL':<16}${sum(totals.values()):>14,.2f}")




def handle_delete(data):
    """Show the expenses, ask for an ID and delete that expense."""
    if not data:
        print("No expenses yet.")
        return

    handle_view(data)
    text = input("Enter the ID to delete: ").strip()
    try:
        expense_id = int(text)
    except ValueError:
        print("Please enter a whole number, like 2.")
        return

    if expenses.delete_expense(data, expense_id):
        storage.save_expenses(data)
        print("Expense deleted.")
    else:
        print("No expense with that ID.")




def run():
    """Show the menu repeatedly until the user chooses Exit."""
    data = storage.load_expenses()
    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()
        if choice == "5":
            print("Goodbye!")
            break
        elif choice == "1":
            handle_add(data)
        elif choice == "2":
            handle_view(data)
        elif choice == "3":
            handle_summary(data)
        elif choice == "4":
            handle_delete(data)
        else:
            print("Please enter a number from 1 to 5.")




    if __name__ == "__main__":
      run()
