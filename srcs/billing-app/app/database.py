from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import get_env_variable


BILLING_DATABASE_URL = get_env_variable("BILLING_DATABASE_URL")
engine = create_engine(BILLING_DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)