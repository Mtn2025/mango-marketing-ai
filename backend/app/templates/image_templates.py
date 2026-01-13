"""
Templates de imagen por plataforma

Del implementation_plan.md líneas 261, 459-497
"""

# Tamaños de imagen por plataforma (del plan líneas 462-486)
IMAGE_SIZES = {
    "facebook": {
        "feed": (1200, 630),        # Landscape
        "story": (1080, 1920),      # Vertical
        "cuadrado": (1080, 1080)
    },
    "instagram": {
        "cuadrado": (1080, 1080),   # Post estándar
        "portrait": (1080, 1350),   # 4:5
        "story": (1080, 1920),      # Story/Reel
        "landscape": (1080, 566)    # 1.91:1
    },
    "tiktok": {
        "video": (1080, 1920),      # Vertical (9:16)
        "thumbnail": (1080, 1920)
    },
    "linkedin": {
        "feed": (1200, 627),        # Post
        "story": (1080, 1920)
    },
    "whatsapp": {
        "status": (1080, 1920),     # Story/estado
        "cuadrado": (1080, 1080)    # Mensaje
    }
}

# Configuración de imagen por tipo
IMAGE_TYPE_CONFIG = {
    "producto": {
        "position": "center",
        "background": "white",
        "padding": 0.05,  # 5%
        "effects": ["rounded_corners"],
        "logo_position": "bottom-right"
    },
    "servicio": {
        "position": "center",
        "background": "gradient",
        "padding": 0.03,
        "effects": ["glow"],
        "logo_position": "bottom-left"
    },
    "logo": {
        "position": "corner",
        "background": "transparent",
        "padding": 0,
        "effects": [],
        "overlay": True
    }
}

# Prompts base por tipo de imagen
IMAGE_PROMPTS = {
    "es-MX": {
        "producto": "Fotografía profesional de {product_name}, fondo limpio, iluminación suave, alta calidad, estilo comercial",
        "servicio": "Escena profesional de {service_description}, personas satisfechas, ambiente cálido, iluminación natural",
        "logo": "Logo profesional minimalista para {brand_name}, diseño moderno, vectorial, fondo transparente"
    },
    "en": {
        "producto": "Professional product photography of {product_name}, clean background, soft lighting, high quality, commercial style",
        "servicio": "Professional scene of {service_description}, satisfied customers, warm atmosphere, natural lighting",
        "logo": "Professional minimalist logo for {brand_name}, modern design, vector, transparent background"
    }
}

def get_image_size(platform: str, format_type: str = "cuadrado") -> tuple:
    """
    Obtiene tamaño de imagen para plataforma y formato
    
    Args:
        platform: facebook, instagram, tiktok, linkedin, whatsapp
        format_type: cuadrado, portrait, story, feed, etc.
        
    Returns:
        (width, height) en píxeles
    """
    return IMAGE_SIZES.get(platform, {}).get(format_type, (1080, 1080))

def get_all_sizes_for_platform(platform: str) -> dict:
    """Obtiene todos los tamaños disponibles para una plataforma"""
    return IMAGE_SIZES.get(platform, {})

def get_image_config(image_type: str) -> dict:
    """Obtiene configuración de procesamiento según tipo de imagen"""
    return IMAGE_TYPE_CONFIG.get(image_type, IMAGE_TYPE_CONFIG["producto"])

def get_image_prompt(image_type: str, language: str = "es-MX", **kwargs) -> str:
    """
    Genera prompt para generación de imagen
    
    Args:
        image_type: producto, servicio, logo
        language: es-MX, en
        **kwargs: Variables para el template (product_name, service_description, etc.)
        
    Returns:
        Prompt formateado
    """
    template = IMAGE_PROMPTS.get(language, IMAGE_PROMPTS["es-MX"]).get(image_type, "")
    return template.format(**kwargs)
