import zipfile
from io import BytesIO
from typing import Dict, List, Optional
import json
from datetime import datetime


class ExportService:
    """
    Servicio para exportar contenido generado
    
    Del implementation_plan.md:
    - Exportar ZIP con imágenes + copy
    - Copiar copy al portapapeles
    - Optimización para compartir
    """
    
    async def create_export_package(
        self,
        copy_data: Dict[str, str],  # {platform: copy_text}
        images: Dict[str, List[bytes]],  # {platform: [image1, image2, ...]}
        product_name: str,
        metadata: Optional[Dict] = None
    ) -> bytes:
        """
        Crea paquete ZIP con todo el contenido
        
        Estructura:
        package.zip/
        ├── README.txt
        ├── copy/
        │   ├── facebook.txt
        │   ├── instagram.txt
        │   └── ...
        ├── images/
        │   ├── facebook/
        │   │   ├── feed_1.jpg
        │   │   └── story_1.jpg
        │   ├── instagram/
        │   │   ├── cuadrado_1.jpg
        │   │   └── portrait_1.jpg
        │   └── ...
        └── metadata.json
        """
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # README
            readme = self._generate_readme(product_name, list(copy_data.keys()))
            zip_file.writestr('README.txt', readme)
            
            # Copy files
            for platform, copy_text in copy_data.items():
                zip_file.writestr(f'copy/{platform}.txt', copy_text)
            
            # Images
            for platform, img_list in images.items():
                for idx, img_bytes in enumerate(img_list, 1):
                    zip_file.writestr(
                        f'images/{platform}/image_{idx}.jpg',
                        img_bytes
                    )
            
            # Metadata
            meta = {
                "product_name": product_name,
                "generated_at": datetime.utcnow().isoformat(),
                "platforms": list(copy_data.keys()),
                "total_images": sum(len(imgs) for imgs in images.values()),
                **(metadata or {})
            }
            zip_file.writestr('metadata.json', json.dumps(meta, indent=2))
        
        zip_buffer.seek(0)
        return zip_buffer.getvalue()
    
    def _generate_readme(self, product_name: str, platforms: List[str]) -> str:
        """
        Genera README.txt para el package
        """
        return f"""🥭 MANGO MARKETING AI - EXPORT PACKAGE
=====================================

Producto: {product_name}
Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}
Plataformas: {', '.join(platforms)}

📁 ESTRUCTURA:
--------------
copy/           → Textos de marketing por plataforma
images/         → Imágenes optimizadas por plataforma
metadata.json   → Información adicional de la generación

📝 CÓMO USAR:
-------------
1. Navega a la carpeta "copy" para ver los textos
2. Copia el texto de la plataforma que necesites
3. Usa las imágenes correspondientes de la carpeta "images"
4. Publica en tus redes sociales

💡 TIPS:
--------
- Los textos ya están optimizados para cada plataforma
- Las imágenes tienen el tamaño correcto para cada red
- Revisa metadata.json para información técnica

¿Necesitas regenerar? Vuelve a Mango Marketing AI.

---
Generado con ❤️ por Mango Marketing AI
https://mango.ubrokers.mx
"""
    
    async def create_single_platform_export(
        self,
        platform: str,
        copy_text: str,
        images: List[bytes]
    ) -> bytes:
        """
        Exporta contenido de una sola plataforma
        """
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Copy
            zip_file.writestr(f'{platform}_copy.txt', copy_text)
            
            # Images
            for idx, img_bytes in enumerate(images, 1):
                zip_file.writestr(f'{platform}_image_{idx}.jpg', img_bytes)
        
        zip_buffer.seek(0)
        return zip_buffer.getvalue()
    
    def format_for_clipboard(
        self,
        copy_text: str,
        include_hashtags: bool = True,
        hashtags: Optional[List[str]] = None
    ) -> str:
        """
        Formatea copy para copiar al portapapeles
        """
        formatted = copy_text.strip()
        
        if include_hashtags and hashtags:
            formatted += "\n\n" + " ".join(f"#{tag}" for tag in hashtags)
        
        return formatted
    
    def generate_share_urls(
        self,
        copy_text: str,
        platform: str
    ) -> Dict[str, str]:
        """
        Genera URLs para compartir directo en redes
        (pre-pobladas con el copy)
        """
        from urllib.parse import quote
        
        encoded_text = quote(copy_text[:280])  # Límite seguro
        
        urls = {
            "facebook": f"https://www.facebook.com/sharer/sharer.php?quote={encoded_text}",
            "twitter": f"https://twitter.com/intent/tweet?text={encoded_text}",
            "linkedin": f"https://www.linkedin.com/sharing/share-offsite/?url=&summary={encoded_text}",
            "whatsapp": f"https://api.whatsapp.com/send?text={encoded_text}"
        }
        
        return {platform: urls.get(platform)} if platform in urls else {}
