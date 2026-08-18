from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
DATABASE_URL = "sqlite:///./complaints.db"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

#Ye har API request ke liye database connection kholega aur kaam khatam hone par band bhi karega.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()