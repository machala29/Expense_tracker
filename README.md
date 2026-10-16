# Expense Tracker (CLI)

A simple terminal program for recording and reviewing your spending in naira. You pick an option from a menu, and your expenses are saved to a file, so they are still there the next time you open the program.

This is Project 1 of my Python learning roadmap (Phase 1: Foundations). I built it in Google Colab, one small function at a time.

## What it can do

1. **Add an expense.** Enter the amount, a category (for example Transport, Food, Data/Airtime, Rent), a short description and the date. If you press Enter on the date, today's date is used.
2. **View all expenses.** Shows every expense in a table, newest first.
3. **Summary by category.** Shows the total spent in each category, and the overall total.
4. **Delete an expense.** Pick the expense by its ID.
5. **Exit.**

Everything is stored in `data/expenses.json`. The file is loaded when the program starts and saved after every change.

## Input checks

- The amount must be a positive number. Letters, negatives and zero are rejected, and the program asks again.
- Category and description cannot be empty.
- The date must be a real date in `YYYY-MM-DD` format. Something like `2026-02-30` is rejected.
- If `expenses.json` is missing, empty or corrupted, the program starts with an empty list instead of crashing.

## Project structure

```
expense-tracker/
├── main.py          # the menu and the screens the user sees
├── storage.py       # load_expenses(), save_expenses()
├── expenses.py      # add, delete, sort and summarise logic
├── data/
│   └── expenses.json
└── README.md
```

I kept the menu code, the file code and the logic code in separate files. `expenses.py` has no `input()` or `print()` in it, so the logic can be tested on its own and reused later, for example behind a website.

## How to run it

**In Google Colab:** create the three files with `%%writefile` (the magic command must be the very first line of the cell), then start the program from a separate cell:

```python
import main
main.run()
```

**On your own computer:** make sure the `data` folder exists, then run:

```
python main.py
```

(This needs these two lines at the bottom of `main.py`.)

```python
if __name__ == "__main__":
    run()
```

## Example

```
--- Expense Tracker ---
1. Add expense
2. View all expenses
3. Summary by category
4. Delete an expense
5. Exit
Enter your choice:
```

## How I tested it

I ran the test cases from the project brief by hand: adding a valid expense, entering `abc` and `-500` as the amount, entering `2026-02-30` as the date, closing and reopening the program to check the data was still there, deleting an existing ID and one that does not exist, starting with no JSON file, and checking the category totals add up.

## Challenges I ran into

**1. Learning how Colab works.** Colab is a notebook, not a folder of `.py` files. I had to learn that `%%writefile` turns a cell into a real file, and that it only works if it is the very first line of the cell. Putting anything above it gave a `Line magic function not found` error. I also re-ran my folder setup cell by mistake and ended up with `expense-tracker` folders nested inside each other, four levels deep. The fix was to delete the folder and run the setup cell only once.

**2. Indentation errors.** Python uses indentation to decide what belongs inside a function or loop. I got an `IndentationError` because the spacing was not consistent, and a `'return' outside function` error because my code was not inside a `def`. I now use 4 spaces everywhere and paste whole functions at once.

**3. Python remembering the old version of my file.** After editing `storage.py`, I still got `AttributeError` because Python had already imported the old copy. I fixed it by clearing the module before importing it again with `sys.modules.pop(...)`.

**4. Small typos with big effects.** Calling `get_expenses_newest_first` when I had named the function `get_expenses_newsest_first` gave an `AttributeError`, and the same thing happened with `get_category_total` and `get_category_totals`. Python cannot guess what you meant. I learned to read the last line of an error message first and check my spelling.

**5. Generating a new ID after a delete.** The first idea, `len(expenses) + 1`, breaks as soon as something is deleted. With IDs 1, 2 and 3, deleting ID 2 leaves two items, so the next ID would be 3, which is already used. I worked out the next ID from the largest existing ID instead, using `max()` with `default=0` so an empty list starts at 1.

**6. A function pasted into the middle of another function.** When I added `delete_expense`, I pasted it inside `add_expense` and cut it in half. Nothing crashed, but adding an expense silently did nothing, so my test showed an empty list. Printing the file with `!cat expenses.py` showed me what had happened. Now I paste new functions at the bottom of the cell.

**7. Sorting with a tie.** I sorted by date, but two expenses on the same day came out in the wrong order. My key was `(x["date"])`, and the brackets alone do nothing. It needed a comma to make a pair, `(x["date"], x["id"])`, so the ID breaks the tie.

**8. Dates that look right but sort wrong.** `strptime` accepts `2026-1-5` as a valid date, but as text it does not sort like `2026-01-05`. I convert the parsed date back to text with `strftime("%Y-%m-%d")` so every date is stored in the same format.

**9. Saving the wrong list.** My first version of the add function called `load_expenses()` twice. Each call returns a fresh list from the file, so the expense was added to one list and a different list was saved. The program said "Expense added" but nothing was saved. The fix was to load the list once in `run()` and pass that same list to every function.

**10. A function ignoring its input.** My `get_text` function had the prompt typed directly inside `input(...)`, so it kept asking "What Category?" even when I wanted a description. The fix was to use the `prompt` parameter instead.

**11. Mixing up names.** Importing the `expenses` module means I can never use `expenses` as the name of my list in `main.py`, or I would overwrite the module. I used `data` for the list instead.

## What I would improve next

- Filter expenses by month.
- Set a monthly budget and warn when it is passed.
- Edit an existing expense.
- Create the `data` folder automatically if it does not exist.
- Replace the JSON file with a database and put a web front end on top.
