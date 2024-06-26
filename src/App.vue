<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import TheDahboard from './components/TheDahboard.vue'
import { connectionState } from "@/socket";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faMoon, faSun } from '@fortawesome/free-solid-svg-icons'

const darkMode = ref(true)

onMounted(() => {
  document.getElementsByTagName('body')[0].classList.add('dark')
  document.getElementById('app').classList.add('w-5/6')
})

const socketConnected = computed(() => connectionState.connected)

watch(darkMode, (newValue) => {
  if (newValue) {
      document.getElementsByTagName('body')[0].classList.add('dark')
    } else {
      document.getElementsByTagName('body')[0].classList.remove('dark')
  }
})

</script>

<template>
  <main>
    <div class="absolute top-1 right-1">
      <button
        @click="darkMode = !darkMode"
        class="mr-3 px-2 py-1 rounded-md focus-outline font-semibold bg-blue-600 text-slate-200 hover:bg-blue-700"
      >
        <FontAwesomeIcon :icon="faSun" class="mr-1" v-show="!darkMode"></FontAwesomeIcon>
        <FontAwesomeIcon :icon="faMoon" class="mr-1" v-show="darkMode"></FontAwesomeIcon>
        {{ darkMode ? 'Dark' : 'Light'}}
      </button>
      <span class="text-slate-900 dark:text-slate-400 shadow-blue-500/50">
        <span class="mr-1">Socket.IO:</span>
        <span v-show="socketConnected" class="font-semibold text-green-600 dark:text-green-400">Connected</span>
        <span v-show="!socketConnected" class="font-semibold text-red-500">Disconnected</span>
      </span>
    </div>
    <TheDahboard />
  </main>
</template>

<style>
body {
  @apply flex;
  @apply bg-slate-200;
  @apply dark:bg-gray-700;
  @apply text-slate-400;
  @apply dark:text-slate-300;
}

</style>