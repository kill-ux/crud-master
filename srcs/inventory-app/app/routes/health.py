from flask import Blueprint, request

health_bp = Blueprint('movies_bp', __name__, url_prefix='status')

@health_bp.route('/')
def health_check():
    health_status = {
        'status' : 'UP'
    }