import { http } from './http'

export const orderService = {
  list: () => http.get('/orders'),
  get: (id) => http.get(`/orders/${id}`),
  create: ({ orderNumber, items }) =>
    http.post('/orders', {
      order_number: orderNumber,
      items: items.map((i) => ({ id_product: i.productId, quantity: i.quantity })),
    }),
  remove: (id) => http.delete(`/orders/${id}`),
}
