from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    PasswordField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo
)


class RegistrationForm(FlaskForm):

    username = StringField(
        "Имя пользователя",
        validators=[
            DataRequired(),
            Length(min=3, max=80)
        ]
    )

    email = StringField(
        "E-mail",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Пароль",
        validators=[
            DataRequired(),
            Length(min=8)
        ]
    )

    password2 = PasswordField(
        "Повторите пароль",
        validators=[
            DataRequired(),
            EqualTo("password")
        ]
    )

    submit = SubmitField("Зарегистрироваться")


class LoginForm(FlaskForm):

    username = StringField(
        "Имя пользователя",
        validators=[DataRequired()]
    )

    password = PasswordField(
        "Пароль",
        validators=[DataRequired()]
    )

    submit = SubmitField("Войти")



class PostForm(FlaskForm):

    title = StringField(
        "Заголовок",
        validators=[
            DataRequired(),
            Length(min=3, max=200)
        ]
    )

    text = StringField(
        "Текст",
        validators=[
            DataRequired(),
            Length(min=10)
        ]
    )

    submit = SubmitField("Сохранить")