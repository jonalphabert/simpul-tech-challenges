export const OBJECTIVES = {
  A: {
    key: 'min_max_distance',
    label: 'Jarak terjauh minimum',
    hint: 'Opsi A meminimalkan jarak gudang terjauh (semua van berangkat bersamaan), seri dipecah dengan jumlah van.',
  },
  B: {
    key: 'min_vans',
    label: 'Van paling sedikit',
    hint: 'Opsi B meminimalkan jumlah van (= jumlah gudang), seri dipecah dengan jarak terjauh.',
  },
}

export const objectiveLetter = (value) => (value === 'B' ? 'B' : 'A')

export const plansFor = (plans, letter) =>
  plans.filter((p) => p.objective === OBJECTIVES[letter].key && p.status === 'feasible')

// One van per warehouse: group a plan's lines by warehouse, nearest first.
export function vansOf(plan) {
  const byWarehouse = new Map()
  for (const d of plan.details) {
    if (!byWarehouse.has(d.id_warehouse)) byWarehouse.set(d.id_warehouse, { warehouse: d.warehouse, lines: [] })
    byWarehouse.get(d.id_warehouse).lines.push(d)
  }
  return [...byWarehouse.values()].sort((a, b) => a.warehouse.distance - b.warehouse.distance)
}

export const warehouseKey = (plan) => vansOf(plan).map((v) => v.warehouse.id).join(',')

export const totalDistance = (plan) => vansOf(plan).reduce((sum, v) => sum + v.warehouse.distance, 0)

// Order status from its saved plans: null when it has not been planned yet.
export function orderStatus(plans) {
  if (!plans.length) return null
  return plans.some((p) => p.status === 'feasible') ? 'feasible' : 'infeasible'
}
