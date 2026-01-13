from sqlalchemy import Column, String, Integer, Float, Boolean, Text, ARRAY, JSON, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.core.database import Base


class QualityLevel(str, enum.Enum):
    """Niveles de calidad del sistema"""
    RAPIDO = "rapido"  # Llama 4 Scout + Imagen 4 Fast
    PROFESIONAL = "profesional"  # GPT-5-mini + Imagen 4 Standard
    ELITE = "elite"  # Gemini 2.5 Flash + Flux-1.1-Pro


class ImageType(str, enum.Enum):
    """Tipos de imagen"""
    PRODUCT = "product"
    SERVICE = "service"
    LOGO = "logo"
    GENERATED = "generated"
    VARIANT = "variant"
    CAROUSEL_ITEM = "carousel_item"
    FUSED = "fused"
    WATERMARKED = "watermarked"


class Configuration(Base):
    """Configuración del usuario"""
    __tablename__ = "configurations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    language = Column(String(10), nullable=False, default="es-MX")  # 'es-MX' o 'en'
    quality_level = Column(Enum(QualityLevel), nullable=False, default=QualityLevel.RAPIDO)
    
    # LLM Provider
    llm_provider = Column(String(50))  # 'groq', 'google', 'azure'
    llm_model = Column(String(100))  # 'llama-4-scout', 'gemini-2.5-flash', etc.
    llm_api_key_encrypted = Column(Text)
    
    # Image Provider
    image_provider = Column(String(50))  # 'google', 'azure', 'replicate'
    image_model = Column(String(100))  # 'imagen-4-fast', 'flux-1.1-pro', etc.
    image_api_key_encrypted = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Product(Base):
    """Información del producto/servicio"""
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Información básica
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    
    # Precio (opcional)
    price = Column(Float)
    currency = Column(String(3))  # 'MXN', 'USD', etc.
    
    # Características
    key_features = Column(ARRAY(String))  # Array de características
    benefits = Column(ARRAY(String))  # Array de beneficios (máx 3)
    keywords = Column(ARRAY(String))  # Array de palabras clave
    
    # Público objetivo
    target_audience = Column(JSON)  # {"age": "25-35", "gender": "all", "interests": [...]}
    location = Column(String(255))  # Ubicación/región
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    generations = relationship("Generation", back_populates="product", cascade="all, delete-orphan")


class ProductImage(Base):
    """Imágenes del producto subidas por el usuario"""
    __tablename__ = "product_images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    
    image_type = Column(Enum(ImageType), nullable=False)
    file_path = Column(Text, nullable=False)
    file_size = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    product = relationship("Product", back_populates="images")


class Generation(Base):
    """Generación de contenido (copy + imágenes)"""
    __tablename__ = "generations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))
    
    # Plataformas para las que se generó
    platforms = Column(ARRAY(String))  # ['facebook', 'instagram', 'tiktok']
    
    # Configuración de copy
    tone = Column(String(50))  # 'formal', 'casual', 'juvenil', etc.
    length = Column(String(20))  # 'corto', 'medio', 'largo'
    use_emojis = Column(Boolean, default=False)
    cta = Column(String(255))  # Call to action
    
    # Configuración de imágenes
    image_options = Column(JSON)  # {"has_logo": true, "has_watermark": false, "variants": 3, etc.}
    
    # Modelos utilizados
    quality_level = Column(Enum(QualityLevel))
    llm_used = Column(String(100))
    image_model_used = Column(String(100))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    product = relationship("Product", back_populates="generations")
    copies = relationship("Copy", back_populates="generation", cascade="all, delete-orphan")
    images = relationship("GeneratedImage", back_populates="generation", cascade="all, delete-orphan")
    history_entries = relationship("History", back_populates="generation", cascade="all, delete-orphan")


class Copy(Base):
    """Copy generado por IA"""
    __tablename__ = "copies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    generation_id = Column(UUID(as_uuid=True), ForeignKey("generations.id"), nullable=False)
    
    platform = Column(String(50))  # 'facebook', 'instagram', etc.
    variant_number = Column(Integer)  # 1, 2, 3 (si se generan variantes)
    copy_text = Column(Text, nullable=False)
    
    is_favorite = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    generation = relationship("Generation", back_populates="copies")


class GeneratedImage(Base):
    """Imágenes generadas por IA"""
    __tablename__ = "generated_images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    generation_id = Column(UUID(as_uuid=True), ForeignKey("generations.id"), nullable=False)
    
    image_type = Column(Enum(ImageType), nullable=False)
    platform = Column(String(50))  # 'facebook', 'instagram', etc.
    
    file_path = Column(Text, nullable=False)
    width = Column(Integer)
    height = Column(Integer)
    
    variant_number = Column(Integer)  # Si es variante
    processing_options = Column(JSON)  # {has_logo, has_watermark, carousel_position, etc.}
    
    is_favorite = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    generation = relationship("Generation", back_populates="images")


class History(Base):
    """Historial de acciones para edición/regeneración"""
    __tablename__ = "history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    generation_id = Column(UUID(as_uuid=True), ForeignKey("generations.id"), nullable=False)
    
    action = Column(String(50))  # 'generated', 'edited', 'regenerated', 'exported'
    request_metadata = Column(JSON)  # Información adicional de la acción (renombrado de 'metadata' para evitar conflicto con SQLAlchemy)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    generation = relationship("Generation", back_populates="history")
