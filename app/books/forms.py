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

    def str_to_date(date_string):
        """Takes date in format mm/dd/yy and returns date object"""
        d = list(map(lambda x: int(x), date_string.split('/')))
        return date(d[2], d[0]. d[1])


    