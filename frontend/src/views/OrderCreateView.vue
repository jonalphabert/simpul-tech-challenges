<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import OrderForm from '../components/order/OrderForm.vue'
import ErrorAlert from '../components/ui/ErrorAlert.vue'
import { orderService } from '../services/orderService'
import { planService } from '../services/planService'
import { useCatalog } from '../stores/catalog'
import { useOrders } from '../stores/orders'

const router = useRouter()
const { products, warehouses, error: catalogError } = useCatalog()
const { orders, loaded, refresh: refreshOrders } = useOrders()

const submitting = ref(false)
const serverError = ref('')

const existingNumbers = computed(() => orders.value.map((o) => o.order_number))

// Suggests ORD-YYMM-NNN, continuing from the highest trailing number in use.
const defaultNumber = computed(() => {
  if (!loaded.value) return ''
  const now = new Date()
  const prefix = `ORD-${String(now.getFullYear()).slice(2)}${String(now.getMonth() + 1).padStart(2, '0')}-`
  const max = Math.max(0, ...existingNumbers.value.map((n) => Number(/(\d+)$/.exec(n)?.[1] ?? 0)))
  return prefix + String(max + 1).padStart(3, '0')
})

async function create({ orderNumber, items }) {
  submitting.value = true
  serverError.value = ''
  try {
    const order = await orderService.create({ orderNumber, items })
    // The order exists even if planning fails; its page then offers "Buat plan".
    await planService.runAll(order.id).catch(() => {})
    await refreshOrders()
    router.push(`/orders/${order.id}`)
  } catch (e) {
    serverError.value = e.message
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <ErrorAlert :message="catalogError" />
  <OrderForm
    :products="products"
    :warehouses="warehouses"
    :default-number="defaultNumber"
    :existing-numbers="existingNumbers"
    :submitting="submitting"
    :server-error="serverError"
    @submit="create"
    @cancel="router.push('/orders')"
  />
</template>
