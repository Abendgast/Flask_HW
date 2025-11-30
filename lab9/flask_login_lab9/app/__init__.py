import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    # директорія для збереження аватарів
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'profile_pics')
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB limit (опціонально)

    # переконаємось, що папка існує
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    # before_request: оновлює last_seen
    from flask_login import current_user
    from datetime import datetime

    @app.before_request
    def update_last_seen():
        if current_user.is_authenticated:
            current_user.last_seen = datetime.utcnow()
            db.session.commit()

    return app

