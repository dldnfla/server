from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from starlette.config import Config

config = Config(".env")
SQLALCHEMY_DATABASE_URL = config("SQLALCHEMY_DATABASE_URL")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
