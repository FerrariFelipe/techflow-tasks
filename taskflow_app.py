import sqlite3
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)
DB='taskflow.db'

def init_db():
    with sqlite3.connect(DB) as con:
        con.execute('''CREATE TABLE IF NOT EXISTS tasks (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          title TEXT NOT NULL,
          description TEXT DEFAULT '',
          priority TEXT NOT NULL DEFAULT 'Media',
          status TEXT NOT NULL DEFAULT 'A Fazer',
          due_date TEXT DEFAULT ''
        )''')

def get_tasks():
    with sqlite3.connect(DB) as con:
        con.row_factory=sqlite3.Row
        return con.execute('SELECT * FROM tasks ORDER BY id DESC').fetchall()

HTML='''<!doctype html><html><head><meta charset="utf-8"><title>TechFlow Tasks</title>
<style>body{font-family:Arial;max-width:1000px;margin:30px auto;background:#f6f7fb}form,.card{background:white;padding:16px;margin:12px;border-radius:10px}input,select,button{padding:8px;margin:4px} .cols{display:flex;gap:10px}.col{flex:1}</style></head>
<body><h1>TechFlow Tasks</h1><p>Gerenciamento agil de tarefas</p>
<form method="post" action="/create"><input name="title" placeholder="Titulo" required><input name="description" placeholder="Descricao"><select name="priority"><option>Baixa</option><option selected>Media</option><option>Alta</option><option>Critica</option></select><input type="date" name="due_date"><button>Criar</button></form>
<div class="cols">{% for s in statuses %}<div class="col"><h2>{{s}}</h2>{% for t in tasks if t['status']==s %}<div class="card"><b>{{t['title']}}</b><p>{{t['description']}}</p><small>Prioridade: {{t['priority']}} | Prazo: {{t['due_date'] or '-'}}</small><form method="post" action="/update/{{t['id']}}"><select name="status">{% for x in statuses %}<option {% if x==t['status'] %}selected{% endif %}>{{x}}</option>{% endfor %}</select><button>Atualizar</button></form><form method="post" action="/delete/{{t['id']}}"><button>Excluir</button></form></div>{% endfor %}</div>{% endfor %}</div></body></html>'''

@app.get('/')
def index():
    return render_template_string(HTML,tasks=get_tasks(),statuses=['A Fazer','Em Progresso','Concluido'])
@app.post('/create')
def create():
    title=request.form.get('title','').strip()
    if not title: return 'Titulo obrigatorio',400
    with sqlite3.connect(DB) as con:
        con.execute('INSERT INTO tasks(title,description,priority,due_date) VALUES(?,?,?,?)',(title,request.form.get('description',''),request.form.get('priority','Media'),request.form.get('due_date','')))
    return redirect('/')
@app.post('/update/<int:id>')
def update(id):
    status=request.form.get('status','A Fazer')
    with sqlite3.connect(DB) as con: con.execute('UPDATE tasks SET status=? WHERE id=?',(status,id))
    return redirect('/')
@app.post('/delete/<int:id>')
def delete(id):
    with sqlite3.connect(DB) as con: con.execute('DELETE FROM tasks WHERE id=?',(id,))
    return redirect('/')

if __name__=='__main__':
    init_db(); app.run(debug=True)
