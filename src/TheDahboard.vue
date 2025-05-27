<script setup>
import { onMounted, watch } from 'vue'
import TheLiveLogs from './components/TheLiveLogs.vue'
import TheScores from './components/TheScores.vue'
import TheStats from './components/TheStats.vue'
import { resetState, fullReload, socketConnected } from './socket'
import { fullscreenModeOn } from './settings.js'

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
  <div class="main-grid h-screen w-screen overflow-hidden p-2">
    <div style="grid-area: stats;">
      <TheStats></TheStats>
    </div>
    <div style="grid-area: scores;" class="overflow-x-hidden overflow-y-auto">
      <TheScores></TheScores>
    </div>
    <div style="grid-area: logs;" class="overflow-hidden">
      <TheLiveLogs></TheLiveLogs>
    </div>
  </div>
</template>


<style>
.main-grid {
  display: grid;
  grid-template-columns: 5fr 2fr;
  grid-template-rows: 2fr 5fr;
  gap: 1rem;
  grid-template-areas:
    'scores stats'
    'scores logs';
}
</style>