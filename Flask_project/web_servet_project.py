import os
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename

c = []
b = []
dinamic_user = ''
flag_user = False
fulname_user = ''
app = Flask(__name__)
UPLOAD_FOLDER = 'static/photo'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
a = False


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class RegForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired()])
    surname = StringField('Ваша фамилия', validators=[DataRequired()])
    login = StringField('Введите email или номер телефона', validators=[DataRequired()])
    adres = StringField('adres', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Регистрация')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    surname = db.Column(db.String(80), unique=False, nullable=False)
    login = db.Column(db.String(120), unique=True, nullable=False)
    adres = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<User {} {} {} {} {}>'.format(
            self.name, self.surname, self.login, self.adres, self.password)


class Recept(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_recept = db.Column(db.String(80), unique=False, nullable=False)
    recept = db.Column(db.String(80), unique=False, nullable=False)
    logo = db.Column(db.String(80), unique=False, nullable=False)
    user_id = db.Column(db.Integer)

    def __repr__(self):
        return '<User {} {} {} {}>'.format(
            self.name_recept, self.recept, self.user_id, self.logo)


class AddReceptForm(FlaskForm):
    title = StringField('Заголовок новости', validators=[DataRequired()])
    content = TextAreaField('Текст новости', validators=[DataRequired()])
    # file = FileField("Загрузить изображение файла")
    submit = SubmitField('Добавить')


db.create_all()


@app.route('/Log_out')
def Log_out():
    global flag_user, dinamic_user, c
    flag_user = False
    dinamic_user = ''
    c = []
    print(Recept.query.all())
    return redirect("/")


@app.route('/')
def form_sample():
    # recept = Recept(name_recept="brule",
    #               recept="gotov",
    #               user_id=1)
    # db.session.add(recept)
    # db.session.commit()

    return render_template('standart.html', flag_user=flag_user, fulname_user=fulname_user)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/Add_recept', methods=['GET', 'POST'])
def Add_recept():
    form = AddReceptForm()
    if form.validate_on_submit():
        # files = request.files.getlist('add_recept.html')
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], dinamic_user + "_" + form.title.data + "_" + filename))
        recept = Recept(name_recept=form.title.data,
                        recept=form.content.data,
                        user_id=(User.query.filter(User.login == dinamic_user).first()).id,
                        logo=dinamic_user + "_" + form.title.data + "_" + filename)
        db.session.add(recept)
        db.session.commit()
        return redirect("/")
    return render_template('add_recept.html', title='Новая новость', form=form)


@app.route('/Log_Form', methods=['GET', 'POST'])
def Log_Form():
    global c, flag_user, dinamic_user
    form = LoginForm()
    if form.validate_on_submit():
        # print(type(form.username.data))
        password = User.query.filter(User.login == form.username.data).first()
        if password is not None:
            if password.password == form.password.data:
                flag_user = True
                dinamic_user = form.username.data
                c = Recept.query.filter(
                    Recept.user_id == (User.query.filter(User.login == form.username.data).first()).id).all()
                return redirect("/user/" + password.name + "_" + password.surname)
        else:
            pass
            ##return redirect('/log')
    else:
        pass
    return render_template('Log_form.html', title='Авторизация', form=form)


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    form = RegForm()
    user = User(name=form.name.data,
                surname=form.surname.data,
                login=form.login.data,
                adres=form.adres.data,
                password=form.password.data)
    if form.validate_on_submit():
        if User.query.filter(User.login == form.login.data).first() is None:
            db.session.add(user)
            db.session.commit()
            return redirect("/")
    # else:
    #  pass
    return render_template('regform.html', title='Авторизация', form=form)


@app.route('/user/<fulname>', methods=['GET', 'POST'])
def user(fulname):
    global c, b, fulname_user
    b = []
    for x in c:
        b.append(x.name_recept)
        b.append(x.logo)
    fulname_user = 'http://127.0.0.1:8080/user/' + fulname
    return render_template('user.html', title=fulname, list=b, fulname_user=fulname_user,
                           flag_user=flag_user)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
