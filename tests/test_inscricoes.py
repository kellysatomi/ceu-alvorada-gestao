import pytest

from app.models import Inscricao
from app.services.erros import RegraNegocioError
from app.services.inscricoes import inscrever, vagas_livres


def test_inscricao_reduz_vagas_livres(futsal, participantes):
    inscrever(participantes[0].id_participante, futsal.id_atividade)
    assert vagas_livres(futsal) == 0


def test_inscricao_recusada_sem_vaga(futsal, participantes):
    inscrever(participantes[0].id_participante, futsal.id_atividade)
    with pytest.raises(RegraNegocioError, match="vagas"):
        inscrever(participantes[1].id_participante, futsal.id_atividade)


def test_inscricao_duplicada_recusada(volei, participantes):
    inscrever(participantes[0].id_participante, volei.id_atividade)
    with pytest.raises(RegraNegocioError, match="já inscrito"):
        inscrever(participantes[0].id_participante, volei.id_atividade)
    assert Inscricao.query.count() == 1
