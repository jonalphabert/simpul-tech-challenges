import { onBeforeUnmount, ref, watch } from 'vue'
import { planService } from '../services/planService'

const DEBOUNCE_MS = 400

// Re-runs the planner preview whenever the (valid, unique) order lines change.
export function usePlanPreview(linesRef) {
  const result = ref(null)
  const loading = ref(false)
  const error = ref('')
  let timer = null
  let requestId = 0

  watch(
    linesRef,
    (lines) => {
      clearTimeout(timer)
      result.value = null
      error.value = ''
      if (!lines.length) return
      loading.value = true
      timer = setTimeout(async () => {
        const id = ++requestId
        try {
          const data = await planService.preview(lines)
          if (id === requestId) result.value = data
        } catch (e) {
          if (id === requestId) error.value = e.message
        } finally {
          if (id === requestId) loading.value = false
        }
      }, DEBOUNCE_MS)
    },
    { deep: true, immediate: true },
  )

  onBeforeUnmount(() => clearTimeout(timer))

  return { result, loading, error }
}
