"""ORM models mirroring database/schema.sql."""

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    category: Mapped[str] = mapped_column(String(50))
    need_refrigerator: Mapped[bool] = mapped_column(Boolean, default=False)


class Warehouse(Base):
    __tablename__ = "warehouse"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(10), unique=True)
    location: Mapped[str] = mapped_column(String(100))
    distance: Mapped[int] = mapped_column(Integer)
    refrigerated_storage_available: Mapped[bool] = mapped_column(Boolean, default=False)
    delivery_fleet: Mapped[str] = mapped_column(String(20))

    stock: Mapped[list["WarehouseStock"]] = relationship(back_populates="warehouse")


class WarehouseStock(Base):
    __tablename__ = "warehouse_stock"

    id_warehouse: Mapped[int] = mapped_column(ForeignKey("warehouse.id"), primary_key=True)
    id_product: Mapped[int] = mapped_column(ForeignKey("product.id"), primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer)

    warehouse: Mapped[Warehouse] = relationship(back_populates="stock")
    product: Mapped[Product] = relationship()


class Order(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_number: Mapped[str] = mapped_column(String(50), unique=True)

    details: Mapped[list["OrderDetail"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )
    plans: Mapped[list["OrderPlan"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )

    @property
    def best_plan(self) -> "OrderPlan | None":
        """Rank-1 plan of Option A, shown as the order's headline result."""
        return next(
            (p for p in self.plans if p.objective == "min_max_distance" and p.rank == 1), None
        )


class OrderDetail(Base):
    __tablename__ = "order_detail"

    id_order: Mapped[int] = mapped_column(ForeignKey("order.id"), primary_key=True)
    id_product: Mapped[int] = mapped_column(ForeignKey("product.id"), primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer)

    order: Mapped[Order] = relationship(back_populates="details")
    product: Mapped[Product] = relationship()


class OrderPlan(Base):
    __tablename__ = "order_plan"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_order: Mapped[int] = mapped_column(ForeignKey("order.id"))
    objective: Mapped[str] = mapped_column(String(20))
    rank: Mapped[int] = mapped_column(Integer)
    max_distance: Mapped[int | None] = mapped_column(Integer, nullable=True)
    vans_used: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(20))

    order: Mapped[Order] = relationship(back_populates="plans")
    details: Mapped[list["OrderPlanDetail"]] = relationship(
        back_populates="plan", cascade="all, delete-orphan"
    )


class OrderPlanDetail(Base):
    __tablename__ = "order_plan_detail"

    id_order_plan: Mapped[int] = mapped_column(ForeignKey("order_plan.id"), primary_key=True)
    id_warehouse: Mapped[int] = mapped_column(ForeignKey("warehouse.id"), primary_key=True)
    id_product: Mapped[int] = mapped_column(ForeignKey("product.id"), primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer)

    plan: Mapped[OrderPlan] = relationship(back_populates="details")
    warehouse: Mapped[Warehouse] = relationship()
    product: Mapped[Product] = relationship()
