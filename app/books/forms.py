from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, SubmitField, DateTimeField, FileField
from wtforms.validators import DataRequired, Optional

class BookForm(FlaskForm):
    title = StringField('Book Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    publication_date = DateTimeField('Publication Date', format='%m/%d/%Y', validators=[Optional()])
    description = TextAreaField('Description')
    cover_img = FileField('Cover Image')



    



    