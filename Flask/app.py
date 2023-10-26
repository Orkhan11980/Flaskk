from flask import Flask, render_template,flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config['SECRET_KEY'] = "my super secret"


class NameForm(FlaskForm):
    name = StringField("YOUR NAME", validators=[DataRequired()])
    submit = SubmitField("submit")


@app.route('/')
def index():
    firstname = "Orki"
    fav_pizza = ["che", 41, "pepo"]
    stuff = "this <strong>bold</strong> is bold"
    return render_template("index.html",
                           firstname=firstname,
                           stuff=stuff,
                           fav_pizza=fav_pizza)


@app.route('/user/<name>')
def user(name):
    return render_template("user.html", name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("succesfuly submit")
    return render_template("name.html",
                           name=name,
                           form=form)
