import os


class Config:
    # Em produção, SECRET_KEY e DATABASE_URL vêm de variáveis de ambiente.
    SECRET_KEY = os.environ.get("SECRET_KEY", "somente-desenvolvimento")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///dev.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    TESTING = True
    SECRET_KEY = "teste"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
