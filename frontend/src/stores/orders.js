import { ref } from 'vue'
import { orderService } from '../services/orderService'

// Shared order list: used by the sidebar and the header count.
const orders = ref([])
const error = ref('')
const loaded = ref(false)

async function refresh() {
  error.value = ''
  try {
    orders.value = await orderService.list()
  } catch (e) {
    error.value = e.message
  } finally {
    loaded.value = true
  }
}

export function useOrders() {
  return { orders, error, loaded, refresh }
}
