from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, SubmitField, DateTimeField
from wtforms.validators import DataRequired

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    publication_date = DateTimeField('Publication Date', format='%m/%d/%Y')
    description = TextAreaField('Description')
    cover_image = StringField('Cover Image')
    submit = SubmitField()

    



    