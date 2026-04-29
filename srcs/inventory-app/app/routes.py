from flask import Blueprint
from .models import Movie

inventory_bp = Blueprint('inventory', __name__, url_prefix='/api/movies')

@inventory_bp.route('/', methods=['GET'])
def list_movies():
    movies = Movie.query.all()
    print(movies)
    return '<p>Hello, World!</p>'