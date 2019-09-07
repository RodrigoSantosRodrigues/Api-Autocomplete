# API AUTO COMPLETE
serviço de autocomplete

## Compatibility
* [Requisito: Python 3.7.3]

## Instalação
  - Instalar [Python](https://www.python.org/downloads/) e [Postgres](https://www.postgresql.org/) 
 
  - Instalar ambiente virtual `pip install Pipenv`
  - Criar ambiente virtual `$ pipenv shell` 
  - Instalar dependências  `$ pipenv install`

  - Renomear `.env.example` para `.env`

 ## Configure o .env
  - Exemplo:
```
APP_HOST= localhost
APP_PORT= 5000
FLASK_ENV=development
.
.
.
```

## Migrações
  - Iniciar migrations
```
python manage.py db init
```
  - Migrar modelos
```
python manage.py db migrate
```
  - Atualizar migrações com o banco de dados
```
python manage.py db upgrade
```

## Start o APP
  - Iniciar APP `python run.py`


Configurado corretamente a página inicial do aplicativo pode ser acessado pelo endereço `http://localhost:5000`, a documentação da API pode ser acessada pelo endereço `http://localhost:5000/apidocs/`


Notes
=================
 - Para desemvolver o Autocomplete foi utilizado python na versão 3.7.3, compatível com python > 2.7
 - Flask microframework e quart. Foi utilizado o Quart e Flask concorrentemente, a implementação do projeto
   concorrente é nescessário para projeto com grande número de requisições e agilidade.
 - O banco de dados utilizado foi o postgres, Mongodb também é uma boa escolha para grandes volumes de dados.
 - A biblioteca autocomplete para python permite um treinamento de modelos próprio, ou seja, auto complete de acordo com dados de nagevação de cada usuário. As palavras autocompletadas seguem a idéia de peso, ou seja, de acordo com o peso em que os eventos são gerados.
  Exemplo:  "pagar" tem uma maior chance de ser autocompletada quando "pa" for solicitado.
```
'pagar'  -> 842
'comprar' -> 125
'produto' -> 406
'valor' -> 393
```
 

  - Foi implementado End Points de usuário, é nescessário cadastrar um usuário, é retornado um token de autenticação para usar os outros End Points. 