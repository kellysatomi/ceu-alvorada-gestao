from datetime import date

import pytest

from app.models import Presenca
from app.services.erros import RegraNegocioError
from app.services.inscricoes import inscrever
from app.services.presencas import registrar_presenca


def test_presenca_de_inscrito_e_registrada(volei, participantes):
    insc = inscrever(participantes[0].id_participante, volei.id_atividade)
    registrar_presenca(insc.id_inscricao, date(2026, 11, 3), True)
    assert Presenca.query.count() == 1


def test_presenca_repetida_atualiza_sem_duplicar(volei, participantes):
    insc = inscrever(participantes[0].id_participante, volei.id_atividade)
    registrar_presenca(insc.id_inscricao, date(2026, 11, 3), True)
    registrar_presenca(insc.id_inscricao, date(2026, 11, 3), False)
    assert Presenca.query.count() == 1
    assert Presenca.query.first().presente is False


def test_presenca_de_nao_inscrito_e_recusada(app):
    with pytest.raises(RegraNegocioError):
        registrar_presenca(999, date(2026, 11, 3), True)
