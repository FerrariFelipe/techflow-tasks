## TechFlow Tasks

Sistema web para gerenciamento de tarefas desenvolvido como projeto da disciplina de Software Engineering.
## Objetivo

O TechFlow Tasks tem como objetivo permitir o gerenciamento de tarefas por meio de uma interface web simples e intuitiva.

O sistema permite cadastrar tarefas, definir prioridade e prazo, acompanhar o andamento e excluir tarefas.
## Funcionalidades

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

## Tecnologias

    Python
    Flask
    SQLite
    HTML
    CSS
    Pytest

## Banco de dados

O sistema utiliza SQLite para armazenar as tarefas.

O banco é criado automaticamente na primeira execução da aplicação.
## Testes automatizados

Os testes foram desenvolvidos utilizando Pytest.

Para executá-los:

python -m pytest -v
## Executando o projeto

Instale as dependências:

python -m pip install -r requirements.txt

Execute:

python taskflow_app.py

Acesse no navegador:

http://127.0.0.1:5000
## Mudança de escopo
Escopo inicial

Inicialmente, o sistema foi planejado para realizar o CRUD de tarefas, permitindo:

    criação de tarefas;
    visualização das tarefas;
    atualização das informações;
    alteração do status;
    exclusão de tarefas.

Necessidade identificada

Durante o desenvolvimento, foi identificada a necessidade de controlar também os prazos das atividades. Apenas o status e a prioridade não eram suficientes para indicar quando cada tarefa deveria ser concluída.
Alteração realizada

Por esse motivo, o escopo do projeto foi ampliado com a inclusão do campo data limite, permitindo definir um prazo para cada tarefa.

Essa mudança exigiu adaptações:

    no banco de dados SQLite;
    no formulário de criação;
    na edição das tarefas;
    na interface da aplicação;
    nos testes automatizados.

Impacto no projeto

A mudança melhorou o acompanhamento das atividades e demonstrou a capacidade de adaptação do projeto diante de novos requisitos.
A funcionalidade foi implementada sem remover os recursos planejados originalmente e foi validada por meio dos testes automatizados.