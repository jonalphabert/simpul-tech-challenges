<script setup>
import { computed } from 'vue'
import { shortages } from '../../utils/eligibility'
import { fmt } from '../../utils/format'

const props = defineProps({
  details: { type: Array, required: true },
  warehouses: { type: Array, required: true },
})

const issues = computed(() => shortages(props.details, props.warehouses))
</script>

<template>
  <div class="flex flex-col gap-2 rounded-xl border border-orange-300 bg-orange-50 p-4" role="alert">
    <h3 class="font-semibold text-orange-900">Order tidak dapat dipenuhi</h3>
    <p class="text-sm text-orange-900">
      Tidak ada kombinasi warehouse yang bisa mengirim seluruh jumlah.
      <template v-if="issues.length">Produk yang kurang:</template>
    </p>
    <ul v-if="issues.length" class="flex flex-col gap-1 text-sm text-orange-950">
      <li v-for="i in issues" :key="i.id_product" class="font-mono">
        {{ i.product.name }}: dipesan {{ fmt(i.quantity) }}, tersedia {{ fmt(i.available) }} → kurang
        {{ fmt(i.quantity - i.available) }} unit
      </li>
    </ul>
  </div>
</template>
