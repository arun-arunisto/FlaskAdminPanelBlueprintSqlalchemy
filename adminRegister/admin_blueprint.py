from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import AdminRegistrationForm, AdminLoginForm
from databaseModel.models import db, AdminUser, ClientUser
from flask_login import login_user, current_user, login_required, logout_user

admin_bp = Blueprint("admin_bp", __name__,
                     template_folder="templates",
                     static_folder="static",
                     static_url_path="/adminRegister/static")


@admin_bp.route("/admin_panel")
@login_required
def admin_panel():
    client = db.session.execute(db.select(ClientUser)).scalars()
    return render_template("admin_panel.html", client=client)

@admin_bp.route("/admin_logout")
def admin_logout():
    logout_user()
    return redirect(url_for('admin_bp.admin_index'))

@admin_bp.route("/admin_index", methods=["GET", "POST"])
def admin_index():
    form = AdminLoginForm()
    if form.validate_on_submit():
        try:
            admin_user = AdminUser.query.filter_by(email=form.email.data).first()
            if admin_user is not None and admin_user.check_password(form.password.data):
                login_user(admin_user)
                return redirect(url_for("admin_bp.admin_panel"))
            flash("Invalid email or password", "error")
        except Exception as e:
            print(e)
            return redirect(url_for("admin_bp.admin_index"))
    return render_template("adminindex.html", form=form)

@admin_bp.route("/admin_register", methods=["GET", "POST"])
def admin_register():
    form = AdminRegistrationForm()
    if form.validate_on_submit():
        try:
            admin = AdminUser(username=form.username.data, email=form.email.data)
            admin.set_password(form.password.data)
            db.session.add(admin)
            db.session.commit()
            flash("Added Successfully!!", "success")
            return redirect(url_for('admin_bp.admin_index'))
        except Exception as e:
            print(e)
            flash("Something Went Wrong")
    return render_template("adminregister.html", form=form)
