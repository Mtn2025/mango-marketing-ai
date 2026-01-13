from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from io import BytesIO
from typing import Tuple, Optional, List
import os


class ImageCompositorService:
    """
    Servicio para composición y procesamiento avanzado de imágenes
    
    Features del Implementation Plan:
    - Detectar tipo de imagen (producto/servicio/logo)
    - Fusión de logos en esquinas
    - Watermarks personalizables
    - Resize y optimización
    - Efectos (esquinas redondeadas, glows)
    - Composiciones múltiples
    """
    
    def __init__(self):
        self.default_logo_position = "bottom-right"
        self.default_logo_opacity = 0.8
    
    async def detect_image_type(
        self,
        image_bytes: bytes,
        user_hint: Optional[str] = None
    ) -> str:
        """
        Detecta el tipo de imagen
        
        Args:
            image_bytes: Imagen en bytes
            user_hint: Hint del usuario ("producto", "servicio", "logo")
            
        Returns:
            Tipo detectado: "product", "service", "logo"
        """
        # Si el usuario dio hint, úsalo (del checkbox en frontend)
        if user_hint:
            type_mapping = {
                "producto": "product",
                "servicio": "service", 
                "logo": "logo"
            }
            return type_mapping.get(user_hint.lower(), "product")
        
        # Si no hay hint, hacer detección básica
        image = Image.open(BytesIO(image_bytes))
        width, height = image.size
        
        # Logos tienden a ser cuadrados y tienen transparencia
        has_alpha = image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info)
        aspect_ratio = width / height
        
        if has_alpha and 0.8 < aspect_ratio < 1.2:
            return "logo"
        
        # Por defecto, asumir producto
        return "product"
    
    async def resize_for_platform(
        self,
        image_bytes: bytes,
        platform: str,
        format_type: str = "cuadrado"
    ) -> bytes:
        """
        Redimensiona imagen según plataforma y formato
        
        Según implementation_plan.md líneas 459-487
        """
        image = Image.open(BytesIO(image_bytes))
        
        # Tamaños del plan
        sizes = {
            "facebook": {
                "feed": (1200, 630),
                "story": (1080, 1920),
                "cuadrado": (1080, 1080)
            },
            "instagram": {
                "cuadrado": (1080, 1080),
                "portrait": (1080, 1350),
                "story": (1080, 1920),
                "landscape": (1080, 566)
            },
            "tiktok": {
                "video": (1080, 1920),
                "thumbnail": (1080, 1920)
            },
            "linkedin": {
                "feed": (1200, 627),
                "story": (1080, 1920)
            },
            "whatsapp": {
                "status": (1080, 1920),
                "cuadrado": (1080, 1080)
            }
        }
        
        target_size = sizes.get(platform, {}).get(format_type, (1080, 1080))
        
        # Resize manteniendo aspect ratio y centrando
        image.thumbnail(target_size, Image.Resampling.LANCZOS)
        
        # Crear canvas con tamaño exacto
        canvas = Image.new('RGB', target_size, (255, 255, 255))
        
        # Centrar imagen
        offset = ((target_size[0] - image.size[0]) // 2,
                  (target_size[1] - image.size[1]) // 2)
        canvas.paste(image, offset)
        
        # Convertir a bytes
        output = BytesIO()
        canvas.save(output, format='JPEG', quality=95, optimize=True)
        return output.getvalue()
    
    async def add_logo_overlay(
        self,
        base_image_bytes: bytes,
        logo_bytes: bytes,
        position: str = "bottom-right",
        opacity: float = 0.8,
        size_percentage: float = 0.15
    ) -> bytes:
        """
        Fusiona logo en la imagen base
        
        Del implementation_plan.md: "logo se coloca en esquina"
        
        Args:
            base_image_bytes: Imagen principal
            logo_bytes: Logo a superponer
            position: "top-left", "top-right", "bottom-left", "bottom-right"
            opacity: 0.0 a 1.0
            size_percentage: Tamaño del logo relativo a la imagen base
        """
        base = Image.open(BytesIO(base_image_bytes)).convert('RGBA')
        logo = Image.open(BytesIO(logo_bytes)).convert('RGBA')
        
        # Calcular tamaño del logo
        base_width, base_height = base.size
        logo_target_width = int(base_width * size_percentage)
        
        # Resize logo manteniendo aspect ratio
        logo.thumbnail((logo_target_width, logo_target_width), Image.Resampling.LANCZOS)
        
        # Ajustar opacidad
        alpha = logo.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        logo.putalpha(alpha)
        
        # Calcular posición
        margin = int(base_width * 0.02)  # 2% de margen
        positions = {
            "top-left": (margin, margin),
            "top-right": (base_width - logo.size[0] - margin, margin),
            "bottom-left": (margin, base_height - logo.size[1] - margin),
            "bottom-right": (base_width - logo.size[0] - margin, base_height - logo.size[1] - margin)
        }
        
        pos = positions.get(position, positions["bottom-right"])
        
        # Superponer logo
        base.paste(logo, pos, logo)
        
        # Convertir a RGB y guardar
        final = base.convert('RGB')
        output = BytesIO()
        final.save(output, format='JPEG', quality=95)
        return output.getvalue()
    
    async def add_watermark(
        self,
        image_bytes: bytes,
        watermark_text: str,
        position: str = "bottom-center",
        font_size: int = 24,
        opacity: float = 0.5
    ) -> bytes:
        """
        Agrega watermark de texto
        """
        image = Image.open(BytesIO(image_bytes)).convert('RGBA')
        
        # Crear capa para texto
        txt_layer = Image.new('RGBA', image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_layer)
        
        # Intentar cargar fuente, si no, usar default
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Calcular posición del texto
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        margin = 20
        positions = {
            "bottom-center": ((image.size[0] - text_width) // 2, image.size[1] - text_height - margin),
            "bottom-right": (image.size[0] - text_width - margin, image.size[1] - text_height - margin),
            "bottom-left": (margin, image.size[1] - text_height - margin)
        }
        
        pos = positions.get(position, positions["bottom-center"])
        
        # Dibujar texto con opacidad
        text_color = (255, 255, 255, int(255 * opacity))
        draw.text(pos, watermark_text, font=font, fill=text_color)
        
        # Combinar capas
        watermarked = Image.alpha_composite(image, txt_layer)
        final = watermarked.convert('RGB')
        
        output = BytesIO()
        final.save(output, format='JPEG', quality=95)
        return output.getvalue()
    
    async def create_rounded_corners(
        self,
        image_bytes: bytes,
        radius: int = 50
    ) -> bytes:
        """
        Crea esquinas redondeadas
        """
        image = Image.open(BytesIO(image_bytes)).convert('RGBA')
        
        # Crear máscara para esquinas redondeadas
        mask = Image.new('L', image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), image.size], radius, fill=255)
        
        # Aplicar máscara
        rounded = Image.new('RGBA', image.size, (255, 255, 255, 0))
        rounded.paste(image, (0, 0), mask)
        
        output = BytesIO()
        rounded.save(output, format='PNG')
        return output.getvalue()
    
    async def apply_glow_effect(
        self,
        image_bytes: bytes,
        glow_radius: int = 10,
        glow_color: Tuple[int, int, int] = (255, 215, 0)  # Gold
    ) -> bytes:
        """
        Aplica efecto de brillo/glow
        """
        image = Image.open(BytesIO(image_bytes)).convert('RGBA')
        
        # Crear capa de glow
        glow = Image.new('RGBA', image.size, glow_color + (0,))
        glow.paste(image, (0, 0), image)
        
        # Aplicar blur para efecto glow
        for _ in range(3):
            glow = glow.filter(ImageFilter.GaussianBlur(glow_radius))
        
        # Combinar glow con imagen original
        result = Image.alpha_composite(glow, image)
        final = result.convert('RGB')
        
        output = BytesIO()
        final.save(output, format='JPEG', quality=95)
        return output.getvalue()
    
    async def create_carousel_images(
        self,
        images: List[bytes],
        platform: str = "instagram"
    ) -> List[bytes]:
        """
        Crea set de imágenes optimizadas para carousel
        
        Del implementation_plan.md: generación de carousels
        """
        carousel = []
        format_type = "cuadrado"  # Default para carousels
        
        for img_bytes in images[:10]:  # Máximo 10 imágenes
            resized = await self.resize_for_platform(img_bytes, platform, format_type)
            carousel.append(resized)
        
        return carousel
