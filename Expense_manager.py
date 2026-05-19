import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# OOP MODELS (Inheritance)

class Expense:
    _id_counter = 1

    def __init__(self, category, amount, description):
        self.id = Expense._id_counter
        Expense._id_counter += 1
        self.category = category
        self.amount = amount
        self.description = description

    def is_valid(self):
        return self.amount > 0


class FoodExpense(Expense):
    def is_valid(self):
        return 0 < self.amount <= 200


class EntertainmentExpense(Expense):
    def is_valid(self):
        return 0 < self.amount <= 300



# SERVICE LAYER

class BudgetService:
    def __init__(self):
        self.total_budget = None
        self.start_date = None
        self.end_date = None
        self.expenses = []  # LIST

    def set_budget(self, amount, start_date, end_date):
        self.total_budget = amount
        self.start_date = start_date
        self.end_date = end_date

    def add_expense(self, expense):
        self.expenses.append(expense)

    def delete_expense(self, expense_id):
        self.expenses = [e for e in self.expenses if e.id != expense_id]

    def get_used_amount(self):
        return sum(e.amount for e in self.expenses)

    def get_remaining(self):
        return self.total_budget - self.get_used_amount()

    def get_category_totals(self):
        totals = {}  # DICTIONARY
        for e in self.expenses:
            totals[e.category] = totals.get(e.category, 0) + e.amount
        return totals



# UI APPLICATION

class ExpenseManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Expense Manager")
        self.geometry("820x520")
        self.resizable(False, False)

        self.service = BudgetService()
        self.categories = ["Food", "Entertainment", "Transport", "Rent", "Other"]

        self._setup_style()
        self.show_home_page()

    def _setup_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"))
        style.configure("Warn.TLabel", foreground="red", font=("Segoe UI", 10, "bold"))

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    # HOME PAGE

    def show_home_page(self):
        self.clear_screen()

        ttk.Label(self, text="Expense Manager", style="Header.TLabel").pack(pady=30)

        ttk.Button(self, text="➕ Add Expense", width=30,
                   command=self.start_add_expense).pack(pady=10)

        ttk.Button(self, text="📋 View Expense List", width=30,
                   command=self.show_expense_list).pack(pady=10)

    
    
    # BUDGET SETUP

    def start_add_expense(self):
        if self.service.total_budget is None:
            self.ask_budget()
        else:
            self.open_expense_dialog()

    def ask_budget(self):
        dialog = tk.Toplevel(self)
        dialog.title("Set Budget")
        dialog.geometry("350x260")
        dialog.grab_set()

        ttk.Label(dialog, text="Total Budget").pack(pady=10)
        budget_entry = ttk.Entry(dialog)
        budget_entry.pack()

        ttk.Label(dialog, text="Budget Period").pack(pady=10)

        start_entry = ttk.Entry(dialog)
        start_entry.pack()
        start_entry.insert(0, "Start Date (YYYY-MM-DD)")

        end_entry = ttk.Entry(dialog)
        end_entry.pack()
        end_entry.insert(0, "End Date (YYYY-MM-DD)")

        def save_budget():
            try:
                amount = float(budget_entry.get())
                start = datetime.strptime(start_entry.get(), "%Y-%m-%d").date()
                end = datetime.strptime(end_entry.get(), "%Y-%m-%d").date()

                if amount <= 0 or end < start:
                    raise ValueError

                self.service.set_budget(amount, start, end)
                dialog.destroy()
                self.open_expense_dialog()

            except ValueError:
                messagebox.showerror("Error", "Invalid budget or dates")

        ttk.Button(dialog, text="Save Budget", command=save_budget).pack(pady=20)



    # EXPENSE LIST PAGE

    def show_expense_list(self):
        self.clear_screen()

        top = ttk.Frame(self)
        top.pack(fill="x", padx=10, pady=10)

        ttk.Button(top, text="⬅ Home", command=self.show_home_page).pack(side="left")
        ttk.Button(top, text="➕ Add Expense", command=self.start_add_expense).pack(side="right")

        ttk.Label(self,
                  text=f"Budget Period: {self.service.start_date} → {self.service.end_date}"
                  ).pack(pady=5)

        columns = ("category", "amount", "description")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col.title())

        self.tree.pack(padx=10, pady=10, fill="x")

        btns = ttk.Frame(self)
        btns.pack()

        ttk.Button(btns, text="✏ Edit", command=self.edit_expense).grid(row=0, column=0, padx=5)
        ttk.Button(btns, text="🗑 Delete", command=self.delete_expense).grid(row=0, column=1, padx=5)

        self.footer = ttk.Frame(self)
        self.footer.pack(fill="x", padx=10, pady=10)

        self.warning_label = ttk.Label(self.footer, style="Warn.TLabel")
        self.warning_label.pack(side="left")

        self.remaining_label = ttk.Label(self.footer)
        self.remaining_label.pack(side="right")

        self.refresh_table()

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for e in self.service.expenses:
            self.tree.insert(
                "", "end", iid=e.id,
                values=(e.category, f"${e.amount:.2f}", e.description)
            )

        remaining = self.service.get_remaining()
        self.remaining_label.config(text=f"Remaining: ${remaining:.2f}")

        self.warning_label.config(
            text="⚠ Low budget remaining!" if remaining < 50 else ""
        )



    # ADD / EDIT EXPENSE

    def open_expense_dialog(self, expense=None):
        dialog = tk.Toplevel(self)
        dialog.title("Add Expense" if not expense else "Edit Expense")
        dialog.geometry("400x300")
        dialog.grab_set()

        ttk.Label(dialog, text="Category").pack(pady=5)
        category_var = tk.StringVar(value=expense.category if expense else self.categories[0])

        category_box = ttk.Combobox(
            dialog, values=self.categories, textvariable=category_var, state="readonly"
        )
        category_box.pack()

        custom_entry = ttk.Entry(dialog)

        def on_change(event):
            if category_var.get() == "Other":
                custom_entry.pack(pady=5)
            else:
                custom_entry.pack_forget()

        category_box.bind("<<ComboboxSelected>>", on_change)

        ttk.Label(dialog, text="Amount").pack(pady=5)
        amount_entry = ttk.Entry(dialog)
        amount_entry.pack()
        if expense:
            amount_entry.insert(0, expense.amount)

        ttk.Label(dialog, text="Description").pack(pady=5)
        desc_entry = ttk.Entry(dialog)
        desc_entry.pack()
        if expense:
            desc_entry.insert(0, expense.description)

        def save():
            try:
                amount = float(amount_entry.get())
                if amount <= 0:
                    raise ValueError

                category = category_var.get()
                if category == "Other":
                    category = custom_entry.get().strip()
                    if not category:
                        raise ValueError
                    if category not in self.categories:
                        self.categories.insert(-1, category)

                if category == "Food":
                    new_expense = FoodExpense(category, amount, desc_entry.get())
                elif category == "Entertainment":
                    new_expense = EntertainmentExpense(category, amount, desc_entry.get())
                else:
                    new_expense = Expense(category, amount, desc_entry.get())

                # POLYMORPHISM APPLIED
                if not new_expense.is_valid():
                    raise ValueError

                if expense:
                    expense.category = new_expense.category
                    expense.amount = new_expense.amount
                    expense.description = new_expense.description
                else:
                    self.service.add_expense(new_expense)

                dialog.destroy()
                self.refresh_table()

            except ValueError:
                messagebox.showerror(
                    "Invalid Expense",
                    "Amount not allowed for this category"
                )

        ttk.Button(dialog, text="Save", command=save).pack(pady=20)

    def edit_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Select", "Select an expense")
            return

        expense_id = int(selected[0])
        expense = next(e for e in self.service.expenses if e.id == expense_id)
        self.open_expense_dialog(expense)

    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            return
        self.service.delete_expense(int(selected[0]))
        self.refresh_table()


# RUN APP

if __name__ == "__main__":
    app = ExpenseManagerApp()
    app.mainloop()
