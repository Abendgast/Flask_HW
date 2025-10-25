from flask import Flask

app = Flask(__name__)

from app.users import users_bp
app.register_blueprint(users_bp)

from app import views
