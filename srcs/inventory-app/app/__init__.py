from flask import Flask
from .config import Config
from .models import db

app = Flask(__name__)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from .routes.movies import movies_bp
    from .routes.health import health_bp

    app.register_blueprint(movies_bp)
    app.register_blueprint(health_bp)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    @app.errorhandler(Exception)
    def handle_exception(e):
        if hasattr(e, "code"):
            print(f"Error: {e}, Code: {e.code}")
            if hasattr(e, "description"):
                return {"error": e.description}, e.code
            return {"error": "An error occurred"}, e.code
        return {"error": "Internal Server Error", "message": str(e)}, 500

    return app
