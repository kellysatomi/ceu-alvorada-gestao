from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from ..extensions import db
from ..models import Usuario

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        usuario = db.session.execute(
            db.select(Usuario).filter_by(email=email)
        ).scalar_one_or_none()
        if usuario and usuario.ativo and usuario.check_senha(senha):
            login_user(usuario)
            return redirect(url_for("main.painel"))
        flash("E-mail ou senha inválidos.", "erro")  # mensagem genérica
    return render_template("login.html")


@bp.route("/sair")
@login_required
def sair():
    logout_user()
    return redirect(url_for("auth.login"))
