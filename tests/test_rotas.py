from app.models import Usuario


def test_rota_interna_sem_login_redireciona(client):
    resp = client.get("/")
    assert resp.status_code == 302
    assert "/login" in resp.headers["Location"]


def test_login_valido_abre_painel(client, usuario):
    resp = client.post("/login", data={"email": "admin@teste.com", "senha": "senha-de-teste-123"})
    assert resp.status_code == 302
    assert client.get("/").status_code == 200


def test_login_invalido_e_recusado(client, usuario):
    resp = client.post("/login", data={"email": "admin@teste.com", "senha": "errada"})
    assert resp.status_code == 200
    assert "inválidos" in resp.get_data(as_text=True)


def test_senha_nao_e_guardada_em_texto_limpo(usuario):
    assert usuario.senha_hash != "senha-de-teste-123"
    assert usuario.senha_hash.startswith("scrypt:")


def test_reserva_conflitante_mostra_horario_em_choque(client, usuario, quadra, volei, futsal):
    client.post("/login", data={"email": "admin@teste.com", "senha": "senha-de-teste-123"})
    base = {"espaco": quadra.id_espaco, "data": "2026-11-03"}
    client.post("/reservar", data={**base, "atividade": volei.id_atividade, "inicio": "18:00", "fim": "19:00"})
    resp = client.post("/reservar", data={**base, "atividade": futsal.id_atividade, "inicio": "18:00", "fim": "19:30"})
    assert "Reserva não realizada" in resp.get_data(as_text=True)
