from flask import Blueprint

bp = Blueprint('users', __name__)

from app.users import routes

from app.users import bp as users_bp
app.register_blueprint(users_bp, url_prefix='/users')

from app.posts import bp as posts_bp
app.register_blueprint(posts_bp, url_prefix='/posts')

