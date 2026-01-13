"""
Templates de copy por plataforma e idioma

Del implementation_plan.md líneas 259-260, 373-455
"""

COPY_TEMPLATES = {
    "es-MX": {
        "facebook": {
            "structure": "{hook}\n\n{body}\n\n{benefits}\n\n{cta}",
            "hooks": [
                "🔥 ¡No te lo puedes perder!",
                "✨ Descubre {product_name}",
                "💡 ¿Buscas {category}?",
                "🎯 La solución que necesitabas"
            ],
            "ctas": [
                "👉 Compra ahora",
                "📲 Contáctanos",
                "🛒 Aprovecha la oferta",
                "💬 Envíanos mensaje"
            ]
        },
        "instagram": {
            "structure": "{hook}\n.\n{body}\n.\n{benefits}\n.\n{hashtags}\n.\n{cta}",
            "hooks": [
                "✨ Nuevo en Instagram",
                "🔥 Te va a encantar",
                "💫 Descubre {product_name}",
                "⚡ Llegó lo que esperabas"
            ],
            "ctas": [
                "🔗 Link en bio",
                "📩 DM para más info",
                "💕 Guarda este post",
                "👆 Toca para ordenar"
            ]
        },
        "tiktok": {
            "structure": "{hook} {body} {cta} {hashtags}",
            "hooks": [
                "🎵 Atención TikTokers:",
                "⚡ Viral alert:",
                "🔥 Esto SÍ funciona:",
                "💯 Real no fake:"
            ],
            "ctas": [
                "🔗 Link en bio para ordenar",
                "💬 Comenta TU EXPERIENCIA",
                "🔁 Comparte con quien lo necesite",
                "❤️ Like si te late"
            ]
        },
        "linkedin": {
            "structure": "{hook}\n\n{body}\n\n{benefits}\n\n{cta}",
            "hooks": [
                "📊 Innovación en {category}:",
                "💼 Profesionales atentos:",
                "🎯 Solución empresarial:",
                "🚀 Optimiza tu negocio:"
            ],
            "ctas": [
                "📧 Contáctanos para más información",
                "🔗 Visita nuestro sitio web",
                "📞 Agenda una demo",
                "💡 Descarga el caso de estudio"
            ]
        },
        "whatsapp": {
            "structure": "{hook}\n\n{body}\n\n{benefits}\n\n{cta}",
            "hooks": [
                "¡Hola! 👋",
                "Buenos días ☀️",
                "Tenemos algo especial para ti 🎁",
                "Noticia importante 📢"
            ],
            "ctas": [
                "💬 Responde este mensaje para ordenar",
                "📲 Llámanos al [NÚMERO]",
                "🛒 Catálogo completo: [LINK]",
                "✅ Confirma tu pedido aquí"
            ]
        }
    },
    "en": {
        "facebook": {
            "structure": "{hook}\n\n{body}\n\n{benefits}\n\n{cta}",
            "hooks": [
                "🔥 Don't miss out!",
                "✨ Discover {product_name}",
                "💡 Looking for {category}?",
                "🎯 The solution you need"
            ],
            "ctas": [
                "👉 Shop now",
                "📲 Contact us",
                "🛒 Get the deal",
                "💬 Send us a message"
            ]
        },
        "instagram": {
            "structure": "{hook}\n.\n{body}\n.\n{benefits}\n.\n{hashtags}\n.\n{cta}",
            "hooks": [
                "✨ New on Instagram",
                "🔥 You'll love this",
                "💫 Discover {product_name}",
                "⚡ What you've been waiting for"
            ],
            "ctas": [
                "🔗 Link in bio",
                "📩 DM for details",
                "💕 Save this post",
                "👆 Tap to order"
            ]
        },
        "tiktok": {
            "structure": "{hook} {body} {cta} {hashtags}",
            "hooks": [
                "🎵 TikTokers listen up:",
                "⚡ Viral alert:",
                "🔥 This actually works:",
                "💯 No cap:"
            ],
            "ctas": [
                "🔗 Link in bio to order",
                "💬 Comment YOUR EXPERIENCE",
                "🔁 Share with who needs this",
                "❤️ Like if you vibe"
            ]
        },
        "linkedin": {
            "structure": "{hook}\n\n{body}\n\n{benefits}\n\n{cta}",
            "hooks": [
                "📊 Innovation in {category}:",
                "💼 Professionals take note:",
                "🎯 Business solution:",
                "🚀 Optimize your operations:"
            ],
            "ctas": [
                "📧 Contact us for more info",
                "🔗 Visit our website",
                "📞 Schedule a demo",
                "💡 Download the case study"
            ]
        },
        "whatsapp": {
            "structure": "{hook}\n\n{body}\n\n{benefits}\n\n{cta}",
            "hooks": [
                "Hi there! 👋",
                "Good morning ☀️",
                "We have something special for you 🎁",
                "Important news 📢"
            ],
            "ctas": [
                "💬 Reply to this message to order",
                "📲 Call us at [NUMBER]",
                "🛒 Full catalog: [LINK]",
                "✅ Confirm your order here"
            ]
        }
    }
}

# Tonos disponibles (del plan líneas 373-391)
TONES = {
    "es-MX": {
        "formal": "Formal y profesional",
        "casual": "Casual y amigable",
        "juvenil": "Juvenil y moderno",
        "entusiasta": "Entusiasta y motivador",
        "elegante": "Elegante y sofisticado",
        "humoristico": "Con toque de humor"
    },
    "en": {
        "formal": "Formal and professional",
        "casual": "Casual and friendly",
        "youthful": "Youthful and trendy",
        "enthusiastic": "Enthusiastic and motivating",
        "elegant": "Elegant and sophisticated",
        "humorous": "With a touch of humor"
    }
}

# Longitudes por plataforma (del plan líneas 427-454)
PLATFORM_COPY_LIMITS = {
    "facebook": {
        "corto": 125,
        "medio": 250,
        "largo": 500
    },
    "instagram": {
        "corto": 150,
        "medio": 300,
        "largo": 2200
    },
    "tiktok": {
        "corto": 80,
        "medio": 150,
        "largo": 300
    },
    "linkedin": {
        "corto": 150,
        "medio": 500,
        "largo": 1300
    },
    "whatsapp": {
        "corto": 100,
        "medio": 200,
        "largo": 500
    }
}

def get_template(platform: str, language: str = "es-MX") -> dict:
    """Obtiene template para plataforma e idioma"""
    return COPY_TEMPLATES.get(language, COPY_TEMPLATES["es-MX"]).get(platform, {})

def get_copy_limit(platform: str, length: str = "medio") -> int:
    """Obtiene límite de caracteres para plataforma"""
    return PLATFORM_COPY_LIMITS.get(platform, {}).get(length, 250)
