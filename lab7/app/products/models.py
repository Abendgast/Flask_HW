from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, ForeignKey, Boolean
from typing import List


class Category(db.Model):
    __tablename__ = 'categories'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    
    products: Mapped[List["Product"]] = relationship(back_populates="category")
    
    def __repr__(self):
        return f'<Category {self.name}>'


class Product(db.Model):
    __tablename__ = 'products'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    category: Mapped["Category"] = relationship(back_populates="products")
    
    def __repr__(self):
        return f'<Product {self.name}>'
