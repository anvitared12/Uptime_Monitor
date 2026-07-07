"""Inspect the `urls` table columns and print schema details.

Run as a module: `python -m app.inspect_urls` from the `backend` folder.
"""
from sqlalchemy import inspect
from app.database import engine

# Ensure models are imported so SQLAlchemy knows about them
import app.models  # noqa: F401


def print_url_columns() -> None:
    inspector = inspect(engine)
    cols = inspector.get_columns("urls")
    print("Columns for 'urls':")
    for c in cols:
        # c is a dict with keys like 'name', 'type', 'nullable', 'default'
        print(f"- {c['name']}: {c['type']} | nullable={c.get('nullable')} | default={c.get('default')}")


if __name__ == "__main__":
    print_url_columns()
