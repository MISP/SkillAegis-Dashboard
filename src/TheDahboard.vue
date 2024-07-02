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
  <TheScores></TheScores>
  <TheLiveLogs></TheLiveLogs>
</template>
