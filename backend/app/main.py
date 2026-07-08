def read_root():
    """Return a simple health message for the API."""
    return {"status": "ok", "message": "Uptime Monitor API is running!"}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize the FastAPI application
app = FastAPI(
    title="Uptime Monitor API",
    description="A minimal API for the uptime monitor project.",
    version="1.0.0",
)

# Allow the frontend (served from a local static server) to access this API during development.
# In production, restrict origins to trusted domains.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5501",
        "http://localhost:5501",
        "null",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """Return a simple health message for the API."""
    return {"status": "ok", "message": "Uptime Monitor API is running!"}


# Include routers
from app.routers import urls as urls_router

app.include_router(urls_router.router)

# Wire the background scheduler to FastAPI startup/shutdown events
from app.scheduler import scheduler as background_scheduler
from app.database import Base, engine
from app import models  # noqa: F401 - registers SQLAlchemy models before create_all
import logging


@app.on_event("startup")
async def _startup_event():
    # configure basic logging for scheduler output
    logging.basicConfig(level=logging.INFO)
    Base.metadata.create_all(bind=engine)
    background_scheduler.start()


@app.on_event("shutdown")
async def _shutdown_event():
    background_scheduler.shutdown()
