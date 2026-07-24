from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
