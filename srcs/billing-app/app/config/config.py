import os

class Config:
    """Billing configuration."""
    SQLALCHEMY_DATABASE_URI = os.getenv("BILLING_DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
    RABBITMQ_QUEUE = "billing_queue"