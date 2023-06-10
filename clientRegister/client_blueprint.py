from flask import Blueprint, render_template, flash, request, url_for, redirect
from .forms import ClientRegister, ClientLogin
from databaseModel.models import db, ClientUser
from flask_login import login_user, current_user, login_required, logout_user


client_bp = Blueprint("client_bp", __name__,
                      template_folder="templates",
                      static_folder="static",
                      static_url_path="/clientRegister/static")


@client_bp.route("/home")
@login_required
def home():
    return render_template("client_home.html")

@client_bp.route("/client_logout")
@login_required
def client_logout():
    logout_user()
    return redirect(url_for("client_bp.client_login"))

@client_bp.route("/")
def index():
    return render_template("index.html")

@client_bp.route("/client_register", methods=["GET", "POST"])
def client_register():
    form = ClientRegister()
    if form.validate_on_submit():
        try:
            client = ClientUser(username=form.username.data, email=form.email.data)
            client.set_password(form.password.data)
            db.session.add(client)
            db.session.commit()
            flash("Created Successfully!", "success")
            return redirect(url_for('client_bp.client_login'))
        except Exception as e:
            print(e)
            return redirect(url_for("client_bp.client_register"))
    return render_template("client_register.html", form=form)

@client_bp.route("/client_login", methods=["GET", "POST"])
def client_login():
    form = ClientLogin()
    if form.validate_on_submit():
        try:
            client = ClientUser.query.filter_by(email=form.email.data).first()
            if client is not None and client.check_password(form.password.data):
                login_user(client)
                return redirect(url_for("client_bp.home"))
            flash("Invalid email or password")
        except Exception as e:
            print(e)
            return redirect(url_for("client_bp.client_login"))
    return render_template("client_login.html", form=form)