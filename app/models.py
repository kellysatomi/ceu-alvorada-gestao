from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db, login_manager


class Usuario(UserMixin, db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    perfil = db.Column(db.String(20), nullable=False, default="responsavel")
    ativo = db.Column(db.Boolean, nullable=False, default=True)

    def get_id(self):
        return str(self.id_usuario)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha, method="scrypt")

    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    @property
    def is_active(self):
        return self.ativo


class Atividade(db.Model):
    id_atividade = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.Text)
    vagas = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="ativa")
    id_responsavel = db.Column(db.Integer, db.ForeignKey("usuario.id_usuario"))


class Participante(db.Model):
    id_participante = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    telefone = db.Column(db.String(30))
    nome_responsavel_legal = db.Column(db.String(120))
    ativo = db.Column(db.Boolean, nullable=False, default=True)


class Inscricao(db.Model):
    __table_args__ = (
        db.UniqueConstraint("id_participante", "id_atividade", name="uq_inscricao"),
    )
    id_inscricao = db.Column(db.Integer, primary_key=True)
    id_participante = db.Column(
        db.Integer, db.ForeignKey("participante.id_participante"), nullable=False
    )
    id_atividade = db.Column(
        db.Integer, db.ForeignKey("atividade.id_atividade"), nullable=False
    )
    data_inscricao = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    status = db.Column(db.String(20), nullable=False, default="ativa")


class Espaco(db.Model):
    id_espaco = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    capacidade = db.Column(db.Integer)
    ativo = db.Column(db.Boolean, nullable=False, default=True)


class Reserva(db.Model):
    id_reserva = db.Column(db.Integer, primary_key=True)
    id_espaco = db.Column(db.Integer, db.ForeignKey("espaco.id_espaco"), nullable=False)
    id_atividade = db.Column(
        db.Integer, db.ForeignKey("atividade.id_atividade"), nullable=False
    )
    data = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fim = db.Column(db.Time, nullable=False)
    id_criador = db.Column(db.Integer, db.ForeignKey("usuario.id_usuario"))


class Presenca(db.Model):
    __table_args__ = (
        db.UniqueConstraint("id_inscricao", "data_aula", name="uq_presenca"),
    )
    id_presenca = db.Column(db.Integer, primary_key=True)
    id_inscricao = db.Column(
        db.Integer, db.ForeignKey("inscricao.id_inscricao"), nullable=False
    )
    data_aula = db.Column(db.Date, nullable=False)
    presente = db.Column(db.Boolean, nullable=False)
    id_registrador = db.Column(db.Integer, db.ForeignKey("usuario.id_usuario"))


@login_manager.user_loader
def carregar_usuario(user_id):
    return db.session.get(Usuario, int(user_id))
