from pydantic_settings import BaseSettings
from typing import Optional
from cryptography.fernet import Fernet


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Mango Marketing AI"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str
    
    # Security - Genera una key automática si no está configurada
    ENCRYPTION_KEY: str = Fernet.generate_key().decode()
    
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
