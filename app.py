from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from flask_migrate import Migrate

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from config import Config

from forms import (
    RegistrationForm,
    LoginForm,
    PostForm
)


app = Flask(__name__)
app.config.from_object(Config)

from extensions import db

db.init_app(app)

migrate = Migrate(app, db)


login_manager = LoginManager(app)
login_manager.login_view = "login"


from models.models import User, Post


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))




@app.route("/")
def index():

    page = request.args.get(
        "page",
        1,
        type=int
    )

    posts = db.paginate(
        db.select(Post)
        .order_by(Post.created_at.desc()),
        page=page,
        per_page=5
    )

    return render_template(
        "index.html",
        posts=posts
    )




@app.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()

    if form.validate_on_submit():

        existing_user = User.query.filter(
            (User.username == form.username.data) |
            (User.email == form.email.data)
        ).first()

        if existing_user:

            flash(
                "Такой пользователь уже существует."
            )

            return redirect(
                url_for("register")
            )

        user = User(
            username=form.username.data,
            email=form.email.data
        )

        user.set_password(
            form.password.data
        )

        db.session.add(user)
        db.session.commit()

        flash(
            "Регистрация прошла успешно!"
        )

        return redirect(
            url_for("login")
        )

    return render_template(
        "register.html",
        form=form
    )




@app.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            username=form.username.data
        ).first()

        if user and user.check_password(
            form.password.data
        ):

            login_user(user)

            flash(
                "Вы успешно вошли!"
            )

            return redirect(
                url_for("index")
            )

        flash(
            "Неверное имя пользователя или пароль."
        )

    return render_template(
        "login.html",
        form=form
    )



@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Вы вышли из аккаунта."
    )

    return redirect(
        url_for("index")
    )




@app.route(
    "/post/create",
    methods=["GET", "POST"]
)
@login_required
def create_post():

    form = PostForm()

    if form.validate_on_submit():

        post = Post(
            title=form.title.data,
            text=form.text.data,
            author=current_user
        )

        db.session.add(post)
        db.session.commit()

        flash(
            "Пост создан!"
        )

        return redirect(
            url_for("index")
        )

    return render_template(
        "create_post.html",
        form=form
    )




@app.route("/post/<int:post_id>")
def post(post_id):

    post = db.get_or_404(
        Post,
        post_id
    )

    return render_template(
        "post.html",
        post=post
    )




@app.route(
    "/post/<int:post_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def edit_post(post_id):

    post = db.get_or_404(
        Post,
        post_id
    )

    if post.user_id != current_user.id:

        flash(
            "Вы не можете редактировать этот пост."
        )

        return redirect(
            url_for(
                "post",
                post_id=post.id
            )
        )

    form = PostForm()

    if form.validate_on_submit():

        post.title = form.title.data
        post.text = form.text.data

        db.session.commit()

        flash(
            "Пост изменён!"
        )

        return redirect(
            url_for(
                "post",
                post_id=post.id
            )
        )

    if request.method == "GET":

        form.title.data = post.title
        form.text.data = post.text

    return render_template(
        "edit_post.html",
        form=form,
        post=post
    )



@app.route(
    "/post/<int:post_id>/delete"
)
@login_required
def delete_post(post_id):

    post = db.get_or_404(
        Post,
        post_id
    )

    if post.user_id != current_user.id:

        flash(
            "Вы не можете удалить этот пост."
        )

        return redirect(
            url_for(
                "post",
                post_id=post.id
            )
        )

    db.session.delete(post)
    db.session.commit()

    flash(
        "Пост удалён."
    )

    return redirect(
        url_for("index")
    )



if __name__ == "__main__":
    app.run(debug=True)