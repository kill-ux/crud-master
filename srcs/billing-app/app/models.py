from sqlalchemy import Column, Integer, Float
from app.database import Base

class Orders(Base):
    __tablename__ = 'orders'

    id              = Column(Integer, primary_key=True, autoincrement=True)
    user_id         = Column(Integer, nullable=False)
    number_of_items = Column(Integer, nullable=False)
    total_amount    = Column(Float, nullable=False)