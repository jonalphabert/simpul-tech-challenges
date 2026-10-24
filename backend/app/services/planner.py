"""Delivery planner: idea.md section 5.

1. Query candidate warehouses for every ordered product.
2. Build a CP-SAT model.
3. Solve it repeatedly, banning each found warehouse set, to get the top N plans.
4. Save the plans into order_plan / order_plan_detail.
"""

from collections import defaultdict
from dataclasses import dataclass, field

from ortools.sat.python import cp_model
from sqlalchemy import delete, select, text
from sqlalchemy.orm import Session, selectinload

from app.models import OrderDetail, OrderPlan, OrderPlanDetail
from app.schemas import BanMode, Objective

SOLVER_TIME_LIMIT_SECONDS = 10.0

# Same filter as idea.md Step 1, keyed by product ids so it also serves
# previews of orders that are not saved yet.
CANDIDATE_SQL = text("""
    SELECT ws.id_product,
           w.id        AS id_warehouse,
           w.distance,
           ws.quantity AS stock_qty
    FROM warehouse_stock ws
    JOIN product p   ON p.id = ws.id_product
    JOIN warehouse w ON w.id = ws.id_warehouse
    WHERE ws.id_product = ANY(:product_ids)
      AND ws.quantity > 0
      AND (
            p.need_refrigerator = FALSE
         OR (w.refrigerated_storage_available = TRUE AND w.delivery_fleet = 'refrigerated')
      )
""")


@dataclass
class Candidate:
    id_product: int
    id_warehouse: int
    distance: int
    stock_qty: int


@dataclass
class PlanResult:
    max_distance: int
    vans_used: int
    # (id_warehouse, id_product) -> quantity shipped
    shipments: dict[tuple[int, int], int] = field(default_factory=dict)


# Step 1 ---------------------------------------------------------------------

def fetch_order_quantities(db: Session, id_order: int) -> dict[int, int]:
    rows = db.scalars(select(OrderDetail).where(OrderDetail.id_order == id_order))
    return {row.id_product: row.quantity for row in rows}


def fetch_candidates(db: Session, product_ids: list[int]) -> list[Candidate]:
    rows = db.execute(CANDIDATE_SQL, {"product_ids": product_ids}).mappings()
    return [Candidate(**row) for row in rows]


def is_feasible(ordered: dict[int, int], candidates: list[Candidate]) -> bool:
    """Every product needs at least one candidate and enough total candidate stock."""
    available: dict[int, int] = defaultdict(int)
    for c in candidates:
        available[c.id_product] += c.stock_qty
    return all(available[p] >= qty for p, qty in ordered.items())


# Steps 2 + 3 ----------------------------------------------------------------

