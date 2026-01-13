from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional


class BaseLLMProvider(ABC):
    """
    Clase base abstracta para proveedores de LLM (Large Language Models)
    """
    
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
    
    @abstractmethod
    async def generate_copy(
        self,
        prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Genera copy usando el modelo de IA
        
        Args:
            prompt: Prompt para generar el copy
            max_tokens: Número máximo de tokens
            temperature: Creatividad del modelo (0-1)
            **kwargs: Parámetros adicionales específicos del provider
            
        Returns:
            str: Copy generado
        """
        pass
    
    @abstractmethod
    async def get_model_info(self) -> Dict[str, Any]:
        """
        Obtiene información del modelo actual
        
        Returns:
            Dict con información del modelo (nombre, precio, velocidad, etc.)
        """
        pass


class BaseImageProvider(ABC):
    """
    Clase base abstracta para proveedores de generación de imágenes
    """
    
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
    
    @abstractmethod
    async def generate_image(
        self,
        prompt: str,
        width: int = 1024,
        height: int = 1024,
        num_images: int = 1,
        **kwargs
    ) -> List[bytes]:
        """
        Genera imágenes usando el modelo de IA
        
        Args:
            prompt: Prompt para generar la imagen
            width: Ancho de la imagen
            height: Alto de la imagen
            num_images: Número de imágenes a generar
            **kwargs: Parámetros adicionales específicos del provider
            
        Returns:
            List[bytes]: Lista de imágenes en bytes
        """
        pass
    
    @abstractmethod
    async def edit_image(
        self,
        image: bytes,
        prompt: str,
        **kwargs
    ) -> bytes:
        """
        Edita una imagen existente
        
        Args:
            image: Imagen en bytes
            prompt: Instrucciones de edición
            **kwargs: Parámetros adicionales
            
        Returns:
            bytes: Imagen editada
        """
        pass
    
    @abstractmethod
    async def get_model_info(self) -> Dict[str, Any]:
        """
        Obtiene información del modelo actual
        
        Returns:
            Dict con información del modelo (nombre, precio, capacidades, etc.)
        """
        pass


class ProviderFactory:
    """
    Factory para crear instancias de providers según configuración
    """
    
    @staticmethod
    def create_llm_provider(
        provider_name: str,
        api_key: str,
        model: str
    ) -> BaseLLMProvider:
        """
        Crea una instancia del provider de LLM especificado
        
        Args:
            provider_name: Nombre del provider ('groq', 'google', 'azure')
            api_key: API key del provider
            model: Nombre del modelo a usar
            
        Returns:
            BaseLLMProvider: Instancia del provider
        """
        from app.providers.llm.groq import GroqProvider
        from app.providers.llm.gemini import GeminiProvider
        # from app.providers.llm.azure_openai import AzureOpenAIProvider
        
        providers = {
            'groq': GroqProvider,
            'google': GeminiProvider,
            # 'azure': AzureOpenAIProvider,
        }
        
        provider_class = providers.get(provider_name.lower())
        if not provider_class:
            raise ValueError(f"Unknown LLM provider: {provider_name}")
        
        return provider_class(api_key=api_key, model=model)
    
    @staticmethod
    def create_image_provider(
        provider_name: str,
        api_key: str,
        model: str
    ) -> BaseImageProvider:
        """
        Crea una instancia del provider de imágenes especificado
        
        Args:
            provider_name: Nombre del provider ('google', 'azure', 'replicate')
            api_key: API key del provider
            model: Nombre del modelo a usar
            
        Returns:
            BaseImageProvider: Instancia del provider
        """
        from app.providers.image.google_imagen import GoogleImagenProvider
        # from app.providers.image.azure_flux import AzureFluxProvider
        
        providers = {
            'google': GoogleImagenProvider,
            # 'azure': AzureFluxProvider,
        }
        
        provider_class = providers.get(provider_name.lower())
        if not provider_class:
            raise ValueError(f"Unknown image provider: {provider_name}")
        
        return provider_class(api_key=api_key, model=model)
