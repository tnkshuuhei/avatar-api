```
./
├── src/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── config.py         # Configuration settings
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py    # Pydantic models for request/response
│   ├── services/
│   │   ├── __init__.py
│   │   └── ai_agent.py   # AI agent logic
│   └── api/
│       ├── __init__.py
│       └── routes.py     # API endpoints
├── data/
│   └── pdfs/            # Directory to store PDF files
├── tests/               # Unit and integration tests
│   └── __init__.py
├── requirements.txt     # Project dependencies
└── .env                # Environment variables (not in version control)
```
