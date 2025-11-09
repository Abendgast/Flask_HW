import os
from flask import Flask, render_template
from .config import DevelopmentConfig, TestingConfig, ProductionConfig
from .extensions import db, migrate

config_map = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

def create_app(config_name: str | None = None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_map.get(config_name, DevelopmentConfig))

    # ensure instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from .posts import post_bp
    app.register_blueprint(post_bp)

    # error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app

