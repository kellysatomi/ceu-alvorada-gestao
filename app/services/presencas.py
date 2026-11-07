from ..extensions import db
from ..models import Inscricao, Presenca
from .erros import RegraNegocioError


def registrar_presenca(id_inscricao, data_aula, presente, id_registrador=None):
    """Registra (ou corrige) a presença; só vale para inscrição ativa."""
    inscricao = db.session.get(Inscricao, id_inscricao)
    if inscricao is None or inscricao.status != "ativa":
        raise RegraNegocioError("Só é possível registrar presença de inscritos ativos.")

    registro = Presenca.query.filter_by(
        id_inscricao=id_inscricao, data_aula=data_aula
    ).first()
    if registro:
        registro.presente = presente
        registro.id_registrador = id_registrador
    else:
        registro = Presenca(
            id_inscricao=id_inscricao,
            data_aula=data_aula,
            presente=presente,
            id_registrador=id_registrador,
        )
        db.session.add(registro)
    db.session.commit()
    return registro
