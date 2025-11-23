from app.users import bp as users_bp
app.register_blueprint(users_bp, url_prefix='/users')

