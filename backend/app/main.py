# Import FastAPI
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

# Import database engine and Base
from app.database import engine, Base

# Import models so SQLAlchemy knows about them
from app import models

from app.database import get_db
from app import schemas, crud, auth


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

# Update an expense
@app.put("/expenses/{expense_id}", response_model=schemas.ExpenseResponse)
def update_expense(
    expense_id: int,
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db)
):
    return crud.update_expense(db, expense_id, expense)    

 # Delete an expense
@app.delete("/expenses/{expense_id}", response_model=schemas.ExpenseResponse)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db)
):
    return crud.delete_expense(db, expense_id)   

# Get total expenses
@app.get("/analytics/total")
def get_total_expenses(db: Session = Depends(get_db)):
    return crud.get_total_expenses(db)   

# Get total expenses by category
@app.get("/analytics/category")
def get_expenses_by_category(db: Session = Depends(get_db)):
    return crud.get_expenses_by_category(db)     


# Register User
@app.post("/register", response_model=schemas.UserResponse)
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    return crud.create_user(db, user)    


# Login User
@app.post("/login")
def login_user(
    user: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    db_user = crud.authenticate_user(
        db,
        user.email,
        user.password
    )

    if not db_user:
        return {
            "message": "Invalid email or password"
        }

    access_token = auth.create_access_token(
        data={
            "sub": db_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }