<script setup>
import { onMounted, watch } from 'vue'
import TheLiveLogs from './components/TheLiveLogs.vue'
import TheScores from './components/TheScores.vue'
import { resetState, fullReload, socketConnected } from "@/socket";


watch(socketConnected, (isConnected) => {
  if (isConnected) {
    resetState()
    fullReload()
  }
})

onMounted(() => {
  fullReload()
})

</script>

<template>
  <h1 class="text-3xl font-bold text-center text-slate-600 dark:text-slate-300">MISP Exercise Dashboard</h1>
  <TheScores></TheScores>
  <TheLiveLogs></TheLiveLogs>
</template>
