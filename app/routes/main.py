from datetime import date, time

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from ..extensions import db
from ..models import Atividade, Espaco, Inscricao
from ..services.erros import ConflitoHorarioError, RegraNegocioError
from ..services.inscricoes import vagas_livres
from ..services.reservas import reservar

bp = Blueprint("main", __name__)


@bp.route("/")
@login_required
def painel():
    atividades = Atividade.query.filter_by(status="ativa").all()
    linhas = [(a, vagas_livres(a)) for a in atividades]
    inscritos = Inscricao.query.filter_by(status="ativa").count()
    return render_template(
        "painel.html", linhas=linhas, inscritos=inscritos,
        vagas=sum(v for _, v in linhas),
    )


@bp.route("/reservar", methods=["GET", "POST"])
@login_required
def reservar_espaco():
    espacos = Espaco.query.filter_by(ativo=True).all()
    atividades = Atividade.query.filter_by(status="ativa").all()
    if request.method == "POST":
        try:
            data = date.fromisoformat(request.form["data"])
            ini = time.fromisoformat(request.form["inicio"])
            fim = time.fromisoformat(request.form["fim"])
            reservar(
                int(request.form["espaco"]), int(request.form["atividade"]),
                data, ini, fim, current_user.id_usuario,
            )
        except ConflitoHorarioError as erro:
            return render_template(
                "resultado.html", ok=False, mensagem=f"Reserva não realizada. {erro}"
            )
        except (RegraNegocioError, ValueError, KeyError) as erro:
            flash(str(erro) or "Confira os campos do formulário.", "erro")
            return render_template("reservar.html", espacos=espacos, atividades=atividades)
        return render_template("resultado.html", ok=True, mensagem="Reserva confirmada.")
    return render_template("reservar.html", espacos=espacos, atividades=atividades)
