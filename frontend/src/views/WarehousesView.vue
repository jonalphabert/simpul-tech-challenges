<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ErrorAlert from '../components/ui/ErrorAlert.vue'
import PlanHighlightBanner from '../components/warehouse/PlanHighlightBanner.vue'
import StockMatrix from '../components/warehouse/StockMatrix.vue'
import WarehouseCard from '../components/warehouse/WarehouseCard.vue'
import { useOrderPlans } from '../composables/useOrderPlans'
import { useCatalog } from '../stores/catalog'
import { objectiveLetter, plansFor } from '../utils/plans'

const route = useRoute()
const router = useRouter()
const { products, warehouses, error: catalogError } = useCatalog()

// ?order=&objective=&rank= selects the plan to highlight.
const orderId = computed(() => Number(route.query.order) || null)
const letter = computed(() => objectiveLetter(route.query.objective))
const rank = computed(() => Number(route.query.rank) || 1)
const { order, plans, error } = useOrderPlans(orderId)

const plan = computed(() => (orderId.value ? plansFor(plans.value, letter.value).find((p) => p.rank === rank.value) : null))

const highlight = computed(() => {
  if (!plan.value || !order.value) return null
  const shipments = new Map(plan.value.details.map((d) => [`${d.id_warehouse}-${d.id_product}`, d.quantity]))
  return {
    title: `Plan #${rank.value} · Opsi ${letter.value} untuk ${order.value.order_number}`,
    usedIds: new Set(plan.value.details.map((d) => d.id_warehouse)),
    productIds: new Set(order.value.details.map((d) => d.id_product)),
    ship: (warehouseId, productId) => shipments.get(`${warehouseId}-${productId}`) ?? 0,
  }
})

function shippedUnits(warehouse) {
  if (!highlight.value) return null
  return plan.value.details.filter((d) => d.id_warehouse === warehouse.id).reduce((sum, d) => sum + d.quantity, 0)
}

function backToOrder() {
  router.push({ path: `/orders/${orderId.value}`, query: { objective: letter.value, rank: rank.value } })
}
</script>

<template>
  <main class="mx-auto flex max-w-7xl flex-col gap-6 px-4 py-6 sm:px-6">
    <div class="flex flex-wrap items-end justify-between gap-4">
      <div class="flex flex-col gap-1">
        <h2 class="text-2xl font-semibold">Warehouse</h2>
        <p class="text-sm text-slate-600">
          Jarak dihitung ke klien. Produk dingin hanya bisa dikirim dari gudang yang punya cold storage
          <span class="font-medium">dan</span> van berpendingin.
        </p>
      </div>
    </div>

    <ErrorAlert :message="catalogError || error" />

    <PlanHighlightBanner v-if="highlight" :title="highlight.title" @back="backToOrder" @clear="router.replace('/warehouses')" />

    <div class="grid grid-cols-[repeat(auto-fill,minmax(min(13rem,100%),1fr))] gap-3">
      <WarehouseCard v-for="w in warehouses" :key="w.id" :warehouse="w" :shipped-units="shippedUnits(w)" />
    </div>

    <StockMatrix :products="products" :warehouses="warehouses" :highlight="highlight" />
  </main>
</template>
