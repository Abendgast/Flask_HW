from app.products import bp


@bp.route('/')
def index():
    return 'Products Blueprint'
