from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.product import ProductService
from app.db.models import ImageType

router = APIRouter()
product_service = ProductService()


class CreateProductRequest(BaseModel):
    """Request para crear producto"""
    name: str = Field(..., description="Nombre del producto")
    description: Optional[str] = Field(None, description="Descripción")
    category: Optional[str] = Field(None, description="Categoría")
    price: Optional[float] = Field(None, description="Precio")
    currency: Optional[str] = Field("MXN", description="Moneda")
    key_features: Optional[List[str]] = Field(None, description="Características clave")
    benefits: Optional[List[str]] = Field(None, description="Beneficios")
    keywords: Optional[List[str]] = Field(None, description="Palabras clave")
    target_audience: Optional[dict] = Field(None, description="Público objetivo")
    location: Optional[str] = Field(None, description="Ubicación")


class ProductResponse(BaseModel):
    """Response con info del producto"""
    id: str
    name: str
    description: Optional[str]
    category: Optional[str]
    price: Optional[float]
    currency: Optional[str]
    key_features: Optional[List[str]]
    benefits: Optional[List[str]]
    keywords: Optional[List[str]]
    
    class Config:
        from_attributes = True


@router.post("/products", response_model=ProductResponse)
async def create_product(
    request: CreateProductRequest,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo producto
    
    ## Ejemplo:
    ```json
    {
      "name": "Café Artesanal Oaxaqueño",
      "description": "Café de altura...",
      "category": "Alimentos",
      "price": 250.00,
      "currency": "MXN",
      "benefits": ["100% orgánico", "Sabor único"],
      "keywords": ["café", "artesanal", "oaxaca"]
    }
    ```
    """
    try:
        product = product_service.create_product(
            db=db,
            name=request.name,
            description=request.description,
            category=request.category,
            price=request.price,
            currency=request.currency,
            key_features=request.key_features,
            benefits=request.benefits,
            keywords=request.keywords,
            target_audience=request.target_audience,
            location=request.location,
        )
        
        return ProductResponse(
            id=str(product.id),
            name=product.name,
            description=product.description,
            category=product.category,
            price=product.price,
            currency=product.currency,
            key_features=product.key_features,
            benefits=product.benefits,
            keywords=product.keywords,
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: str,
    db: Session = Depends(get_db)
):
    """Obtiene un producto por ID"""
    product = product_service.get_product(db, product_id)
    
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    return ProductResponse(
        id=str(product.id),
        name=product.name,
        description=product.description,
        category=product.category,
        price=product.price,
        currency=product.currency,
        key_features=product.key_features,
        benefits=product.benefits,
        keywords=product.keywords,
    )


@router.get("/products", response_model=List[ProductResponse])
async def list_products(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Lista productos con paginación"""
    products = product_service.list_products(db, skip, limit)
    
    return [
        ProductResponse(
            id=str(p.id),
            name=p.name,
            description=p.description,
            category=p.category,
            price=p.price,
            currency=p.currency,
            key_features=p.key_features,
            benefits=p.benefits,
            keywords=p.keywords,
        )
        for p in products
    ]


@router.delete("/products/{product_id}")
async def delete_product(
    product_id: str,
    db: Session = Depends(get_db)
):
    """Elimina un producto"""
    success = product_service.delete_product(db, product_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    return {"message": "Producto eliminado exitosamente"}
