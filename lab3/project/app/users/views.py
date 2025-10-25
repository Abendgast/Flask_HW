from app.users import users_bp
from flask import render_template, redirect, url_for, request

@users_bp.route('/hi/<name>')
def greetings(name):
    age = request.args.get('age', 'невідомий')
    return render_template('users/hi.html', name=name.upper(), age=age)

@users_bp.route('/admin')
def admin():
    return redirect(url_for('users.greetings', name='Administrator', age=45))
