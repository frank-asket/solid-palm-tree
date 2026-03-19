"""Create database tables. Run once: python init_db.py"""
from app.models.database import Base, engine
from app.models.user import User  # noqa: F401 – register model
from app.models.transaction import Transaction  # noqa: F401 – register model

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")
