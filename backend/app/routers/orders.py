from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.models import Order, OrderDetail, Product
from app.schemas import Objective, OrderIn, OrderOut, PlanOut, PlanRequest
from app.services import planner

router = APIRouter(prefix="/orders", tags=["orders"])

ORDER_LOAD_OPTIONS = (
    selectinload(Order.details).selectinload(OrderDetail.product),
    selectinload(Order.plans),
)


def _load_order(db: Session, id_order: int) -> Order:
    order = db.scalar(select(Order).where(Order.id == id_order).options(*ORDER_LOAD_OPTIONS))
    if order is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Order not found")
    return order


@router.get("", response_model=list[OrderOut])
def list_orders(db: Session = Depends(get_db)):
    return db.scalars(select(Order).options(*ORDER_LOAD_OPTIONS).order_by(Order.id.desc())).all()


@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderIn, db: Session = Depends(get_db)):
    if db.scalar(select(Order).where(Order.order_number == payload.order_number)):
        raise HTTPException(status.HTTP_409_CONFLICT, "Order number already exists")

    product_ids = [item.id_product for item in payload.items]
    if len(set(product_ids)) != len(product_ids):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Duplicate product in order")
    known = set(db.scalars(select(Product.id).where(Product.id.in_(product_ids))))
    if missing := set(product_ids) - known:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f"Unknown products: {sorted(missing)}")

    order = Order(
        order_number=payload.order_number,
        details=[OrderDetail(id_product=i.id_product, quantity=i.quantity) for i in payload.items],
    )
    db.add(order)
    db.commit()
    return _load_order(db, order.id)


@router.get("/{id_order}", response_model=OrderOut)
def get_order(id_order: int, db: Session = Depends(get_db)):
    return _load_order(db, id_order)


@router.delete("/{id_order}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(id_order: int, db: Session = Depends(get_db)):
    db.delete(_load_order(db, id_order))
    db.commit()


@router.get("/{id_order}/plans", response_model=list[PlanOut])
def list_plans(id_order: int, objective: Objective | None = None, db: Session = Depends(get_db)):
    _load_order(db, id_order)
    return planner.get_plans(db, id_order, objective)


@router.post("/{id_order}/plans", response_model=list[PlanOut])
def create_plans(id_order: int, payload: PlanRequest, db: Session = Depends(get_db)):
    _load_order(db, id_order)
    return planner.plan_order(db, id_order, payload.objective, payload.top_n, payload.ban_mode)
