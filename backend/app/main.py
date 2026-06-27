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