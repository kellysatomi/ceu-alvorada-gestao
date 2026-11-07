import click
from flask import Flask

from config import Config
from .extensions import csrf, db, login_manager


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    from .routes.auth import bp as auth_bp
    from .routes.main import bp as main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    @app.cli.command("criar-admin")
    @click.argument("email")
    @click.password_option()
    def criar_admin(email, password):
        """Cria um usuário administrativo."""
        from .models import Usuario

        db.create_all()
        u = Usuario(nome="Administrador", email=email, perfil="administrativo")
        u.set_senha(password)
        db.session.add(u)
        db.session.commit()
        click.echo("Usuário criado.")

    return app
