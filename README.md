## Setup

```shell
cp .env.example .env
pip install -r requirements.txt
```

```shell
# start dev server
uvicorn src.main:app --reload

or

docker build -t avatar-api .
docker run -p 8000:80 avatar-api
```

Docs `http://localhost:8000/docs`

```
curl -X POST http://localhost:8000/personalities/community/ask \  -H "Content-Type: application/json" \  -d '{"text": "How would you evaluate a project?", "user_id": "test_user"}'
```

## Structure

```
.
├── README.md
├── data
│   ├── pdfs
│   │   ├── community.pdf
│   │   ├── efficiency.pdf
│   │   ├── equity.pdf
│   │   ├── innovation.pdf
│   │   └── sustainability.pdf
│   └── vector_db
│       └── chroma.sqlite3
├── lib
│   └── deepgov-modelspec
│       ├── README.md
│       ├── agents
│       │   ├── community
│       │   ├── efficiency
│       │   ├── equity
│       │   ├── innovation
│       │   └── sustainability
│       └── prompts
│           └── model-spec.md
├── requirements.txt
└── src
    ├── __init__.py
    ├── api
    │   ├── __init__.py
    │   ├── personality_routes.py
    │   └── routes.py
    ├── config.py
    ├── main.py
    ├── models
    │   └── schemas.py
    ├── prompt-templete.py
    └── services
        ├── ai_agent.py
        ├── personalities
        │   ├── __init__.py
        │   ├── base.py
        │   ├── community.py
        │   ├── efficiency.py
        │   ├── equity.py
        │   ├── innovation.py
        │   └── sustainability.py
        └── personality_manager.py
```
