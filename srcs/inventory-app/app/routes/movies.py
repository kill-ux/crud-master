from flask import Blueprint, request
from ..models import Movie, db

movies_bp = Blueprint('movies_bp', __name__, url_prefix='/api/movies')

@movies_bp.route('/', methods=['GET'])
def list_movies():
    search_query = request.args.get('title')
    if search_query:
        movies = Movie.query.filter(Movie.title.ilike(f"%{search_query}%"))
    else:
        movies = Movie.query.all()
    return [movie.to_dict() for movie in movies]

@movies_bp.route('/', methods=['POST'])
def create_movie():
    data = request.get_json()
    if not data or 'title' not in data:
        return {'error': 'Missing title'}, 400

    movie = Movie(title=data['title'], description=data.get('description', ''))
    db.session.add(movie)
    db.session.commit()
    return movie.to_dict(), 201