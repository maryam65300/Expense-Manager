# Expense Manager
A desktop budgeting application built with Python and Tkinter, 
designed to help users track expenses across a set budget period.

## About
Built to practise OOP principles including inheritance, polymorphism, 
and layered architecture. The app separates data models, business logic, 
and UI into distinct layers.

## Features
- Set a total budget with a custom date range
- Add, edit, and delete expenses by category
- Category-specific validation (e.g. Food capped at €200, 
  Entertainment at €300)
- Real-time remaining budget display with low-budget warning
- Custom category support

## Tech Stack
- Python 3
- Tkinter (GUI)
- OOP — Inheritance & Polymorphism
- Model-Service-UI (Layered) Architecture

## Architecture
- `Expense` — base model class; `FoodExpense` and `EntertainmentExpense` 
  subclasses override `is_valid()` to demonstrate polymorphism — same 
  method call, different behaviour per class
- `BudgetService` — handles all business logic (CRUD, budget tracking, 
  category totals)
- `ExpenseManagerApp` — Tkinter UI layer, calls service methods only

## UML Diagram
📄 [UML Diagram](uml.png)

##Documentation

