from app.database import engine, Base

def init_db():
    Base.metadata.create_all(engine)