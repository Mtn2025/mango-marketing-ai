from typing import Dict, Any, Optional


class PromptBuilder:
    """
    Constructor de prompts para generación de copy
    Soporta ES-MX e EN
    """
    
    SYSTEM_PROMPTS = {
        "es-MX": """Eres un experto copywriter de marketing digital especializado en crear contenido persuasivo para redes sociales en México.

Tu objetivo es crear copy que:
- Capte la atención inmediatamente
- Sea claro y directo
- Genere emoción y conexión
- Incluya un call-to-action efectivo
- Use lenguaje natural y conversacional mexicano

Importante:
- Usa "tú" en lugar de "usted" (más cercano)
- Adapta el tono al producto/servicio
- Mantén el copy conciso pero impactante
- Si se solicitan emojis, úsalos estratégicamente (no en exceso)""",
        
        "en": """You are an expert digital marketing copywriter specialized in creating persuasive content for social media.

Your goal is to create copy that:
- Captures attention immediately
- Is clear and direct
- Generates emotion and connection
- Includes an effective call-to-action
- Uses natural, conversational language

Important:
- Adapt the tone to the product/service
- Keep copy concise but impactful
- If emojis are requested, use them strategically (not excessively)"""
    }
    
    @staticmethod
    def build_copy_prompt(
        product_name: str,
        description: str,
        platform: str,
        tone: str = "casual",
        length: str = "medio",
        use_emojis: bool = False,
        cta: Optional[str] = None,
        benefits: Optional[list] = None,
        keywords: Optional[list] = None,
        language: str = "es-MX"
    ) -> Dict[str, str]:
        """
        Construye el prompt para generación de copy
        
        Args:
            product_name: Nombre del producto/servicio
            description: Descripción detallada
            platform: Red social (facebook, instagram, tiktok, linkedin, whatsapp)
            tone: Tono del mensaje (casual, formal, juvenil, profesional)
            length: Longitud (corto, medio, largo)
            use_emojis: Si debe incluir emojis
            cta: Call to action personalizado
            benefits: Lista de beneficios clave
            keywords: Palabras clave a incluir
            language: Idioma (es-MX, en)
            
        Returns:
            Dict con 'system' y 'user' prompts
        """
        
        # Mapeo de longitudes
        length_guides = {
            "es-MX": {
                "corto": "máximo 50 palabras",
                "medio": "entre 50-100 palabras",
                "largo": "entre 100-150 palabras"
            },
            "en": {
                "corto": "maximum 50 words",
                "medio": "between 50-100 words",
                "largo": "between 100-150 words"
            }
        }
        
        # Mapeo de plataformas
        platform_guides = {
            "facebook": {
                "es-MX": "contenido que fomente la interacción y el compartir",
                "en": "content that encourages interaction and sharing"
            },
            "instagram": {
                "es-MX": "conciso, visual, con hashtags relevantes al final",
                "en": "concise, visual-focused, with relevant hashtags at the end"
            },
            "tiktok": {
                "es-MX": "dinámico, juvenil, que llame a la acción inmediata",
                "en": "dynamic, youthful, with immediate call-to-action"
            },
            "linkedin": {
                "es-MX": "profesional, enfocado en valor y resultados",
                "en": "professional, focused on value and results"
            },
            "whatsapp": {
                "es-MX": "personal, directo, como un mensaje de amigo",
                "en": "personal, direct, like a message from a friend"
            }
        }
        
        # Construir prompt de usuario
        if language == "es-MX":
            user_prompt = f"""Crea un copy de marketing para {platform} sobre el siguiente producto:

Producto: {product_name}
Descripción: {description}

Especificaciones:
- Tono: {tone}
- Longitud: {length_guides[language][length]}
- Plataforma: {platform} ({platform_guides.get(platform, {}).get(language, '')})
"""
        else:  # en
            user_prompt = f"""Create marketing copy for {platform} about the following product:

Product: {product_name}
Description: {description}

Specifications:
- Tone: {tone}
- Length: {length_guides[language][length]}
- Platform: {platform} ({platform_guides.get(platform, {}).get(language, '')})
"""
        
        # Agregar beneficios si existen
        if benefits:
            if language == "es-MX":
                user_prompt += f"\nBeneficios clave:\n"
                for benefit in benefits[:3]:  # Máximo 3
                    user_prompt += f"- {benefit}\n"
            else:
                user_prompt += f"\nKey benefits:\n"
                for benefit in benefits[:3]:
                    user_prompt += f"- {benefit}\n"
        
        # Agregar keywords si existen
        if keywords:
            keywords_str = ", ".join(keywords[:5])  # Máximo 5
            if language == "es-MX":
                user_prompt += f"\nPalabras clave a incluir: {keywords_str}\n"
            else:
                user_prompt += f"\nKeywords to include: {keywords_str}\n"
        
        # Agregar emojis
        if use_emojis:
            if language == "es-MX":
                user_prompt += "\n✨ Incluye emojis relevantes (máximo 3-4) para hacer el copy más atractivo.\n"
            else:
                user_prompt += "\n✨ Include relevant emojis (maximum 3-4) to make the copy more engaging.\n"
        
        # Agregar CTA
        if cta:
            if language == "es-MX":
                user_prompt += f"\nCall-to-action: {cta}\n"
            else:
                user_prompt += f"\nCall-to-action: {cta}\n"
        else:
            if language == "es-MX":
                user_prompt += "\nIncluye un call-to-action efectivo al final.\n"
            else:
                user_prompt += "\nInclude an effective call-to-action at the end.\n"
        
        return {
            "system": PromptBuilder.SYSTEM_PROMPTS[language],
            "user": user_prompt
        }
