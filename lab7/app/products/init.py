from flask import Blueprint

bp = Blueprint("products", __name__, template_folder="templates")

from . import routes, models  # noqa: E402,F401

