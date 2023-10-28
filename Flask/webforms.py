from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo
from wtforms.widgets import TextArea


class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("submit")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("submit")


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    author = StringField("Author")
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit", validators=[DataRequired()])


class NameForm(FlaskForm):
    name = StringField("your NAME", validators=[DataRequired()])
    submit = SubmitField("submit")


class UserForm(FlaskForm):
    name = StringField("NAME", validators=[DataRequired()])
    username = StringField("UserNAME", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favori_color = StringField("favori color")
    password_hash = PasswordField('Password',
                                  validators=[DataRequired(), EqualTo('password_hash2', message='password must match')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField("submit")


class PasswordForm(FlaskForm):
    email = StringField("your email", validators=[DataRequired()])
    password_hash = PasswordField("your password?", validators=[DataRequired()])
    submit = SubmitField("submit")
