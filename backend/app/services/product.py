from typing import Optional, List
from sqlalchemy.orm import Session
from app.db.models import Product, ProductImage, ImageType
import uuid


class ProductService:
    """
    Servicio para manejar productos
    """
    
    def create_product(
        self,
        db: Session,
        name: str,
        description: Optional[str] = None,
        category: Optional[str] = None,
        price: Optional[float] = None,
        currency: Optional[str] = "MXN",
        key_features: Optional[List[str]] = None,
        benefits: Optional[List[str]] = None,
        keywords: Optional[List[str]] = None,
        target_audience: Optional[dict] = None,
        location: Optional[str] = None,
    ) -> Product:
        """
        Crea un nuevo producto
        """
        product = Product(
            id=uuid.uuid4(),
            name=name,
            description=description,
            category=category,
            price=price,
            currency=currency,
            key_features=key_features,
            benefits=benefits,
            keywords=keywords,
            target_audience=target_audience,
            location=location,
        )
        
        db.add(product)
        db.commit()
        db.refresh(product)
        
        return product
    
    def get_product(self, db: Session, product_id: str) -> Optional[Product]:
        """
        Obtiene un producto por ID
        """
        return db.query(Product).filter(Product.id == product_id).first()
    
    def list_products(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 20
    ) -> List[Product]:
        """
        Lista productos con paginación
        """
        return db.query(Product)\
            .order_by(Product.created_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
    
    def update_product(
        self,
        db: Session,
        product_id: str,
        **kwargs
    ) -> Optional[Product]:
        """
        Actualiza un producto
        """
        product = self.get_product(db, product_id)
        if not product:
            return None
        
        for key, value in kwargs.items():
            if hasattr(product, key) and value is not None:
                setattr(product, key, value)
        
        db.commit()
        db.refresh(product)
        
        return product
    
    def delete_product(self, db: Session, product_id: str) -> bool:
        """
        Elimina un producto
        """
        product = self.get_product(db, product_id)
        if not product:
            return False
        
        db.delete(product)
        db.commit()
        
        return True
    
    def add_product_image(
        self,
        db: Session,
        product_id: str,
        file_path: str,
        image_type: ImageType,
        width: Optional[int] = None,
        height: Optional[int] = None,
        file_size: Optional[int] = None,
    ) -> Optional[ProductImage]:
        """
        Agrega una imagen al producto
        """
        product = self.get_product(db, product_id)
        if not product:
            return None
        
        image = ProductImage(
            id=uuid.uuid4(),
            product_id=product.id,
            image_type=image_type,
            file_path=file_path,
            width=width,
            height=height,
            file_size=file_size,
        )
        
        db.add(image)
        db.commit()
        db.refresh(image)
        
        return image
