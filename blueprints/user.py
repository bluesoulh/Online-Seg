#注册相关

from flask import Blueprint, render_template,jsonify,redirect,url_for,session,flash
from exts import mail,db
from flask_mail import Message
from flask import request
import string
import random
from models import EmailCaptchaModel,UserModel
from .forms import RegisterForm,LoginForm
from werkzeug.security import generate_password_hash,check_password_hash

bp = Blueprint("user",__name__,url_prefix="/user",)


@bp.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                flash("邮箱不存在！")
                return redirect(url_for("user.login"))
            if check_password_hash(user.password, password):
                session['user_id'] = user.id
                return redirect("/")
            else:
                flash("密码错误!")
                return redirect(url_for("user.login"))
        else:
            flash(form.errors)
            return redirect(url_for("user.login"))

@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")



@bp.route("/register",methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email,username=username,password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user.login"))
        else:
            flash(form.errors)
            return redirect(url_for("user.register"))


@bp.route("/captcha/email")
def get_email_captcha():#默认是get请求
    email = request.args.get("email")
    source = string.digits*6
    captcha = random.sample(source,6)
    captcha = "".join(captcha)
    message = Message(subject="海上船舶在线语义分割平台注册验证码", recipients=[email], body=f"您正在注册海上船舶在线语义分割平台账号，如果这是您在操作，请在注册页面输入验证码。您的验证码是:{captcha}")
    mail.send(message)
    #用数据库表存储
    email_captcha = EmailCaptchaModel(email=email,captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    return jsonify({"code":200,"message":"","data":None})

