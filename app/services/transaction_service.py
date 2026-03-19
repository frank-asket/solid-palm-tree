"""Transaction CRUD and user resolution by phone."""
import uuid
from typing import Sequence

from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.models.user import User


def get_or_create_user_by_phone(db: Session, phone_number: str) -> User:
    """Get user by phone; create if not exists."""
    user = db.query(User).filter(User.phone_number == phone_number).first()
    if user:
        return user
    user = User(id=str(uuid.uuid4()), phone_number=phone_number)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_transaction(
    db: Session,
    user_id: str,
    type_: str,
    amount: float,
    category: str | None = None,
    note: str | None = None,
) -> Transaction:
    """Create and return a new transaction."""
    t = Transaction(
        id=str(uuid.uuid4()),
        user_id=user_id,
        type=type_,
        amount=amount,
        category=category,
        note=note,
    )
    db.add(t)
    db.commit()
    db.refresh(t)
    return t


def get_transactions_for_user(db: Session, user_id: str) -> Sequence[Transaction]:
    """Return all transactions for a user (e.g. for insights)."""
    return db.query(Transaction).filter(Transaction.user_id == user_id).all()
