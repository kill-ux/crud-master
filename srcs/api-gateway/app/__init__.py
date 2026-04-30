from flask import Flask


def create_app():
    app = Flask(__name__)
    
    from .routes import gateway_bp
    app.register_blueprint(gateway_bp)
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        if hasattr(e, "code"):
            print(f"Error: {e}, Code: {e.code}")
            if hasattr(e, "description"):
                return {"error": e.description}, e.code
            return {"error": "An error occurred"}, e.code
        return {"error": "Internal Server Error", "message": str(e)}, 500

    return app
