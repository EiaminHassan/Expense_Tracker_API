# Expense Tracker API (Learning Project)

Basically I am learning FastAPI and doing hands-on work through this project.

## What it does

- Simple CRUD API for expenses
- Uses PostgreSQL for storage
- Includes basic user creation and listing

## Endpoints

Expenses

- POST /expenses/ - create expense
- GET /expenses/ - list expenses
- GET /expenses/{expense_id} - get expense by id
- PUT /expenses/{expense_id} - update expense by id
- DELETE /expenses/{expense_id} - delete expense by id

Users

- POST /users/ - create user
- GET /users/ - list users

## Requirements

- Python 3.10+
- PostgreSQL running locally
- Packages: fastapi, uvicorn, psycopg2, sqlalchemy, pydantic
- Plan: add a requirements.txt for dependency installs

## Quick start

1. Create a Postgres database named expenses_db
2. Update credentials in app/database.py if needed
3. Install dependencies
4. Run the app

Example run:

- fastapi dev app/main.py

## Notes

- Tables are defined in app/models.py; there is no automatic create-all hook in code.
- The Expense model has: id, description, amount, date.
