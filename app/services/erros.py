class RegraNegocioError(Exception):
    """Violação de uma regra de negócio, com mensagem própria para o usuário."""


class ConflitoHorarioError(RegraNegocioError):
    """Reserva sobreposta a outra no mesmo espaço e data."""
