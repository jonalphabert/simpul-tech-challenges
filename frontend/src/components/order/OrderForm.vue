<script setup>
import { computed, reactive, ref, watch } from 'vue'
import ErrorAlert from '../ui/ErrorAlert.vue'
import Icon from '../ui/Icon.vue'
import OrderFormLine from './OrderFormLine.vue'
import PlanPreview from './PlanPreview.vue'

const props = defineProps({
  products: { type: Array, required: true },
  warehouses: { type: Array, required: true },
  defaultNumber: { type: String, default: '' },
  existingNumbers: { type: Array, default: () => [] },
  submitting: { type: Boolean, default: false },
  serverError: { type: String, default: '' },
})
const emit = defineEmits(['submit', 'cancel'])

let nextKey = 0
const newLine = () => ({ key: ++nextKey, productId: null, qty: '' })

const form = reactive({ number: props.defaultNumber, lines: [newLine()] })
const validationError = ref('')

// The suggested number arrives once the order list has loaded.
watch(
  () => props.defaultNumber,
  (value) => {
    if (!form.number) form.number = value
  },
)

const validLines = computed(() =>
  form.lines
    .filter((l) => l.productId && parseInt(l.qty, 10) > 0)
    .map((l) => ({ productId: l.productId, quantity: parseInt(l.qty, 10) })),
)
const hasDuplicates = computed(() => new Set(validLines.value.map((l) => l.productId)).size !== validLines.value.length)

function updateLine(line, patch) {
  Object.assign(line, patch)
  validationError.value = ''
}

function addLine() {
  form.lines.push(newLine())
}

function removeLine(index) {
  form.lines.splice(index, 1)
}

function validate() {
  const number = form.number.trim()
  if (!number) return 'Nomor order wajib diisi.'
  if (props.existingNumbers.some((n) => n.toLowerCase() === number.toLowerCase())) return `Nomor order ${number} sudah dipakai.`
  const filled = form.lines.filter((l) => l.productId || l.qty !== '')
  if (!filled.length) return 'Tambahkan minimal satu produk.'
  if (filled.some((l) => !l.productId)) return 'Ada baris tanpa produk.'
  if (filled.some((l) => !Number.isInteger(Number(l.qty)) || Number(l.qty) <= 0)) return 'Jumlah harus bilangan bulat lebih dari 0.'
  if (new Set(filled.map((l) => l.productId)).size !== filled.length)
    return 'Produk yang sama muncul di lebih dari satu baris. Gabungkan jumlahnya.'
  return ''
}

function submit() {
  validationError.value = validate()
  if (validationError.value) return
  emit('submit', { orderNumber: form.number.trim(), items: validLines.value })
}
</script>

<template>
  <form
    class="flex flex-col gap-6 rounded-xl border border-slate-200 bg-white p-5 shadow-xs sm:p-6"
    aria-labelledby="form-title"
    novalidate
    @submit.prevent="submit"
  >
    <div class="flex flex-wrap items-start justify-between gap-3">
      <div class="flex flex-col gap-1">
        <h2 id="form-title" class="text-xl font-semibold">Order baru</h2>
        <p class="text-sm text-slate-600">Isi nomor order dan produk. Plan dihitung otomatis dari stok warehouse saat ini.</p>
      </div>
      <button type="button" class="min-h-[44px] rounded-lg px-3 text-sm font-medium text-slate-600 hover:bg-slate-100" @click="emit('cancel')">
        Batal
      </button>
    </div>

    <label class="flex max-w-xs flex-col gap-1.5">
      <span class="text-sm font-medium text-slate-700">Nomor order</span>
      <input
        v-model="form.number"
        type="text"
        autocomplete="off"
        class="min-h-[44px] rounded-lg border border-slate-300 px-3 font-mono text-sm focus:border-blue-600 focus:outline-hidden focus:ring-2 focus:ring-blue-600/20"
        @input="validationError = ''"
      />
    </label>

    <fieldset class="flex flex-col gap-3">
      <legend class="mb-2 text-sm font-medium text-slate-700">Produk</legend>
      <div class="hidden grid-cols-[minmax(0,1fr)_8rem_minmax(0,14rem)_2.75rem] gap-3 px-1 text-xs font-medium uppercase tracking-wider text-slate-500 md:grid">
        <span>Produk</span><span>Jumlah</span><span>Stok yang memenuhi syarat</span><span class="sr-only">Hapus</span>
      </div>

      <OrderFormLine
        v-for="(line, index) in form.lines"
        :key="line.key"
        :line="line"
        :index="index"
        :products="products"
        :warehouses="warehouses"
        :removable="form.lines.length > 1"
        @update="updateLine(line, $event)"
        @remove="removeLine(index)"
      />

      <div>
        <button
          type="button"
          class="inline-flex min-h-[44px] items-center gap-2 rounded-lg border border-dashed border-slate-400 px-4 text-sm font-medium text-slate-700 hover:border-blue-600 hover:text-blue-700"
          @click="addLine"
        >
          <Icon name="plus" />
          Tambah produk
        </button>
      </div>
    </fieldset>

    <PlanPreview :lines="validLines" :has-duplicates="hasDuplicates" :products="products" :warehouses="warehouses" />

    <ErrorAlert :message="validationError || serverError" />

    <div class="flex flex-wrap justify-end gap-3 border-t border-slate-200 pt-5">
      <button
        type="button"
        class="min-h-[44px] rounded-lg border border-slate-300 px-4 text-sm font-medium text-slate-700 hover:bg-slate-50"
        @click="emit('cancel')"
      >
        Batal
      </button>
      <button
        type="submit"
        :disabled="submitting"
        class="min-h-[44px] rounded-lg bg-blue-700 px-5 text-sm font-semibold text-white hover:bg-blue-800 focus:outline-hidden focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 disabled:opacity-60"
      >
        {{ submitting ? 'Menyimpan & menghitung…' : 'Simpan & buat plan' }}
      </button>
    </div>
  </form>
</template>
