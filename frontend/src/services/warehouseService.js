import { http } from './http'

export const warehouseService = {
  // Each warehouse comes with its stock lines and their products.
  list: () => http.get('/warehouses'),
}
