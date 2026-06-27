# Import SQLAlchemy session
from sqlalchemy.orm import Session

# Import database model and schema
from app import models, schemas


# Create a new expense
def create_expense(db: Session, expense: schemas.ExpenseCreate):

    # Convert request data into a database object
    db_expense = models.Expense(
        title=expense.title,
        amount=expense.amount,
        category=expense.category
    )

    # Save to database
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    return db_expense


# Get all expenses
def get_expenses(db: Session):
    return db.query(models.Expense).all()


# Get one expense by ID
def get_expense(db: Session, expense_id: int):
    return db.query(models.Expense).filter(
        models.Expense.id == expense_id
    ).first()