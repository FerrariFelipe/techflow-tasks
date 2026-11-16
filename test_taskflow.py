import sqlite3
import taskflow_app as app


def preparar_banco(tmp_path):
    banco_teste = tmp_path / "teste.db"

    app.DB = str(banco_teste)
    app.init_db()

    return banco_teste


def test_pagina_inicial(tmp_path):
    preparar_banco(tmp_path)

    cliente = app.app.test_client()
    resposta = cliente.get("/")

    assert resposta.status_code == 200
    assert b"TechFlow Tasks" in resposta.data


def test_criar_tarefa_sem_titulo(tmp_path):
    preparar_banco(tmp_path)

    cliente = app.app.test_client()

    resposta = cliente.post(
        "/create",
        data={"title": ""}
    )

    assert resposta.status_code == 400


def test_criar_tarefa(tmp_path):
    banco = preparar_banco(tmp_path)

    cliente = app.app.test_client()

    resposta = cliente.post(
        "/create",
        data={
            "title": "Estudar Python",
            "description": "Revisar Flask",
            "priority": "Alta",
            "due_date": "2026-11-20"
        }
    )

    assert resposta.status_code == 302

    with sqlite3.connect(banco) as con:
        tarefa = con.execute(
            "SELECT * FROM tasks WHERE title = ?",
            ("Estudar Python",)
        ).fetchone()

    assert tarefa is not None


def test_editar_tarefa(tmp_path):
    banco = preparar_banco(tmp_path)

    with sqlite3.connect(banco) as con:
        cursor = con.execute(
            """
            INSERT INTO tasks
            (title, description, priority, status, due_date)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                "Tarefa antiga",
                "Descricao antiga",
                "Baixa",
                "A Fazer",
                ""
            )
        )

        tarefa_id = cursor.lastrowid

    cliente = app.app.test_client()

    resposta = cliente.post(
        f"/edit/{tarefa_id}",
        data={
            "title": "Tarefa atualizada",
            "description": "Descricao atualizada",
            "priority": "Critica",
            "status": "Em Progresso",
            "due_date": "2026-11-30"
        }
    )

    assert resposta.status_code == 302

    with sqlite3.connect(banco) as con:
        tarefa = con.execute(
            "SELECT title, priority, status FROM tasks WHERE id = ?",
            (tarefa_id,)
        ).fetchone()

    assert tarefa[0] == "Tarefa atualizada"
    assert tarefa[1] == "Critica"
    assert tarefa[2] == "Em Progresso"


def test_excluir_tarefa(tmp_path):
    banco = preparar_banco(tmp_path)

    with sqlite3.connect(banco) as con:
        cursor = con.execute(
            """
            INSERT INTO tasks (title)
            VALUES (?)
            """,
            ("Tarefa para excluir",)
        )

        tarefa_id = cursor.lastrowid

    cliente = app.app.test_client()

    resposta = cliente.post(
        f"/delete/{tarefa_id}"
    )

    assert resposta.status_code == 302

    with sqlite3.connect(banco) as con:
        tarefa = con.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (tarefa_id,)
        ).fetchone()

    assert tarefa is None