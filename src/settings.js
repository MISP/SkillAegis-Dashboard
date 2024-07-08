import { ref, computed } from 'vue'

export const darkModeOn = ref(true)
export const darkModeEnabled = computed(() => darkModeOn.value)