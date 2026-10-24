from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Objective = Literal["min_max_distance", "min_vans"]
BanMode = Literal["exact", "superset"]


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ProductOut(ORMModel):
    id: int
    name: str
    category: str
    need_refrigerator: bool


class StockOut(ORMModel):
    id_product: int
    quantity: int
    product: ProductOut


class WarehouseOut(ORMModel):
    id: int
    code: str
    location: str
    distance: int
    refrigerated_storage_available: bool
    delivery_fleet: str
    stock: list[StockOut]


class OrderItemIn(BaseModel):
    id_product: int
    quantity: int = Field(gt=0)


class OrderIn(BaseModel):
    order_number: str = Field(min_length=1, max_length=50)
    items: list[OrderItemIn] = Field(min_length=1)


class OrderDetailOut(ORMModel):
    id_product: int
    quantity: int
    product: ProductOut


class PlanSummaryOut(ORMModel):
    status: str
    max_distance: int | None
    vans_used: int | None


class OrderOut(ORMModel):
    id: int
    order_number: str
    details: list[OrderDetailOut]
    best_plan: PlanSummaryOut | None


class PlanRequest(BaseModel):
    objective: Objective
    top_n: int = Field(default=5, ge=1, le=20)
    ban_mode: BanMode = "superset"


class WarehouseRef(ORMModel):
    id: int
    code: str
    location: str
    distance: int
    delivery_fleet: str


class PlanDetailOut(ORMModel):
    id_warehouse: int
    id_product: int
    quantity: int
    warehouse: WarehouseRef
    product: ProductOut


class PreviewIn(BaseModel):
    items: list[OrderItemIn] = Field(min_length=1)


class PreviewPlanOut(BaseModel):
    max_distance: int
    vans_used: int
    warehouse_ids: list[int]


class PreviewOut(BaseModel):
    feasible: bool
    min_max_distance: PreviewPlanOut | None
    min_vans: PreviewPlanOut | None


class PlanOut(ORMModel):
    id: int
    id_order: int
    objective: Objective
    rank: int
    max_distance: int | None
    vans_used: int | None
    status: str
    details: list[PlanDetailOut]
