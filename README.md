# Framework Challenge

API REST de blog desenvolvida com Python 3 (Flask) e Postgres, utilizando containers Docker.

## Estrutura

O projeto foi desenvolvido seguindo o padrão de projeto *application factories* e algumas práticas do *twelve-factor app*, sendo:

* ```/app/__init__.py```: responsável por inicializar a aplicação e suas dependências, como *CORS*;

* ```/app/blueprints/```: contêm as regras de negócio, incluindo os models, desacoplado, para caso seja necessário utilizar os templates do Flask; e os endpoints, já versionados via blueprints + diretórios;

* ```/app/config/```: configurações da aplicação, segregadas por tipos de ambiente (*dev/local*, *prod* e *testing*);

* ```/app/ext/```: bibliotecas/extensões de terceiros utilizadas no projeto, como *sqlalchemy* e *flask-jwt-extended*;

* ```/app/tests/```: testes escritos com unittest;

* ```/migrations/```: arquivos de migração do Postgres;

* ```/scripts/```: scripts para, por exemplo, aplicar as *migrations* no container do Postgres;

* ```/static/```: diretório para armazenamento de imagens.

**Visão geral:**
```
.
├── app
│   ├── blueprints
│   │   ├── __init__.py
│   │   ├── models.py
│   │   └── rest_api
│   │       ├── __init__.py
│   │       ├── utils
│   │       │   └── __init__.py
│   │       └── v1
│   │           ├── album
│   │           │   ├── __init__.py
│   │           │   ├── resources.py
│   │           │   └── serializers.py
│   │           ├── comment
│   │           │   ├── __init__.py
│   │           │   ├── resources.py
│   │           │   └── serializers.py
│   │           ├── __init__.py
│   │           ├── post
│   │           │   ├── __init__.py
│   │           │   ├── resources.py
│   │           │   └── serializers.py
│   │           └── user
│   │               ├── __init__.py
│   │               ├── resources.py
│   │               └── serializers.py
│   ├── config
│   │   ├── config.py
│   │   └── __init__.py
│   ├── ext
│   │   ├── auth
│   │   │   ├── flask_jwt_extended.py
│   │   │   └── __init__.py
│   │   ├── database
│   │   │   ├── flask_sqlalchemy.py
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── log
│   │   │   └── __init__.py
│   │   └── serializer
│   │       ├── flask_marshmallow.py
│   │       └── __init__.py
│   ├── __init__.py
│   └── tests
│       ├── __init__.py
│       ├── test_album.py
│       ├── test_comment.py
│       ├── test_post.py
│       └── test_user.py
├── docs/
├── migrations/
├── scripts/
├── static/
├── .git/
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── README.md
├── requirements.txt
├── wsgi.py
├── .env
└── .gitignore
```

A aplicação pode ser executada nos seguintes ambientes: *dev*, *prod*, *testing* e *local*, todos em Docker, exceto *local*, que nada mais é que um ambiente de *dev* sem Docker, sendo necessário ter instalado Python 3 e demais ferramentas, como pip e virtualenv.

Cada ambiente possui database próprio via Docker, caso deseje trabalhar no ambiente *local*, instale o Postgres e crie um database, com usuário/senha, de acordo com o .env.

Para escolher algum dos ambientes, exporte-o para as variáveis de ambiente do SO: `export ENV_APP="dev"`, para ativar o ambiente de *dev*, `export ENV_APP="local"` para *local*, etc.

## Configurações

**Requisitos:**

* Git - https://git-scm.com/downloads

* Docker - https://docs.docker.com/engine/install/

* Docker Compose - https://docs.docker.com/compose/install/

Após instalar os requisitos acima:

1. Clone este repositório: `git clone https://github.com/daltroedu/framework-challenge.git`
2. Acesse o diretório: `cd framework-challenge/`
3. Exporte o ambiente de *dev*: `export ENV_APP="dev"`
4. Gere uma *SECRET_KEY* e exporte-a, exemplo:
    * `export SECRET_KEY="83r3tsr=tn7+%$uiotf+$xw*1+36n4(yfuu&0pf3j4e511p*82"`
    * Mas não utilize esta, gerar uma nova aqui: https://djecrety.ir/
    * E salve-a em local seguro
