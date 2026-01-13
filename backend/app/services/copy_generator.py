from typing import Dict, Any, Optional
from app.providers.base import ProviderFactory, BaseLLMProvider
from app.services.prompt_builder import PromptBuilder


class CopyGeneratorService:
    """
    Servicio para generar copy de marketing usando providers de IA
    """
    
    def __init__(self):
        self.prompt_builder = PromptBuilder()
    
    async def generate_copy(
        self,
        # Producto
        product_name: str,
        description: str,
        # Configuración
        platform: str,
        language: str = "es-MX",
        quality_level: str = "rapido",
        # Provider config
        llm_provider: str = "groq",
        llm_model: str = "llama-4-scout",
        api_key: str = None,
        # Copy config
        tone: str = "casual",
        length: str = "medio",
        use_emojis: bool = False,
        cta: Optional[str] = None,
        benefits: Optional[list] = None,
        keywords: Optional[list] = None,
        # Generation params
        temperature: float = 0.7,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Genera copy de marketing
        
        Returns:
            Dict con:
            - copy_text: El copy generado
            - metadata: Info del provider, modelo, costos, etc.
        """
        try:
            # 1. Crear provider
            provider: BaseLLMProvider = ProviderFactory.create_llm_provider(
                provider_name=llm_provider,
                api_key=api_key,
                model=llm_model
            )
            
            # 2. Construir prompt
            prompts = self.prompt_builder.build_copy_prompt(
                product_name=product_name,
                description=description,
                platform=platform,
                tone=tone,
                length=length,
                use_emojis=use_emojis,
                cta=cta,
                benefits=benefits,
                keywords=keywords,
                language=language
            )
            
            # 3. Crear prompt completo (system + user)
            full_prompt = f"{prompts['system']}\n\n{prompts['user']}"
            
            # 4. Generar copy
            copy_text = await provider.generate_copy(
                prompt=full_prompt,
                temperature=temperature,
                **kwargs
            )
            
            # 5. Obtener metadata del modelo
            model_info = await provider.get_model_info()
            
            return {
                "copy_text": copy_text,
                "metadata": {
                    "provider": llm_provider,
                    "model": llm_model,
                    "platform": platform,
                    "language": language,
                    "quality_level": quality_level,
                    "model_info": model_info,
                    "prompt_tokens": len(full_prompt.split()),  # Aproximado
                }
            }
            
        except Exception as e:
            raise Exception(f"Error generating copy: {str(e)}")