def solve_top_n(
    ordered: dict[int, int],
    candidates: list[Candidate],
    objective: Objective,
    top_n: int,
    ban_mode: BanMode,
) -> list[PlanResult]:
    model = cp_model.CpModel()

    distance = {c.id_warehouse: c.distance for c in candidates}
    max_possible_distance = max(distance.values())

    use = {w: model.new_bool_var(f"use_{w}") for w in distance}
    qty: dict[tuple[int, int], cp_model.IntVar] = {}
    upper: dict[tuple[int, int], int] = {}
    for c in candidates:
        key = (c.id_warehouse, c.id_product)
        upper[key] = min(c.stock_qty, ordered[c.id_product])  # constraint 1: stock limit
        qty[key] = model.new_int_var(0, upper[key], f"qty_{c.id_warehouse}_{c.id_product}")

    # Constraint 2: full delivery of every product.
    for p, ordered_qty in ordered.items():
        model.add(sum(v for (_, pp), v in qty.items() if pp == p) == ordered_qty)

    # Constraint 3: shipping anything needs the warehouse's van.
    for (w, p), v in qty.items():
        model.add(v <= upper[w, p] * use[w])

    # Constraint 4: a used warehouse must ship something.
    for w in use:
        model.add(sum(v for (ww, _), v in qty.items() if ww == w) >= use[w])

    # Constraint 5: maxDist covers every used warehouse.
    max_dist = model.new_int_var(0, max_possible_distance, "max_dist")
    for w, d in distance.items():
        model.add(max_dist >= d * use[w])

    vans = sum(use.values())
    if objective == "min_max_distance":
        # Option A: minimize maxDist, tie-break on fewest vans.
        main = max_dist * (len(use) + 1) + vans
    else:
        # Option B: minimize vans, tie-break on smallest maxDist.
        main = vans * (max_possible_distance + 1) + max_dist

    # Last tie-breaker: total unit-km, so each product ships from the closest
    # van that is already going instead of an arbitrary split between vans.
    unit_km = sum(distance[w] * v for (w, _), v in qty.items())
    max_unit_km = sum(distance[w] * ub for (w, _), ub in upper.items())
    model.minimize(main * (max_unit_km + 1) + unit_km)

    plans: list[PlanResult] = []
    while len(plans) < top_n:
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = SOLVER_TIME_LIMIT_SECONDS
        status = solver.solve(model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            break

        used = {w for w, var in use.items() if solver.value(var)}
        shipments = {key: solver.value(v) for key, v in qty.items() if solver.value(v) > 0}
        plans.append(
            PlanResult(
                max_distance=max(distance[w] for w in used),
                vans_used=len(used),
                shipments=shipments,
            )
        )

        # Ban this warehouse combination for the next iteration.
        if ban_mode == "exact":
            model.add(
                sum(use[w] for w in used) - sum(use[w] for w in use if w not in used)
                <= len(used) - 1
            )
        else:
            model.add(sum(use[w] for w in used) <= len(used) - 1)

    return plans


def solve(
    db: Session,
    ordered: dict[int, int],
    objective: Objective,
    top_n: int,
    ban_mode: BanMode = "superset",
) -> list[PlanResult]:
    """Steps 1-3 for a {product id: quantity} order. An empty list means infeasible."""
    candidates = fetch_candidates(db, list(ordered))
    if not candidates or not is_feasible(ordered, candidates):
        return []
    return solve_top_n(ordered, candidates, objective, top_n, ban_mode)


# Step 4 ---------------------------------------------------------------------

def plan_order(
    db: Session,
    id_order: int,
    objective: Objective,
    top_n: int = 5,
    ban_mode: BanMode = "superset",
) -> list[OrderPlan]:
    """Run the planner for one objective and replace any plans saved for it before."""
    db.execute(
        delete(OrderPlan).where(OrderPlan.id_order == id_order, OrderPlan.objective == objective)
    )

    results = solve(db, fetch_order_quantities(db, id_order), objective, top_n, ban_mode)

    if not results:
        db.add(OrderPlan(id_order=id_order, objective=objective, rank=1, status="infeasible"))
    for rank, result in enumerate(results, start=1):
        db.add(
            OrderPlan(
                id_order=id_order,
                objective=objective,
                rank=rank,
                max_distance=result.max_distance,
                vans_used=result.vans_used,
                status="feasible",
                details=[
                    OrderPlanDetail(id_warehouse=w, id_product=p, quantity=q)
                    for (w, p), q in result.shipments.items()
                ],
            )
        )
    db.commit()

    return get_plans(db, id_order, objective)


def get_plans(db: Session, id_order: int, objective: Objective | None = None) -> list[OrderPlan]:
    query = (
        select(OrderPlan)
        .where(OrderPlan.id_order == id_order)
        .options(
            selectinload(OrderPlan.details).selectinload(OrderPlanDetail.warehouse),
            selectinload(OrderPlan.details).selectinload(OrderPlanDetail.product),
        )
        .order_by(OrderPlan.objective, OrderPlan.rank)
    )
    if objective:
        query = query.where(OrderPlan.objective == objective)
    return list(db.scalars(query))
