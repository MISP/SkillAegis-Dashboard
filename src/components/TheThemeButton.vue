<script setup>
  import { ref, watch } from 'vue'
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
  import { faMoon, faSun } from '@fortawesome/free-solid-svg-icons'

  const darkMode = ref(true)

  watch(darkMode, (newValue) => {
    if (newValue) {
        document.getElementsByTagName('body')[0].classList.add('dark')
      } else {
        document.getElementsByTagName('body')[0].classList.remove('dark')
    }
  })
</script>

<template>
  <button
    @click="darkMode = !darkMode"
    class="mr-3 px-2 py-1 rounded-md focus-outline font-semibold bg-blue-600 text-slate-200 hover:bg-blue-700"
  >
    <FontAwesomeIcon :icon="faSun" class="mr-1" v-show="!darkMode"></FontAwesomeIcon>
    <FontAwesomeIcon :icon="faMoon" class="mr-1" v-show="darkMode"></FontAwesomeIcon>
    {{ darkMode ? 'Dark' : 'Light'}}
  </button>
</template>