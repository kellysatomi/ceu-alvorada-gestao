# Gestão de Atividades e Espaços do CEU Alvorada

MVP web responsivo para a equipe do CEU Alvorada (Centro Educacional Unificado) organizar inscrições, presença e agenda de espaços, hoje feitas em papel, planilhas e WhatsApp.

## Problema
Informações espalhadas causam retrabalho, vagas desatualizadas e conflitos de horário na reserva de salas, quadra e auditório.

## Funcionalidades do MVP
- Login da equipe (senha com hash scrypt)
- Atividades com controle de vagas e inscrição sem duplicidade
- Agenda de espaços com bloqueio de conflito de horário
- Registro de presença por turma (apenas inscritos ativos)
- Painel com inscritos e vagas livres

## Arquitetura
Monólito em camadas: rotas (`app/routes`), regras de negócio (`app/services`) e dados (`app/models.py`). As regras de vaga, conflito e presença ficam em `app/services` e são testadas sem navegador.

## Tecnologias
Python 3.12, Flask, Flask-SQLAlchemy (SQLAlchemy), Flask-Login, Flask-WTF (CSRF), PostgreSQL (produção) e SQLite (desenvolvimento e testes), Bootstrap 5, pytest.

## Como executar
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export SECRET_KEY="troque-esta-chave"
flask --app app criar-admin seu@email.com
flask --app app run
```
Em produção, defina também `DATABASE_URL` (PostgreSQL). Segredos ficam em variáveis de ambiente, nunca no repositório.

## Como rodar os testes
```bash
pytest --cov=app --cov-report=term-missing
```

## Contexto
Projeto da disciplina Projeto de Software (ODS 4: Educação de Qualidade).
Autora: Kelly Satomi Habara Cruz
