import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    APP_NAME: str = "AI Avatar API"

    # OpenAI API key - assuming we're using OpenAI for the AI agent
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # Vector database settings if needed
    VECTOR_DB_PATH: str = os.getenv("VECTOR_DB_PATH", "./data/vector_db")

    # Path to PDF files
    PDF_DIR: str = os.getenv("PDF_DIR", "./data/pdfs")

    # Model settings
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4")
    
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "api-key")
    
    ANTHROPIC_MODEL_NAME: str = os.getenv("ANTHROPIC_MODEL_NAME", "claude-3-haiku-20240307")


    class Config:
        env_file = ".env"


settings = Settings()
