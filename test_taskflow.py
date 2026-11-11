import taskflow_app as app


def test_pagina_inicial():
    app.init_db()

    cliente = app.app.test_client()
    resposta = cliente.get("/")

    assert resposta.status_code == 200


def test_criar_tarefa_sem_titulo():
    app.init_db()

    cliente = app.app.test_client()

    resposta = cliente.post(
        "/create",
        data={"title": ""}
    )

    assert resposta.status_code == 400