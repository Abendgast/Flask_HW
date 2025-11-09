from flask import Flask
from .extensions import db, migrate
from .products import bp as products_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(products_bp, url_prefix="/products")
    return app

