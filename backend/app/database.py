from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLITE database file location
# This tells SQLAlchemy to create a file named "uptime_monitor.db" in the backend directory.
SQLALCHEMY_DATABASE_URL = "sqlite:///./uptime_monitor.db"

# Create the SQLAlchemy engine
# The engine is the core interface to the database. It manages connections and translates SQL.
# 'connect_args={"check_same_thread": False}' is specific to SQLite.
# By default, SQLite only allows one thread to communicate with it. Since FastAPI is asynchronous
# and handles requests on multiple threads, we disable this check.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class.
# Each instance of SessionLocal will be a single database session (a temporary workspace for database work).
# - autocommit=False: We explicitly control when transactions are committed to the DB (using db.commit()).
# - autoflush=False: We control when objects are flushed (staged) to the DB.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a declarative Base class
# All database models (tables) we define later will inherit from this Base class.
# SQLAlchemy uses this class to keep track of all models and map them to database tables.
Base = declarative_base()

# Dependency to get the database session.
# This yields a session to a FastAPI endpoint and guarantees the session is closed after the request is finished.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
