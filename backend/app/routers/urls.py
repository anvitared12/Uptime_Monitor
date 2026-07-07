from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload
from app import schemas, models
from app.database import get_db

router = APIRouter(prefix="/urls", tags=["urls"])


@router.post("/", response_model=schemas.UrlRead, status_code=status.HTTP_201_CREATED)
def create_url(payload: schemas.UrlCreate, db: Session = Depends(get_db)):
    """Register a new URL to be monitored.

    - Validates the incoming URL (Pydantic `HttpUrl`).
    - Ensures uniqueness.
    - Inserts a new `URL` row and returns it.
    """
    # Check for existing URL
    existing = db.query(models.URL).filter(models.URL.url == str(payload.url)).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="URL already registered")

    url_obj = models.URL(url=str(payload.url))
    db.add(url_obj)
    db.commit()
    db.refresh(url_obj)
    return url_obj


@router.get("/", response_model=list[schemas.UrlStatusRead])
def list_urls(db: Session = Depends(get_db)):
    """Return all registered URLs with the latest health check."""
    urls = db.query(models.URL).options(selectinload(models.URL.checks)).order_by(models.URL.id).all()
    for url in urls:
        if url.checks:
            url.latest_check = max(url.checks, key=lambda c: c.checked_at)
        else:
            url.latest_check = None
    return urls
