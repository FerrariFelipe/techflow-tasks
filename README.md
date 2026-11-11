TechFlow Tasks

Sistema web para gerenciamento de tarefas desenvolvido como projeto da disciplina de Software Engineering.
Objetivo

O TechFlow Tasks tem como objetivo permitir o gerenciamento de tarefas por meio de uma interface web simples e intuitiva.

O sistema permite cadastrar tarefas, definir prioridade e prazo, acompanhar o andamento e excluir tarefas.
Funcionalidades

    Criar tarefas
    Visualizar tarefas
    Definir prioridade
    Definir prazo
    Alterar status
    Excluir tarefas
    Organização em:
        A Fazer
        Em Progresso
        Concluído

Tecnologias

    Python
    Flask
    SQLite
    HTML
    CSS
    Pytest

Banco de dados

O sistema utiliza SQLite para armazenar as tarefas.

O banco é criado automaticamente na primeira execução da aplicação.
Testes automatizados

Os testes foram desenvolvidos utilizando Pytest.

Para executá-los:

python -m pytest -v
Executando o projeto

Instale as dependências:

python -m pip install -r requirements.txt

Execute:

python taskflow_app.py

Acesse no navegador:

http://127.0.0.1:5000
Mudança de escopo

Inicialmente, o sistema foi planejado para realizar o CRUD de tarefas, permitindo criação, visualização, atualização e exclusão.

Durante o desenvolvimento, foi identificada a necessidade de controlar também o prazo das atividades.

Por esse motivo, o escopo foi ampliado com a funcionalidade de data limite para cada tarefa.

Essa mudança permite melhorar o acompanhamento das atividades e demonstrar a adaptação do projeto a novos requisitos.