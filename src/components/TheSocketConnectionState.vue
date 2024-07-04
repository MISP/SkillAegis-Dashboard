<script setup>
  import { ref, onMounted } from "vue"
  import { socketConnected, zmqLastTime } from "@/socket";

  const zmqLastTimeSecond = ref(0)

  function refreshLastTime() {
    zmqLastTimeSecond.value = parseInt(((new Date()).getTime() - zmqLastTime.value * 1000) / 1000)
  }

  onMounted(() => {
    setInterval(() => {
      refreshLastTime()
    }, 1000)
  })

</script>

<template>
  <span class="flex flex-col justify-center mt-1">
    <span :class="{
      'px-2 rounded-md inline-block w-48 leading-4': true,
      'text-slate-900 dark:text-slate-400': socketConnected,
      'text-slate-50 bg-red-600 px-2 py-1': !socketConnected,
    }">
      <span class="mr-1">Socket.IO:</span>
      <span v-show="socketConnected" class="font-semibold text-green-600 dark:text-green-400">Connected</span>
      <span v-show="!socketConnected" class="font-semibold text-slate-50">Disconnected</span>
    </span>
    <span
      v-if="socketConnected"
      class="text-xs font-thin leading-3 inline-block text-center"
    >
      <template v-if="zmqLastTimeSecond == 0">
        online
      </template>
      <template v-else>
        Last keep-alive: {{ zmqLastTimeSecond }}s ago
      </template>
    </span>
  </span>
</template>