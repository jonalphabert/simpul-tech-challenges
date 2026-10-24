<script setup>
import { computed } from 'vue'
import Chip from '../ui/Chip.vue'
import Icon from '../ui/Icon.vue'
import { eligibleStock } from '../../utils/eligibility'
import { fmt } from '../../utils/format'

const props = defineProps({
  line: { type: Object, required: true }, // { key, productId, qty }
  index: { type: Number, required: true },
  products: { type: Array, required: true },
  warehouses: { type: Array, required: true },
  removable: { type: Boolean, default: true },
})
defineEmits(['update', 'remove'])

const n = computed(() => props.index + 1)
const product = computed(() => props.products.find((p) => p.id === props.line.productId))

const availability = computed(() => {
  if (!product.value) return { text: 'Pilih produk', cls: 'text-slate-500' }
  const { total, warehouses } = eligibleStock(props.warehouses, product.value)
  const qty = parseInt(props.line.qty, 10) || 0
  if (qty > total) return { text: `Kurang ${fmt(qty - total)} · tersedia ${fmt(total)}`, cls: 'font-medium text-orange-800' }
  return { text: `${fmt(total)} unit di ${warehouses.length} gudang`, cls: 'text-slate-700' }
})

const INPUT = 'min-h-[44px] w-full rounded-lg border border-slate-300 bg-white px-3 text-sm focus:border-blue-600 focus:outline-hidden focus:ring-2 focus:ring-blue-600/20'
const REMOVE = 'h-11 w-11 items-center justify-center rounded-lg text-slate-500 hover:bg-red-50 hover:text-red-700 disabled:opacity-30'
</script>

<template>
  <div
    class="grid grid-cols-[minmax(0,1fr)_2.75rem] gap-3 rounded-lg border border-slate-200 bg-slate-50 p-3 md:grid-cols-[minmax(0,1fr)_8rem_minmax(0,14rem)_2.75rem] md:items-center md:border-0 md:bg-transparent md:p-1"
  >
    <label class="col-span-1 flex flex-col gap-1">
      <span class="text-xs font-medium text-slate-600 md:sr-only">Produk baris {{ n }}</span>
      <select
        :value="line.productId ?? ''"
        :class="INPUT"
        @change="$emit('update', { productId: Number($event.target.value) || null })"
      >
        <option value="">Pilih produk…</option>
        <option v-for="p in products" :key="p.id" :value="p.id">
          {{ p.name }}{{ p.need_refrigerator ? ' (dingin)' : '' }}
        </option>
      </select>
    </label>

    <button
      type="button"
      :class="[REMOVE, 'flex self-end md:hidden']"
      :disabled="!removable"
      :aria-label="`Hapus baris ${n}`"
      @click="$emit('remove')"
    >
      <Icon name="close" :size="18" />
    </button>

    <label class="flex flex-col gap-1">
      <span class="text-xs font-medium text-slate-600 md:sr-only">Jumlah baris {{ n }}</span>
      <input
        :value="line.qty"
        type="number"
        min="1"
        step="1"
        inputmode="numeric"
        placeholder="0"
        :class="[INPUT, 'text-right font-mono']"
        @input="$emit('update', { qty: $event.target.value })"
      />
    </label>

    <div class="flex min-h-[44px] items-center gap-2 text-sm">
      <Chip v-if="product?.need_refrigerator" tone="sky" title="Butuh rantai dingin">
        <Icon name="snowflake" :size="12" />Dingin
      </Chip>
      <span :class="availability.cls">{{ availability.text }}</span>
    </div>

    <button
      type="button"
      :class="[REMOVE, 'hidden md:flex']"
      :disabled="!removable"
      :aria-label="`Hapus baris ${n}`"
      @click="$emit('remove')"
    >
      <Icon name="close" :size="18" />
    </button>
  </div>
</template>
