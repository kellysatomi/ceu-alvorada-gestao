from datetime import date, time

import pytest

from app.services.erros import ConflitoHorarioError, RegraNegocioError
from app.services.reservas import reservar

DIA = date(2026, 11, 3)


def test_reserva_em_horario_livre(quadra, volei):
    r = reservar(quadra.id_espaco, volei.id_atividade, DIA, time(18), time(19))
    assert r.id_reserva is not None


def test_reserva_sobreposta_e_recusada_com_horario_em_conflito(quadra, volei, futsal):
    reservar(quadra.id_espaco, volei.id_atividade, DIA, time(18), time(19))
    with pytest.raises(ConflitoHorarioError, match="18h às 19h por Vôlei Adulto"):
        reservar(quadra.id_espaco, futsal.id_atividade, DIA, time(18), time(19, 30))


def test_horarios_adjacentes_sao_aceitos(quadra, volei, futsal):
    reservar(quadra.id_espaco, volei.id_atividade, DIA, time(18), time(19))
    r = reservar(quadra.id_espaco, futsal.id_atividade, DIA, time(19), time(20, 30))
    assert r.id_reserva is not None


def test_hora_final_deve_ser_depois_da_inicial(quadra, volei):
    with pytest.raises(RegraNegocioError, match="depois do inicial"):
        reservar(quadra.id_espaco, volei.id_atividade, DIA, time(19), time(18))
