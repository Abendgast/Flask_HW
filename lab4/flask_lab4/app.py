from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

# Заглушка для автентифікації
USERS = {
    'admin': 'password123',
    'user': 'qwerty',
    'test': 'test123'
}

# Декоратор для перевірки автентифікації
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Будь ласка, увійдіть в систему', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Перевірка автентифікації
        if username in USERS and USERS[username] == password:
            session['username'] = username
            flash(f'Ласкаво просимо, {username}!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Невірне ім\'я користувача або пароль', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/profile')
@login_required
def profile():
    username = session.get('username')
    # Отримання всіх кукі
    cookies = {key: value for key, value in request.cookies.items()}
    
    # Отримання вибраної теми
    theme = request.cookies.get('theme', 'light')
    
    return render_template('profile.html', username=username, cookies=cookies, theme=theme)

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Ви успішно вийшли з системи', 'info')
    return redirect(url_for('login'))

@app.route('/add_cookie', methods=['POST'])
@login_required
def add_cookie():
    cookie_key = request.form.get('cookie_key')
    cookie_value = request.form.get('cookie_value')
    cookie_days = request.form.get('cookie_days', type=int, default=7)
    
    if cookie_key and cookie_value:
        response = make_response(redirect(url_for('profile')))
        expires = datetime.now() + timedelta(days=cookie_days)
        response.set_cookie(cookie_key, cookie_value, expires=expires)
        flash(f'Кукі "{cookie_key}" успішно додано', 'success')
        return response
    else:
        flash('Будь ласка, заповніть всі поля', 'error')
        return redirect(url_for('profile'))

@app.route('/delete_cookie', methods=['POST'])
@login_required
def delete_cookie():
    cookie_key = request.form.get('cookie_key')
    
    if cookie_key:
        response = make_response(redirect(url_for('profile')))
        response.set_cookie(cookie_key, '', expires=0)
        flash(f'Кукі "{cookie_key}" успішно видалено', 'success')
        return response
    else:
        flash('Вкажіть ключ кукі для видалення', 'error')
        return redirect(url_for('profile'))

@app.route('/delete_all_cookies', methods=['POST'])
@login_required
def delete_all_cookies():
    response = make_response(redirect(url_for('profile')))
    
    # Видалення всіх кукі (крім системних)
    for key in request.cookies.keys():
        if key not in ['session', 'theme']:
            response.set_cookie(key, '', expires=0)
    
    flash('Всі кукі успішно видалено', 'success')
    return response

@app.route('/set_theme/<theme>')
@login_required
def set_theme(theme):
    if theme in ['light', 'dark']:
        response = make_response(redirect(url_for('profile')))
        response.set_cookie('theme', theme, max_age=60*60*24*365)  # 1 рік
        flash(f'Тему змінено на {"світлу" if theme == "light" else "темну"}', 'success')
        return response
    else:
        flash('Невірна тема', 'error')
        return redirect(url_for('profile'))

if __name__ == '__main__':
    app.run(debug=True)
