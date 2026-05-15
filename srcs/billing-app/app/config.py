import os

class Config:
    """Billing configuration."""
    SQLALCHEMY_DATABASE_URI = os.getenv("BILLING_DATABASE_URL")
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
    RABBITMQ_QUEUE = "order_queue"