5. Faça *build* dos containers: `docker-compose build`
    * Depois da primeira, as próximas *builds* são mais rápidas
    * A aplicação (Flask) escuta na porta 5000 e o Postgres na 5432
6. Ative os containers: `docker-compose up`
    * Em outro terminal, você pode visualizar os containers com `docker ps`
    * Para encerrar, `docker-compose down` ou Ctrl+C

## Aplicação

Os endpoints estão divididos em quatro contextos, seguindo a lógica da regra de negócio: *users*, *albums*, *posts* e *comments*, requisitando autenticação via token JWT para algumas operações.

Endpoint padrão para *dev*: `http://localhost:5000/api/v1/...`

### Users

* **[POST]** `/api/v1/users`

    Criar usuário.

    Payload:

    ```JSON
    {
        "email": "admin@example.com",
        "username": "admin",
        "password": "admin",
        "name": "Admin"
    }
    ```

* **[POST]** `/api/v1/login`
    
    Obter token para determinado usuário.

    Payload:

    ```JSON
    {
        "email": "admin@example.com",
        "password": "admin"
    }
    ```

    Response:

    ```JSON
    {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTc0MjU5NDQsIm5iZiI6MTU5NzQyNTk0NCwianRpIjoiMTQzMjM3ODItMjdkOC00Yjg2LTllMzItN2UzYjQ4N2ZmZDJhIiwiZXhwIjoxNTk3NTEyMzQ0LCJpZGVudGl0eSI6MiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.NVgI2RxAAhAy4Ti5cHwFTgBGTrKau0mPv5_bW5wh2PY"
    }
    ```


### Albums

* **[POST]** `/api/v1/albums`

    Criar um álbum, com a possibilidade de adicionar várias fotos. Necessário ser um usuário autenticado.

    Exemplo via Insomnia:

    ![album_post](docs/imgs/album_post.jpg)

    Estrutura *Multipart Form*, para possibilitar POST de dados e imagens, com *Bearer Token* configurado utilizando token obtido via `/api/v1/login`.

* **[GET]** `/api/v1/albums/<id:int>`

    Consulta um álbum específico.

    Exemplo: `http://localhost:5000/api/v1/albums/1`

    Response:

    ```JSON
    {
        "id": 1,
        "images": [
            {
                "url": "http://localhost:5000/_uploads/photos/praia.jpg"
            },
            {
                "url": "http://localhost:5000/_uploads/photos/restaurante.jpg"
            }
        ],
        "created_at": "2020-08-15T03:13:18.971329",
        "contents": "Viagem do ano passado",
        "title": "Viagem",
        "user_id": 1
    }
    ```

* **[GET]** `/api/v1/albums`

    Consulta todos os álbums, com response paginado.

    Response:

    ```JSON
    {
        "_meta": {
            "page": 1,
            "per_page": 10,
            "total_pages": 1,
            "total_items": 1
        },
        "_links": {
            "self": "/api/v1/albums?page=1&per_page=10",
            "next": null,
            "prev": null
        },
        "items": [
            {
                "id": 1,
                "images": [
                    {
                        "url": "http://localhost:5000/_uploads/photos/praia.jpg"
                    },
                    {
                        "url": "http://localhost:5000/_uploads/photos/restaurante.jpg"
                    }
                ],
                "created_at": "2020-08-15T03:13:18.971329",
                "contents": "Viagem do ano passado",
                "title": "Viagem",
                "user_id": 1
            }
        ]
    }
    ```

* **[DELETE]** `/api/v1/albums/<id:int>`

    Deleta um álbum e suas respectivas fotos. Necessário ser um usuário autenticado e somente o respectivo criador poderá realizar a operação.

    Exemplo: `http://localhost:5000/api/v1/albums/1`


### Posts

* **[POST]** `/api/v1/posts`

    Cria um post, e possui os mesmos parâmetros de `/api/v1/albums`: possibilidade de adicionar dados (*title* e *contents*) junto a várias imagens, via estrutura *Multipart Form*, sendo também necessário ser um usuário autenticado.

