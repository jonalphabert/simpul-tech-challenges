<script setup>
defineProps({ title: { type: String, required: true } })
defineEmits(['back', 'clear'])
</script>

<template>
  <div class="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-blue-200 bg-blue-50 px-4 py-3">
    <p class="text-sm text-blue-950">
      <span class="font-semibold">Mencocokkan {{ title }}</span> — gudang yang dipakai ditandai, angka biru adalah jumlah yang dikirim dari stok.
    </p>
    <div class="flex flex-wrap gap-2">
      <button
        type="button"
        class="min-h-[44px] rounded-lg bg-white px-3 text-sm font-medium text-blue-800 ring-1 ring-blue-200 hover:bg-blue-100"
        @click="$emit('back')"
      >
        Kembali ke order
      </button>
      <button type="button" class="min-h-[44px] rounded-lg px-3 text-sm font-medium text-blue-800 hover:bg-blue-100" @click="$emit('clear')">
        Hapus sorotan
      </button>
    </div>
  </div>
</template>
