from flask import Flask
from .config import Config
from .models import db

app = Flask(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    from .routes import inventory_bp
    app.register_blueprint(inventory_bp)
    
    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app

