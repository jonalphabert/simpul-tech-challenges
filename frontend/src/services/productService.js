import { http } from './http'

export const productService = {
  list: () => http.get('/products'),
}
