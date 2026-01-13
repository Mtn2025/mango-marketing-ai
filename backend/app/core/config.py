from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Mango Marketing AI"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str
    
    # Security
    ENCRYPTION_KEY: str
    
    # Google AI
    GOOGLE_API_KEY: Optional[str] = None
    
    # Azure OpenAI
    AZURE_OPENAI_ENDPOINT: Optional[str] = None
    AZURE_OPENAI_KEY: Optional[str] = None
    
    # Groq
    GROQ_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
