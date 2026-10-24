from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import PreviewIn, PreviewOut, PreviewPlanOut
from app.services import planner

router = APIRouter(prefix="/plans", tags=["plans"])


@router.post("/preview", response_model=PreviewOut)
def preview_plan(payload: PreviewIn, db: Session = Depends(get_db)):
    """Best plan per objective for an unsaved order. Nothing is stored."""
    ordered = {item.id_product: item.quantity for item in payload.items}
    if len(ordered) != len(payload.items):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Duplicate product in order")

    best: dict[str, PreviewPlanOut | None] = {}
    for objective in ("min_max_distance", "min_vans"):
        results = planner.solve(db, ordered, objective, top_n=1)
        best[objective] = (
            PreviewPlanOut(
                max_distance=results[0].max_distance,
                vans_used=results[0].vans_used,
                warehouse_ids=sorted({w for w, _ in results[0].shipments}),
            )
            if results
            else None
        )
    return PreviewOut(feasible=best["min_max_distance"] is not None, **best)
