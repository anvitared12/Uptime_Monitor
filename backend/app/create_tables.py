"""Small utility to create database tables and list them.

Run this script to ensure the SQLite database file and the `urls` table are created.
"""
from sqlalchemy import inspect
from app.database import engine, Base


def create_tables() -> None:
    """Import models so they register on `Base`, create tables, and print names."""
    # Import models module so SQLAlchemy model classes are registered on Base
    # (they define tables via declarative_base inheritance).
    import app.models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print("Tables in database:", tables)


if __name__ == "__main__":
    create_tables()
