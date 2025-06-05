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
  <div class="main-grid default-template h-screen w-screen overflow-hidden p-2">
    <div style="grid-area: stats;" class="the-stats overflow-hidden">
      <TheStats></TheStats>
    </div>
    <div style="grid-area: scores;" class="the-scores overflow-x-hidden overflow-y-auto">
      <TheScores></TheScores>
    </div>
    <div style="grid-area: logs;" class="the-logs overflow-hidden">
      <TheLiveLogs></TheLiveLogs>
    </div>
  </div>
</template>


<style>
.main-grid {
  display: grid;
  gap: 1rem;
}

.default-template {
  grid-template-columns: 7fr 3fr;
  grid-template-rows: auto 1fr;
  grid-template-areas:
    'scores stats'
    'scores logs';
}

.score-fullscreen-template {
  grid-template-columns: 1fr 0px;
  grid-template-rows: 1fr 0px;
  grid-template-areas:
  'scores scores'
  'scores scores';
}
.score-fullscreen-template .the-stats,
.score-fullscreen-template .the-logs {
  display: none;
}

.logs-fullscreen-template {
  grid-template-columns: 1fr 0px;
  grid-template-rows: 1fr 0px;
  grid-template-areas:
  'logs logs'
  'logs logs';
}
.logs-fullscreen-template .the-stats,
.logs-fullscreen-template .the-scores {
  display: none;
}
</style>