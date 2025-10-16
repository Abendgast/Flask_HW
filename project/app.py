from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

@app.route('/')
@app.route('/resume')
def resume():
    """Головна сторінка з резюме"""
    page_title = "Моє Резюме"
    return render_template('resume.html', title=page_title)

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    """Сторінка контактів з формою"""
    page_title = "Контакти"
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        flash(f'Дякуємо, {name}! Ваше повідомлення отримано.', 'success')
        return redirect(url_for('contacts'))
    
    return render_template('contacts.html', title=page_title)

if __name__ == '__main__':
    app.run(debug=True)
