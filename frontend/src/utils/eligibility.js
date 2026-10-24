// Business rules from idea.md §3, mirrored on the client for display only.
// The backend planner stays the source of truth.

export const canShipCold = (w) =>
  w.refrigerated_storage_available && w.delivery_fleet === 'refrigerated'

export const stockOf = (warehouse, productId) =>
  warehouse.stock.find((s) => s.id_product === productId)?.quantity ?? 0

export const isBlocked = (warehouse, product) => product.need_refrigerator && !canShipCold(warehouse)

// Warehouses allowed to ship a product, and their combined stock.
export function eligibleStock(warehouses, product) {
  const sources = warehouses.filter((w) => stockOf(w, product.id) > 0 && !isBlocked(w, product))
  return {
    warehouses: sources,
    total: sources.reduce((sum, w) => sum + stockOf(w, product.id), 0),
  }
}

// Order lines that cannot be covered by eligible stock.
export function shortages(details, warehouses) {
  return details
    .map((d) => ({ ...d, available: eligibleStock(warehouses, d.product).total }))
    .filter((d) => d.available < d.quantity)
}
