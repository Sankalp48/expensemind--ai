# Import create_engine to connect to the database
from sqlalchemy import create_engine

# Import declarative_base to create database models
from sqlalchemy.orm import declarative_base

# Import sessionmaker to interact with the database
from sqlalchemy.orm import sessionmaker

# Database connection URL
# %40 represents @ in the password
DATABASE_URL = "mariadb+pymysql://root:Root%40123@localhost:3307/expensemind_db"

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create a SessionLocal class for database operations
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all database models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()