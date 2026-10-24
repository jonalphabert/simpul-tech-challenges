import { ref, toValue, watch } from 'vue'
import { orderService } from '../services/orderService'
import { planService } from '../services/planService'
import { useOrders } from '../stores/orders'

// Loads one order with its saved plans and can (re)run the planner for it.
export function useOrderPlans(orderId) {
  const order = ref(null)
  const plans = ref([])
  const loading = ref(false)
  const planning = ref(false)
  const error = ref('')
  const { refresh: refreshOrders } = useOrders()

  async function load() {
    const id = toValue(orderId)
    if (!id) {
      order.value = null
      plans.value = []
      return
    }
    loading.value = true
    error.value = ''
    try {
      ;[order.value, plans.value] = await Promise.all([orderService.get(id), planService.list(id)])
    } catch (e) {
      error.value = e.message
      order.value = null
    } finally {
      loading.value = false
    }
  }

  async function runPlans() {
    planning.value = true
    error.value = ''
    try {
      await planService.runAll(toValue(orderId))
      plans.value = await planService.list(toValue(orderId))
      await refreshOrders()
    } catch (e) {
      error.value = e.message
    } finally {
      planning.value = false
    }
  }

  watch(() => toValue(orderId), load, { immediate: true })

  return { order, plans, loading, planning, error, load, runPlans }
}
