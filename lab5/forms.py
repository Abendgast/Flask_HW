from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError

class ContactForm(FlaskForm):
    """Форма зворотного зв'язку"""
    name = StringField('Ім\'я', validators=[
        DataRequired(message='Поле обов\'язкове для заповнення'),
        Length(min=2, max=50, message='Ім\'я має бути від 2 до 50 символів')
    ])
    
    email = StringField('Email', validators=[
        DataRequired(message='Поле обов\'язкове для заповнення'),
        Email(message='Введіть коректну email адресу')
    ])
    
    subject = StringField('Тема', validators=[
        DataRequired(message='Поле обов\'язкове для заповнення'),
        Length(min=5, max=100, message='Тема має бути від 5 до 100 символів')
    ])
    
    message = TextAreaField('Повідомлення', validators=[
        DataRequired(message='Поле обов\'язкове для заповнення'),
        Length(min=10, max=500, message='Повідомлення має бути від 10 до 500 символів')
    ])
    
    submit = SubmitField('Відправити')


class LoginForm(FlaskForm):
    """Форма входу в систему"""
    username = StringField('Ім\'я користувача / Email', validators=[
        DataRequired(message='Поле обов\'язкове для заповнення')
    ])
    
    password = PasswordField('Пароль', validators=[
        DataRequired(message='Поле обов\'язкове для заповнення'),
        Length(min=4, max=10, message='Пароль має бути від 4 до 10 символів')
    ])
    
    remember = BooleanField('Запам\'ятати мене')
    
    submit = SubmitField('Увійти')
    
    def validate_username(self, field):
        """Кастомна валідація username"""
        if len(field.data) < 3:
            raise ValidationError('Ім\'я користувача має бути не менше 3 символів')
