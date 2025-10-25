from app.products import products_bp
from flask import render_template

@products_bp.route('/')
def index():
    return render_template('products/index.html')

