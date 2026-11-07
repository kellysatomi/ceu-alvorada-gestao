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


## Requisitos funcionais
- RF01 (obrigatório): autenticar a equipe por e-mail e senha antes de liberar as telas internas.
- RF02 (obrigatório): cadastrar atividades com número de vagas.
- RF03 (obrigatório): inscrever participantes e mostrar as vagas livres atualizadas.
- RF04 (obrigatório): reservar espaços e bloquear horários sobrepostos, informando o horário em conflito.
- RF05 (obrigatório): registrar presença apenas de inscritos ativos.
- RF06 (obrigatório): exibir painel com inscritos, vagas livres e frequência.
- RF07 (desejável): cancelar inscrição mantendo o histórico.


## Incrementos planejados
1. Login e controle de acesso (RF01)
2. Atividades e inscrições com controle de vagas (RF02 e RF03)
3. Agenda de espaços com bloqueio de conflito de horário (RF04)
4. Presença por turma e painel (RF05 e RF06)
5. Cancelamento de inscrição (RF07, desejável)

6. ## Regras de negócio
- Vagas livres = vagas da atividade menos as inscrições ativas.
- Inscrição recusada sem vaga, em atividade encerrada ou duplicada.
- Reserva recusada quando o horário se sobrepõe a outra no mesmo espaço e data.
- Presença só é registrada para inscrições ativas.
