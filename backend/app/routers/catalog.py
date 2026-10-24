from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.models import Product, Warehouse, WarehouseStock
from app.schemas import ProductOut, WarehouseOut

router = APIRouter(tags=["catalog"])


@router.get("/products", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.scalars(select(Product).order_by(Product.id)).all()


@router.get("/warehouses", response_model=list[WarehouseOut])
def list_warehouses(db: Session = Depends(get_db)):
    query = (
        select(Warehouse)
        .options(selectinload(Warehouse.stock).selectinload(WarehouseStock.product))
        .order_by(Warehouse.code)
    )
    return db.scalars(query).all()
