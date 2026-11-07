from ..extensions import db
from ..models import Atividade, Espaco, Reserva
from .erros import ConflitoHorarioError, RegraNegocioError


def _fmt(hora):
    return f"{hora.hour}h" if hora.minute == 0 else f"{hora.hour}h{hora.minute:02d}"


def reservar(id_espaco, id_atividade, data, hora_inicio, hora_fim, id_criador=None):
    """Cria a reserva, recusando horários sobrepostos no mesmo espaço e data."""
    if hora_fim <= hora_inicio:
        raise RegraNegocioError("Horário final deve ser depois do inicial.")

    # O bloqueio da linha do espaço serializa pedidos simultâneos (PostgreSQL).
    espaco = db.session.execute(
        db.select(Espaco).filter_by(id_espaco=id_espaco).with_for_update()
    ).scalar_one_or_none()
    if espaco is None or not espaco.ativo:
        raise RegraNegocioError("Espaço indisponível para reserva.")

    atividade = db.session.get(Atividade, id_atividade)
    if atividade is None or atividade.status != "ativa":
        raise RegraNegocioError("Atividade indisponível para reserva.")

    conflito = Reserva.query.filter(
        Reserva.id_espaco == id_espaco,
        Reserva.data == data,
        Reserva.hora_inicio < hora_fim,
        Reserva.hora_fim > hora_inicio,
    ).first()
    if conflito:
        outra = db.session.get(Atividade, conflito.id_atividade)
        raise ConflitoHorarioError(
            f"{espaco.nome} ocupado de {_fmt(conflito.hora_inicio)} "
            f"às {_fmt(conflito.hora_fim)} por {outra.nome}."
        )

    reserva = Reserva(
        id_espaco=id_espaco,
        id_atividade=id_atividade,
        data=data,
        hora_inicio=hora_inicio,
        hora_fim=hora_fim,
        id_criador=id_criador,
    )
    db.session.add(reserva)
    db.session.commit()
    return reserva
