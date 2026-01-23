"""
Database models for storing Teller data.
"""
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()


class Account(Base):
    """Represents a financial account (bank or credit card)."""
    __tablename__ = "accounts"
    
    id = Column(String, primary_key=True)  # Teller account ID
    name = Column(String, nullable=False)
    display_name = Column(String, nullable=True)  # Custom user-friendly name
    type = Column(String, nullable=False)  # depository, credit
    subtype = Column(String)  # checking, savings, credit_card
    institution_name = Column(String)
    currency = Column(String, default="USD")
    status = Column(String, default="open")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    balances = relationship("Balance", back_populates="account", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="account", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Account(id={self.id}, name={self.name}, type={self.type})>"


class Balance(Base):
    """Represents account balance at a point in time."""
    __tablename__ = "balances"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(String, ForeignKey("accounts.id"), nullable=False)
    available = Column(Float, nullable=False)
    ledger = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    account = relationship("Account", back_populates="balances")
    
    def __repr__(self):
        return f"<Balance(account_id={self.account_id}, available={self.available}, timestamp={self.timestamp})>"


class Transaction(Base):
    """Represents a financial transaction."""
    __tablename__ = "transactions"
    
    id = Column(String, primary_key=True)  # Teller transaction ID
    account_id = Column(String, ForeignKey("accounts.id"), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String)
    type = Column(String)  # card_payment, ach, etc.
    status = Column(String, default="posted")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    account = relationship("Account", back_populates="transactions")
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, amount={self.amount}, description={self.description})>"


class ScheduledPayment(Base):
    """Represents a scheduled bill payment or subscription."""
    __tablename__ = "scheduled_payments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    account_id = Column(String, ForeignKey("accounts.id"), nullable=True)
    day_of_month = Column(Integer, nullable=False)  # 1-31
    is_active = Column(Boolean, default=True)
    is_recurring = Column(Boolean, default=True)  # True for monthly recurring, False for one-time
    frequency = Column(String, default="monthly")  # monthly, yearly, one-time
    email = Column(String, nullable=True)  # Email associated with subscription/service
    category = Column(String)
    notes = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<ScheduledPayment(name={self.name}, amount={self.amount}, day={self.day_of_month}, frequency={self.frequency})>"


class UserEnrollment(Base):
    """Stores Teller user enrollment and access tokens."""
    __tablename__ = "user_enrollments"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    enrollment_id = Column(String, unique=True, nullable=False, index=True)
    user_id = Column(String, nullable=False, index=True)
    access_token = Column(String, nullable=False)  # TODO: Encrypt this in production!
    institution_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_synced = Column(DateTime)
    is_active = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<UserEnrollment(enrollment_id={self.enrollment_id}, user_id={self.user_id}, active={self.is_active})>"


# Database setup functions
def get_database_url():
    """Get the database URL from environment or use default SQLite."""
    return os.getenv("DATABASE_URL", "sqlite:///teller_home.db")


def create_db_engine():
    """Create and return a database engine."""
    database_url = get_database_url()
    return create_engine(database_url, echo=False)


def init_database():
    """Initialize the database by creating all tables."""
    engine = create_db_engine()
    Base.metadata.create_all(engine)
    print("Database initialized successfully!")
    return engine


def get_session():
    """Get a database session."""
    engine = create_db_engine()
    Session = sessionmaker(bind=engine)
    return Session()


if __name__ == "__main__":
    # Initialize database when run directly
    init_database()
