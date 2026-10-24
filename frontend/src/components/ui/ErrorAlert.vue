<script setup>
defineProps({ message: { type: String, default: '' } })
</script>

<template>
  <p v-if="message" class="rounded-lg bg-red-50 px-3 py-2 text-sm font-medium text-red-800" role="alert">{{ message }}</p>
</template>
