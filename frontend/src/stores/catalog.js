import { ref } from 'vue'
import { productService } from '../services/productService'
import { warehouseService } from '../services/warehouseService'

// Shared across views: products and warehouses (with stock) rarely change.
const products = ref([])
const warehouses = ref([])
const error = ref('')
let pending = null

function load({ force = false } = {}) {
  if (pending && !force) return pending
  error.value = ''
  pending = Promise.all([productService.list(), warehouseService.list()])
    .then(([p, w]) => {
      products.value = p
      warehouses.value = w
    })
    .catch((e) => {
      error.value = e.message
      pending = null
    })
  return pending
}

export function useCatalog() {
  return { products, warehouses, error, load }
}
