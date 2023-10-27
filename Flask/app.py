from flask import request
from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
import psycopg2

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/users'
app.config['SECRET_KEY'] = "my super secret"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favori_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.name


class UserForm(FlaskForm):
    name = StringField("NAME", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favori_color = StringField("favori color")
    submit = SubmitField("submit")


@app.route('/delete/<int:id>')
def delete(id, ):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()
    name_to_update = None
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("deleted succesfully")
        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html",
                               form=form,
                               name=name,
                               our_users=our_users,
                               name_to_update=name_to_update)
    except:
        flash("a problem ")
        return render_template("add_user.html",
                               form=form,
                               name=name,
                               our_users=our_users,
                               name_to_update=name_to_update)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favori_color = request.form['favori_color']
        try:
            db.session.commit()
            flash("user updated")
            return render_template("update.html",
                                   form=form,
                                   name_to_update=name_to_update)
        except:
            flash("looks like error")
            return render_template("update.html",
                                   form=form,
                                   name_to_update=name_to_update)
    else:
        return render_template("update.html",
                               form=form,
                               name_to_update=name_to_update,
                               id=id
                               )


class NameForm(FlaskForm):
    name = StringField("your NAME", validators=[DataRequired()])
    submit = SubmitField("submit")


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    name_to_update = None
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data, favori_color=form.favori_color.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favori_color.data = ''
        flash("User added")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html",
                           form=form,
                           name=name,
                           our_users=our_users,
                           name_to_update=name_to_update)


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


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
