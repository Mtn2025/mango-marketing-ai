from typing import Dict, Any
from groq import Groq
import httpx

from app.providers.base import BaseLLMProvider


class GroqProvider(BaseLLMProvider):
    """
    Provider para Groq (Llama 4 Scout)
    - Ultra rápido: 594 tokens/segundo
    - Económico: $0.11/1M input, $0.34/1M output
    """
    
    MODEL_INFO = {
        "llama-4-scout": {
            "name": "Llama 4 Scout",
            "speed": "594 TPS",
            "input_cost": 0.11,  # por 1M tokens
            "output_cost": 0.34,
            "context_window": 128000,
            "capabilities": ["text", "image_understanding"],
        }
    }
    
    def __init__(self, api_key: str, model: str = "llama-4-scout"):
        super().__init__(api_key, model)
        self.client = Groq(api_key=api_key)
    
    async def generate_copy(
        self,
        prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Genera copy usando Llama 4 Scout
        """
        try:
            # Groq usa sync API, pero lo envolvemos en async context
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                **kwargs
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Error generating copy with Groq: {str(e)}")
    
    async def get_model_info(self) -> Dict[str, Any]:
        """
        Obtiene información del modelo Llama 4 Scout
        """
        return self.MODEL_INFO.get(self.model, {})
