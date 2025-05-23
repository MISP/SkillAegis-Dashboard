import { computed, ref } from 'vue'

let toastID = 0
export const toastBuffer = ref([])
export const allToasts = computed(() => toastBuffer.value)
export function toast(toast) {
  toastID += 1
  toast.id = toastID
  toastBuffer.value.push(toast)
}
export function removeToast(id) {
  toastBuffer.value = toastBuffer.value.filter((toast) => toast.id != id)
}
export function ajaxFeedback(response) {
  toast({
    variant: response.success ? 'success' : 'danger',
    message: String(response.message),
    title: response.title
  })
}

let timer = null
const timerInterval = 7000
const timerCallbacks = {}

if (timer === null) {
  timer = setInterval(() => {
    Object.values(timerCallbacks).forEach(callback => {
      callback()
    });
  }, timerInterval)
}

export function registerTimerCallback(callback) {
  const id = Math.random().toString(36).substring(2, 15)
  if (!timerCallbacks[id]) {
    timerCallbacks[id] = callback
    return id
  }
  return null
}
export function unregisterTimerCallback(id) {
  if (timerCallbacks[id]) {
    delete timerCallbacks[id]
  }
}