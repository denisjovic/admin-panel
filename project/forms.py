from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, Email, DataRequired


class RegisterForm(FlaskForm):
    email = StringField(label='Email', validators=[Length(min=5, max=30), Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=3), DataRequired()])
    submit = SubmitField()


class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField()


class ClientForm(FlaskForm):
    name = StringField(label='Company name', validators=[Length(min=2), DataRequired()])
    pib = StringField(label='Company pib/vat', validators=[Length(min=5), DataRequired()])
    contact = StringField(label='Contact', validators=[Length(min=5), DataRequired()])
    submit = SubmitField()