* **[GET]** `/api/v1/posts/<id:int>`

    Consulta um post específico, incluindo seus respectivos comentários, se houver.

    Exemplo: `http://localhost:5000/api/v1/posts/1`

    Response:

    ```JSON
    {
        "title": "Meu primeiro post",
        "created_at": "2020-08-15T08:51:41.608844",
        "user_id": 1,
        "id": 1,
        "comments": [],
        "contents": "Este é o meu primeiro post",
        "images": [
            {
                "url": "http://localhost:5000/_uploads/photos/tutorial_01.jpg"
            },
            {
                "url": "http://localhost:5000/_uploads/photos/tutorial_02.jpg"
            }
        ]
    }
    ```

* **[GET]** `/api/v1/posts`

    Consulta todos os posts, com response paginado.

    Response:

    ```JSON
    {
        "_meta": {
            "page": 1,
            "per_page": 10,
            "total_pages": 1,
            "total_items": 1
        },
        "_links": {
            "self": "/api/v1/posts?page=1&per_page=10",
            "next": null,
            "prev": null
        },
        "items": [
            {
                "title": "Meu primeiro post",
                "created_at": "2020-08-15T08:51:41.608844",
                "user_id": 1,
                "id": 1,
                "comments": [],
                "contents": "Este é o meu primeiro post",
                "images": [
                    {
                        "url": "http://localhost:5000/_uploads/photos/tutorial_01.jpg"
                    },
                    {
                        "url": "http://localhost:5000/_uploads/photos/tutorial_02.jpg"
                    }
                ]
            }
        ]
    }
    ```

* **[DELETE]** `/api/v1/posts/<id:int>`

    Deleta um post e suas respectivas imagens e comentários. Necessário ser um usuário autenticado e somente o respectivo criador poderá realizar a operação.

    Exemplo: `http://localhost:5000/api/v1/posts/1`

### Comments

* **[POST]** `/api/v1/comments`
    
    Adiciona um comentário a um determinado post. Necessário ser um usuário autenticado.

    Payload:

    ```JSON
    {
        "post_id": 1,
        "contents": "Muito bom este tutorial!"
    }
    ```

    Agora o post #1, criado na seção anterior, possui um comentário:

    ```JSON
    {
        "title": "Meu primeiro post",
        "created_at": "2020-08-15T08:51:41.608844",
        "user_id": 1,
        "id": 1,
        "contents": "Este é o meu primeiro post",
        "images": [
            {
                "url": "http://localhost:5000/_uploads/photos/tutorial_01.jpg"
            },
            {
                "url": "http://localhost:5000/_uploads/photos/tutorial_02.jpg"
            }
        ],
        "comments": [
            {
                "contents": "Muito bom este tutorial!",
                "id": 1
            }
        ]
    }
    ```

* **[GET]** `/api/v1/comments/<id:int>`

    Consulta um comentário específico.

    Exemplo: `http://localhost:5000/api/v1/comments/1`

    Response:

    ```JSON
    {
        "contents": "Muito bom este tutorial!",
        "id": 1,
        "post_id": 1,
        "user_id": 1,
        "created_at": "2020-08-15T09:04:29.567075"
    }
    ```

* **[GET]** `/api/v1/comments`

    Consulta todos os comentários, com response paginado.

    Response:

    ```JSON
    {
        "_meta": {
            "page": 1,
            "per_page": 10,
            "total_pages": 1,
            "total_items": 1
        },
        "_links": {
            "self": "/api/v1/comments?page=1&per_page=10",
            "next": null,
            "prev": null
        },
        "items": [
            {
                "contents": "Muito bom este tutorial!",
                "id": 1,
                "post_id": 1,
                "user_id": 1,
                "created_at": "2020-08-15T09:04:29.567075"
            }
        ]
    }
    ```

* **[DELETE]** `/api/v1/comments/<id:int>`

    Deleta um comentário. Necessário ser um usuário autenticado e somente o respectivo criador poderá realizar a operação.

    Exemplo: `http://localhost:5000/api/v1/comments/1`

### Testes

1. Acesse o container do app: `docker exec -it framework-challenge-app bash`
    * Se não conseguir desta forma, com *NAMES*, tente via *CONTAINER ID*:
        * `docker ps` para listar os containers
        * Localize o *CONTAINER ID* do *app*, por exemplo: `24fd17f35abf`
        * Execute: `docker exec -it 24fd17f35abf bash`

2. Exporte a variável de ambiente para testes: `export ENV_APP=testing`

3. Execute os testes: `python -m unittest discover app/tests`
    * `exit` ou Ctrl+D para sair