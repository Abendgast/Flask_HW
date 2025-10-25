from flask import Flask, render_template, request, redirect, url_for, session, flash
from forms import ContactForm, LoginForm
from loguru import logger
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production-2024'

# Налаштування логування
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logger.add(
    "logs/contact_form.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    rotation="1 MB",
    level="INFO"
)

# Заглушка для автентифікації
USERS = {
    'admin': 'password123',
    'user': 'qwerty',
    'test': 'test123'
}

# Зберігання даних форм для відображення
contact_submissions = []
login_attempts = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Обробка контактної форми з використанням WTF"""
    form = ContactForm()
    
    if form.validate_on_submit():
        # Отримання даних з форми
        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        message = form.message.data
        
        # Логування даних
        logger.info(f"Контактна форма - Ім'я: {name}, Email: {email}, Тема: {subject}")
        logger.info(f"Повідомлення: {message}")
        
        # Збереження даних для відображення
        submission = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        contact_submissions.append(submission)
        
        # Flash повідомлення про успіх
        flash(f'Дякуємо, {name}! Ваше повідомлення успішно відправлено на {email}', 'success')
        
        # Post/Redirect/Get pattern
        return redirect(url_for('contact'))
    
    # Якщо форма не валідна, виводимо помилки
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Помилка в полі {field}: {error}', 'error')
    
    return render_template('contact.html', form=form, submissions=contact_submissions)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Обробка форми входу з використанням WTF"""
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        
        # Збереження спроби входу для відображення
        login_attempt = {
            'username': username,
            'remember': remember,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        login_attempts.append(login_attempt)
        
        # Перевірка автентифікації
        if username in USERS and USERS[username] == password:
            session['username'] = username
            session['remember'] = remember
            
            # Flash повідомлення про успіх
            remember_msg = ' Вас буде запам\'ятано.' if remember else ''
            flash(f'Ласкаво просимо, {username}!{remember_msg}', 'success')
            
            # Post/Redirect/Get pattern
            return redirect(url_for('profile'))
        else:
            flash('Невірне ім\'я користувача або пароль', 'error')
            # Post/Redirect/Get pattern
            return redirect(url_for('login'))
    
    # Якщо форма не валідна, виводимо помилки
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Помилка в полі {getattr(form, field).label.text}: {error}', 'error')
    
    return render_template('login.html', form=form, login_attempts=login_attempts)


@app.route('/profile')
def profile():
    """Сторінка профілю користувача"""
    if 'username' not in session:
        flash('Будь ласка, увійдіть в систему', 'error')
        return redirect(url_for('login'))
    
    username = session.get('username')
    remember = session.get('remember', False)
    
    return render_template('profile.html', username=username, remember=remember)


@app.route('/logout')
def logout():
    """Вихід з системи"""
    session.pop('username', None)
    session.pop('remember', None)
    flash('Ви успішно вийшли з системи', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
