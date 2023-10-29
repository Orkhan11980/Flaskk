from datetime import datetime
from flask import Flask, render_template, flash, jsonify
from flask import request, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.urls import url_decode
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from wtforms.widgets import TextArea
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from webforms import LoginForm, SearchForm, UserForm, PostForm, PasswordForm, NameForm
from database import Users, Posts, db
from flask_ckeditor import CKEditor

app = Flask(__name__)
ckeditor = CKEditor(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/users'
app.config['SECRET_KEY'] = "my super secret"
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("login succesfull ")
                return redirect(url_for('dashboard'))
            else:
                flash("wrong password")
        else:
            flash("that user doesnt exist")
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("you are logged out")
    return redirect(url_for('login'))


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    name_to_update = Users.query.get_or_404(id)

    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favori_color = request.form['favori_color']
        name_to_update.username = request.form['username']
        name_to_update.about_author = request.form['about_author']

        try:
            db.session.commit()
            flash("user updated")
            return render_template("dashboard.html",
                                   form=form,
                                   name_to_update=name_to_update, id=id)
        except:
            flash("looks like error")
            return render_template("dashboard.html",
                                   form=form,
                                   name_to_update=name_to_update, id=id)
    else:
        form.name.data = name_to_update.name
        form.email.data = name_to_update.email
        form.favori_color.data = name_to_update.favori_color
        form.username.data = name_to_update.username
        form.about_author.data = name_to_update.about_author

        return render_template("dashboard.html",
                               form=form,
                               name_to_update=name_to_update,
                               id=id
                               )


@app.route('/posts')
def posts():
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts=posts)


@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post=post)


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        # post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data

        db.session.add(post)
        db.session.commit()
        flash("post has been updated")
        return redirect(url_for('post', id=post.id))

    if current_user.id == post.poster_id:
        form.title.data = post.title
        # form.author.data = post.author
        form.slug.data = post.slug
        form.content.data = post.content
        return render_template('edit_post.html', form=form)
    else:
        flash("You are not Allowed to  edit this post")
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)


@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


@app.route('/search', methods=["POST"])
def search():
    form = SearchForm()
    posts = Posts.query
    if form.validate_on_submit():
        post.searched = form.searched.data
        posts = posts.filter(Posts.content.like('%' + post.searched + '%'))
        posts = posts.order_by(Posts.title).all()

    return render_template("search.html", form=form, searched=post.searched, posts=posts)


@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    id = current_user.id
    if id == post_to_delete.poster.id:
        try:
            db.session.delete(post_to_delete)
            db.session.commit()

            flash("Blog removed")

            posts = Posts.query.order_by(Posts.date_posted)
            return render_template('posts.html', posts=posts)

        except:
            flash("There is a problem")
            posts = Posts.query.order_by(Posts.date_posted)
            return render_template('posts.html', posts=posts)
    else:
        flash("you can not delete this post")

        posts = Posts.query.order_by(Posts.date_posted)
        return render_template('posts.html', posts=posts)


@app.route('/add-post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        poster = current_user.id
        post = Posts(title=form.title.data, content=form.content.data,
                     poster_id=poster, slug=form.slug.data)
        form.title.data = ''
        form.content.data = ''
        # form.author.data = ''
        form.slug.data = ''

        db.session.add(post)
        db.session.commit()

        flash("blog submitted")

    return render_template("add_post.html", form=form)


@app.route('/date')
def get_current_date():
    fav_pizza = {
        "jon": "pape",
        "mary": "cheese"
    }
    return jsonify(fav_pizza)

    #  return jsonify(date.today())

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Name %r>' % self.name


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
@login_required
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favori_color = request.form['favori_color']
        name_to_update.username = request.form['username']
        name_to_update.about_author = request.form['about_author']
        try:
            db.session.commit()
            flash("user updated")
            return render_template("update.html",
                                   form=form,
                                   name_to_update=name_to_update,
                                   id=id)
        except:
            flash("looks like errorrr")
            return render_template("update.html",
                                   form=form,
                                   name_to_update=name_to_update,
                                   id=id

                                   )
    else:
        form.name.data = name_to_update.name
        form.email.data = name_to_update.email
        form.favori_color.data = name_to_update.favori_color
        form.username.data = name_to_update.username
        form.about_author.data = name_to_update.about_author

        return render_template("update.html",
                               form=form,
                               name_to_update=name_to_update,
                               id=id
                               )


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    name_to_update = None
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            hashed_pw = generate_password_hash(form.password_hash.data)
            user = Users(username=form.username.data, name=form.name.data, email=form.email.data,
                         favori_color=form.favori_color.data,
                         password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.favori_color.data = ''
        form.password_hash.data = ''
        flash("User added")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html",
                           form=form,
                           name=name,
                           our_users=our_users,
                           name_to_update=name_to_update)


@app.route('/admin')
@login_required
def admin():
    id = current_user.id
    if id == 20:
        return render_template("admin.html")
    else:
        flash("You must be admin")
        return redirect(url_for('dashboard'))


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


@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        form.email.data = ''
        form.password_hash.data = ''
        pw_to_check = Users.query.filter_by(email=email).first()

        passed = check_password_hash(pw_to_check.password_hash, password)
    return render_template("test_pw.html",
                           email=email,
                           password=password,
                           pw_to_check=pw_to_check,
                           passed=passed,
                           form=form)


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
