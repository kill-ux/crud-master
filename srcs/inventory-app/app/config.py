import os


class Config:
    """Base configuration."""
    SQLALCHEMY_DATABASE_URI = os.getenv("MOVIES_DATABASE_URL")
    