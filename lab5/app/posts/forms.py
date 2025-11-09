from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
# DateTimeLocalField availability may vary; try import, otherwise use StringField as fallback
try:
    from wtforms.fields import DateTimeLocalField
except Exception:
    DateTimeLocalField = None

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=150)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=10, max=5000)])
    enabled = BooleanField('Enabled', default=True)
    if DateTimeLocalField:
        publish_date = DateTimeLocalField('Publish date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    else:
        publish_date = StringField('Publish date (YYYY-MM-DD HH:MM)', validators=[DataRequired()])
    category = SelectField('Category', choices=[('news','news'),('publication','publication'),('tech','tech'),('other','other')], default='other')
    submit = SubmitField('Save')

