from typing import Dict, Any
import google.generativeai as genai

from app.providers.base import BaseLLMProvider


class GeminiProvider(BaseLLMProvider):
    """
    Provider para Google Gemini (2.0 Flash-Lite, 2.5 Flash)
    - Gemini 2.0 Flash-Lite: $0.075/1M input, ultra económico
    - Gemini 2.5 Flash: $0.30/1M input, visión multimodal
    """
    
    MODEL_INFO = {
        "gemini-2.0-flash-lite": {
            "name": "Gemini 2.0 Flash-Lite",
            "input_cost": 0.075,
            "output_cost": 0.225,
            "context_window": 1_000_000,
            "capabilities": ["text", "multimodal"],
        },
        "gemini-2.5-flash": {
            "name": "Gemini 2.5 Flash",
            "input_cost": 0.30,
            "output_cost": 0.60,
            "context_window": 1_000_000,
            "capabilities": ["text", "vision", "multimodal"],
        }
    }
    
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash-lite"):
        super().__init__(api_key, model)
        genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel(model)
    
    async def generate_copy(
        self,
        prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Genera copy usando Gemini
        """
        try:
            generation_config = genai.GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=temperature,
            )
            
            response = self.client.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            return response.text
            
        except Exception as e:
            raise Exception(f"Error generating copy with Gemini: {str(e)}")
    
    async def get_model_info(self) -> Dict[str, Any]:
        """
        Obtiene información del modelo Gemini
        """
        return self.MODEL_INFO.get(self.model, {})
