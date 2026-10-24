import { http } from './http'

export const OBJECTIVE_KEYS = ['min_max_distance', 'min_vans']

export const planService = {
  list: (orderId) => http.get(`/orders/${orderId}/plans`),

  run: (orderId, { objective, topN = 5 }) =>
    http.post(`/orders/${orderId}/plans`, { objective, top_n: topN, ban_mode: 'superset' }),

  // Plans both objectives (A and B) so they can be compared.
  async runAll(orderId, { topN = 5 } = {}) {
    for (const objective of OBJECTIVE_KEYS) await planService.run(orderId, { objective, topN })
  },

  // Best plan per objective for an unsaved order; nothing is stored.
  preview: (items) =>
    http.post('/plans/preview', {
      items: items.map((i) => ({ id_product: i.productId, quantity: i.quantity })),
    }),
}
