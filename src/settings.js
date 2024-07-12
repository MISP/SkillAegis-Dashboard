import { ref, computed } from 'vue'

export const darkModeOn = ref(true)
export const darkModeEnabled = computed(() => darkModeOn.value)

export const fullscreenModeOn = ref(false)