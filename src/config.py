import os
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    APP_NAME: str = Field("AI Avatar API")

    # API keys
    OPENAI_API_KEY: str = Field(os.getenv("OPENAI_API_KEY", ""))
    ANTHROPIC_API_KEY: str = Field(os.getenv("ANTHROPIC_API_KEY", ""))

    # Path settings
    VECTOR_DB_PATH: str = Field(
        os.getenv("VECTOR_DB_PATH", os.path.join(PROJECT_ROOT, "data", "vector_db"))
    )
    PDF_DIR: str = Field(
        os.getenv("PDF_DIR", os.path.join(PROJECT_ROOT, "data", "pdfs"))
    )

    # Model settings
    MODEL_NAME: str = Field(os.getenv("MODEL_NAME", "gpt-3.5-turbo"))
    ANTHROPIC_MODEL_NAME: str = Field(
        os.getenv("ANTHROPIC_MODEL_NAME", "claude-3-haiku-20240307")
    )

    class Config:
        env_file = ".env"


settings = Settings()

# Export PROJECT_ROOT as a module-level variable
__all__ = ["settings", "PROJECT_ROOT"]
