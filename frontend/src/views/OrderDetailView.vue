<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import InfeasibleAlert from '../components/order/InfeasibleAlert.vue'
import OrderItemsTable from '../components/order/OrderItemsTable.vue'
import PlanSection from '../components/plan/PlanSection.vue'
import EmptyState from '../components/ui/EmptyState.vue'
import ErrorAlert from '../components/ui/ErrorAlert.vue'
import Icon from '../components/ui/Icon.vue'
import StatusBadge from '../components/ui/StatusBadge.vue'
import { useOrderPlans } from '../composables/useOrderPlans'
import { useCatalog } from '../stores/catalog'
import { fmt } from '../utils/format'
import { objectiveLetter, orderStatus, plansFor } from '../utils/plans'

const props = defineProps({ id: { type: String, required: true } })

const route = useRoute()
const router = useRouter()
const { warehouses } = useCatalog()
const { order, plans, loading, planning, error, runPlans } = useOrderPlans(() => Number(props.id))

// Objective and plan rank live in the URL so the warehouse page can link back.
const letter = computed({
  get: () => objectiveLetter(route.query.objective),
  // A new objective starts at its best plan.
  set: (value) => router.replace({ query: { ...route.query, objective: value, rank: 1 } }),
})
const rank = computed({
  get: () => {
    const wanted = Number(route.query.rank) || 1
    const available = plansFor(plans.value, letter.value)
    return available.some((p) => p.rank === wanted) ? wanted : 1
  },
  set: (value) => router.replace({ query: { ...route.query, rank: value } }),
})

const status = computed(() => orderStatus(plans.value))
const units = computed(() => order.value?.details.reduce((sum, d) => sum + d.quantity, 0) ?? 0)

function matchInWarehouses() {
  router.push({ path: '/warehouses', query: { order: props.id, objective: letter.value, rank: rank.value } })
}
</script>

<template>
  <ErrorAlert :message="error" />

  <p v-if="loading && !order" class="text-sm text-slate-500">Memuat order…</p>

  <div v-if="order" class="flex flex-col gap-6">
    <div class="flex flex-wrap items-end justify-between gap-4">
      <div class="flex flex-col gap-1">
        <span class="text-xs font-semibold uppercase tracking-wider text-slate-500">Order</span>
        <div class="flex flex-wrap items-center gap-3">
          <h2 class="font-mono text-2xl font-semibold">{{ order.order_number }}</h2>
          <StatusBadge :status="status" />
        </div>
        <p class="text-sm text-slate-600">
          {{ order.details.length }} produk · {{ fmt(units) }} unit · dikirim ke klien tunggal
        </p>
      </div>
      <button
        v-if="status === 'feasible'"
        type="button"
        class="inline-flex min-h-[44px] items-center gap-2 rounded-lg border border-slate-300 bg-white px-4 text-sm font-medium text-slate-800 hover:border-blue-600 hover:text-blue-700"
        @click="matchInWarehouses"
      >
        <Icon name="warehouse" />
        Cocokkan Plan #{{ rank }} di Warehouse
      </button>
    </div>

    <OrderItemsTable :details="order.details" :warehouses="warehouses" />

    <EmptyState
      v-if="status === null"
      title="Order belum diplan"
      description="Hitung plan dari stok warehouse saat ini untuk kedua tujuan optimasi."
    >
      <button
        type="button"
        :disabled="planning"
        class="min-h-[44px] rounded-lg bg-blue-700 px-5 text-sm font-semibold text-white hover:bg-blue-800 disabled:opacity-60"
        @click="runPlans"
      >
        {{ planning ? 'Menghitung…' : 'Buat plan' }}
      </button>
    </EmptyState>

    <InfeasibleAlert v-else-if="status === 'infeasible'" :details="order.details" :warehouses="warehouses" />

    <PlanSection v-else v-model:letter="letter" v-model:rank="rank" :plans="plans" :warehouses="warehouses" />
  </div>
</template>
