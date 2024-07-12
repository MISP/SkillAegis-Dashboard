<script setup>
import { onMounted, watch } from 'vue'
import TheLiveLogs from './components/TheLiveLogs.vue'
import TheScores from './components/TheScores.vue'
import { resetState, fullReload, socketConnected } from "@/socket";
import { fullscreenModeOn } from "@/settings.js"


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
  <div class="mb-3">
    <TheScores></TheScores>
    <TheLiveLogs v-show="!fullscreenModeOn"></TheLiveLogs>
  </div>
</template>
