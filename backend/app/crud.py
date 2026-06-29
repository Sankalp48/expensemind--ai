# Import SQLAlchemy session
from sqlalchemy.orm import Session
from sqlalchemy import func

# NEW (Add this line)
from passlib.context import CryptContext


# Import database model and schema
from app import models, schemas

# NEW (Add this block)
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# Create a new expense
def create_expense(
    db: Session,
    expense: schemas.ExpenseCreate,
    user_id: int
):

    # Convert request data into a database object
    db_expense = models.Expense(
    title=expense.title,
    amount=expense.amount,
    category=expense.category,
    user_id=user_id
)

    # Save to database
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    return db_expense


# Get all expenses
def get_expenses(
    db: Session,
    user_id: int
):
    return db.query(models.Expense).filter(
        models.Expense.user_id == user_id
    ).all()


# Get one expense by ID
def get_expense(db: Session, expense_id: int):
    return db.query(models.Expense).filter(
        models.Expense.id == expense_id
    ).first()


# Update an expense
def update_expense(db: Session, expense_id: int, expense: schemas.ExpenseCreate):

    db_expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id
    ).first()

    if db_expense:

        db_expense.title = expense.title
        db_expense.amount = expense.amount
        db_expense.category = expense.category

        db.commit()
        db.refresh(db_expense)

    return db_expense

# Delete an expense
def delete_expense(db: Session, expense_id: int):

    db_expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id
    ).first()

    if db_expense:
        db.delete(db_expense)
        db.commit()

    return db_expense 


# Hash Password
def get_password_hash(password: str):
    return pwd_context.hash(password)

# Verify Password
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)    


# Create User
def create_user(db: Session, user: schemas.UserCreate):

    print("Password received:", user.password)
    print("Length:", len(user.password))

    hashed_password = get_password_hash(user.password)

    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# Get User by Email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(
        models.User.email == email
    ).first()

# Login User
def authenticate_user(db: Session, email: str, password: str):

    user = get_user_by_email(db, email)

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user    

# Get total expenses
def get_total_expenses(db: Session):

    total = db.query(
        func.sum(models.Expense.amount)
    ).scalar()

    return {
        "total_expenses": total or 0
    }       

# Get total expenses by category
def get_expenses_by_category(db: Session):
    return (
        db.query(
            models.Expense.category,
            func.sum(models.Expense.amount).label("total")
        )
        .group_by(models.Expense.category)
        .all()
    )    

 