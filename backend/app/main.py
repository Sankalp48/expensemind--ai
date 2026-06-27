# Import FastAPI
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

# Import database engine and Base
from app.database import engine, Base

# Import models so SQLAlchemy knows about them
from app import models

from app.database import get_db
from app import schemas, crud

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="ExpenseMind AI",
    version="1.0.0",
    description="AI-powered Personal Expense Tracker"
)

# Home route
@app.get("/")
def home():
    return {
        "message": "Welcome to ExpenseMind AI 🚀",
        "status": "Backend is running successfully!"
    }


# Create a new expense
@app.post("/expenses", response_model=schemas.ExpenseResponse)
def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db)
):
    return crud.create_expense(db, expense)

    # Get all expenses
@app.get("/expenses", response_model=list[schemas.ExpenseResponse])
def get_expenses(db: Session = Depends(get_db)):
    return crud.get_expenses(db)

    # Get one expense by ID
@app.get("/expenses/{expense_id}", response_model=schemas.ExpenseResponse)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_expense(db, expense_id)