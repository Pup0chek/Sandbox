from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Email, DataRequired

class MessageForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[Email()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField('Submit')
