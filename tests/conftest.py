from datetime import date

import pytest

from app import create_app
from app.extensions import db
from app.models import Atividade, Espaco, Participante, Usuario
from config import TestConfig


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def usuario(app):
    u = Usuario(nome="Admin Demonstração", email="admin@teste.com", perfil="administrativo")
    u.set_senha("senha-de-teste-123")
    db.session.add(u)
    db.session.commit()
    return u


@pytest.fixture
def futsal(app):
    a = Atividade(nome="Futsal Iniciante", vagas=1)
    db.session.add(a)
    db.session.commit()
    return a


@pytest.fixture
def volei(app):
    a = Atividade(nome="Vôlei Adulto", vagas=10)
    db.session.add(a)
    db.session.commit()
    return a


@pytest.fixture
def quadra(app):
    e = Espaco(nome="Quadra Poliesportiva", tipo="quadra")
    db.session.add(e)
    db.session.commit()
    return e


@pytest.fixture
def participantes(app):
    lista = [Participante(nome=f"Participante {i}", data_nascimento=date(1990, 1, 1)) for i in (1, 2)]
    db.session.add_all(lista)
    db.session.commit()
    return lista
