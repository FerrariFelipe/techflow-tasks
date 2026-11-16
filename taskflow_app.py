import sqlite3
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

DB = "taskflow.db"


def init_db():
    with sqlite3.connect(DB) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                priority TEXT NOT NULL DEFAULT 'Media',
                status TEXT NOT NULL DEFAULT 'A Fazer',
                due_date TEXT DEFAULT ''
            )
        """)


def get_tasks():
    with sqlite3.connect(DB) as con:
        con.row_factory = sqlite3.Row
        return con.execute(
            "SELECT * FROM tasks ORDER BY id DESC"
        ).fetchall()


HTML = """
<!doctype html>

<html>
<head>
    <meta charset="utf-8">
    <title>TechFlow Tasks</title>

    <style>
        body {
            font-family: Arial;
            max-width: 1200px;
            margin: 30px auto;
            background: #f6f7fb;
        }

        h1 {
            color: #222;
        }

        form, .card {
            background: white;
            padding: 16px;
            margin: 12px 0;
            border-radius: 10px;
        }

        input, select, button {
            padding: 8px;
            margin: 4px;
        }

        .cols {
            display: flex;
            gap: 20px;
        }

        .col {
            flex: 1;
        }

        .card {
            box-shadow: 0 2px 5px #ccc;
        }

        .editar {
            background: #007bff;
            color: white;
            border: none;
            cursor: pointer;
        }

        .excluir {
            background: #dc3545;
            color: white;
            border: none;
            cursor: pointer;
        }

        .atualizar {
            background: #28a745;
            color: white;
            border: none;
            cursor: pointer;
        }
    </style>
</head>

<body>

<h1>TechFlow Tasks</h1>

<p>Sistema de gerenciamento de tarefas</p>

<h2>Nova tarefa</h2>

<form method="post" action="/create">

    <input
        name="title"
        placeholder="Titulo"
        required
    >

    <input
        name="description"
        placeholder="Descricao"
    >

    <select name="priority">
        <option>Baixa</option>
        <option selected>Media</option>
        <option>Alta</option>
        <option>Critica</option>
    </select>

    <input
        type="date"
        name="due_date"
    >

    <button type="submit">
        Criar
    </button>

</form>


<div class="cols">

{% for s in statuses %}

<div class="col">

    <h2>{{ s }}</h2>

    {% for t in tasks if t['status'] == s %}

    <div class="card">

        <form
            method="post"
            action="/edit/{{ t['id'] }}"
        >

            <label>Titulo:</label>

            <input
                name="title"
                value="{{ t['title'] }}"
                required
            >

            <br>

            <label>Descricao:</label>

            <input
                name="description"
                value="{{ t['description'] }}"
            >

            <br>

            <label>Prioridade:</label>

            <select name="priority">

                {% for p in priorities %}

                <option
                    {% if p == t['priority'] %}
                    selected
                    {% endif %}
                >
                    {{ p }}
                </option>

                {% endfor %}

            </select>

            <br>

            <label>Prazo:</label>

            <input
                type="date"
                name="due_date"
                value="{{ t['due_date'] }}"
            >

            <br>

            <label>Status:</label>

            <select name="status">

                {% for x in statuses %}

                <option
                    {% if x == t['status'] %}
                    selected
                    {% endif %}
                >
                    {{ x }}
                </option>

                {% endfor %}

            </select>

            <br>

            <button
                class="editar"
                type="submit"
            >
                Salvar alteracoes
            </button>

        </form>


        <form
            method="post"
            action="/delete/{{ t['id'] }}"
        >

            <button
                class="excluir"
                type="submit"
            >
                Excluir
            </button>

        </form>

    </div>

    {% endfor %}

</div>

{% endfor %}

</div>

</body>
</html>
"""


@app.get("/")
def index():

    return render_template_string(
        HTML,
        tasks=get_tasks(),
        statuses=[
            "A Fazer",
            "Em Progresso",
            "Concluido"
        ],
        priorities=[
            "Baixa",
            "Media",
            "Alta",
            "Critica"
        ]
    )


@app.post("/create")
def create():

    title = request.form.get(
        "title",
        ""
    ).strip()

    if not title:
        return "Titulo obrigatorio", 400

    description = request.form.get(
        "description",
        ""
    )

    priority = request.form.get(
        "priority",
        "Media"
    )

    due_date = request.form.get(
        "due_date",
        ""
    )

    with sqlite3.connect(DB) as con:

        con.execute(
            """
            INSERT INTO tasks
            (
                title,
                description,
                priority,
                due_date
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                title,
                description,
                priority,
                due_date
            )
        )

    return redirect("/")


@app.post("/edit/<int:id>")
def edit(id):

    title = request.form.get(
        "title",
        ""
    ).strip()

    if not title:
        return "Titulo obrigatorio", 400

    description = request.form.get(
        "description",
        ""
    )

    priority = request.form.get(
        "priority",
        "Media"
    )

    status = request.form.get(
        "status",
        "A Fazer"
    )

    due_date = request.form.get(
        "due_date",
        ""
    )

    with sqlite3.connect(DB) as con:

        con.execute(
            """
            UPDATE tasks

            SET
                title = ?,
                description = ?,
                priority = ?,
                status = ?,
                due_date = ?

            WHERE id = ?
            """,
            (
                title,
                description,
                priority,
                status,
                due_date,
                id
            )
        )

    return redirect("/")


@app.post("/delete/<int:id>")
def delete(id):

    with sqlite3.connect(DB) as con:

        con.execute(
            "DELETE FROM tasks WHERE id = ?",
            (id,)
        )

    return redirect("/")


if __name__ == "__main__":

    init_db()

    app.run(debug=True)
