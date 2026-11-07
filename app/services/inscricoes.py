from ..extensions import db
from ..models import Atividade, Inscricao, Participante
from .erros import RegraNegocioError


def vagas_livres(atividade):
    ativas = Inscricao.query.filter_by(
        id_atividade=atividade.id_atividade, status="ativa"
    ).count()
    return atividade.vagas - ativas


def inscrever(id_participante, id_atividade):
    """Inscreve um participante se houver vaga e não houver inscrição ativa."""
    atividade = db.session.execute(
        db.select(Atividade).filter_by(id_atividade=id_atividade).with_for_update()
    ).scalar_one_or_none()
    if atividade is None or atividade.status != "ativa":
        raise RegraNegocioError("Atividade indisponível para inscrição.")

    participante = db.session.get(Participante, id_participante)
    if participante is None or not participante.ativo:
        raise RegraNegocioError("Participante não encontrado ou inativo.")

    existente = Inscricao.query.filter_by(
        id_participante=id_participante, id_atividade=id_atividade
    ).first()
    if existente and existente.status == "ativa":
        raise RegraNegocioError("Participante já inscrito nesta atividade.")

    if vagas_livres(atividade) <= 0:
        raise RegraNegocioError("Não há vagas livres nesta atividade.")

    if existente:
        existente.status = "ativa"
        inscricao = existente
    else:
        inscricao = Inscricao(id_participante=id_participante, id_atividade=id_atividade)
        db.session.add(inscricao)
    db.session.commit()
    return inscricao
