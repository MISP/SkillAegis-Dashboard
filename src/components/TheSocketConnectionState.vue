<script setup>
import { ref, onMounted } from 'vue'
import { socketConnected, zmqLastTime } from '../socket'
import { faCircle } from '@fortawesome/free-solid-svg-icons'

const zmqLastTimeSecond = ref('?')

function refreshLastTime() {
  if (zmqLastTime.value !== false) {
    zmqLastTimeSecond.value = parseInt((new Date().getTime() - zmqLastTime.value * 1000) / 1000)
  } else {
    zmqLastTimeSecond.value = '?'
  }
}

onMounted(() => {
  setInterval(() => {
    refreshLastTime()
  }, 1000)
})
</script>

<template>
  <span class="inline-flex flex-row items-center">
    <span
      :class="{
        'inline-flex leading-4': true,
        'text-slate-900 dark:text-slate-400': socketConnected,
        'text-red-600 px-2 py-1': !socketConnected
      }"
    >
      <span v-show="socketConnected" class="text-sm text-green-600 dark:text-green-500 justify-content-end leading-4">
        <FontAwesomeIcon :icon="faCircle" size="sm"></FontAwesomeIcon>
        Connected
      </span>
      <span v-show="!socketConnected" class="text-sm leading-4">
        <FontAwesomeIcon :icon="faCircle" size="sm"></FontAwesomeIcon>
        Disconnected
      </span>
    </span>
    <span v-if="socketConnected" class="ml-1 text-xs leading-3 inline-block text-center">
      <span v-show="zmqLastTimeSecond > 10"> Last ZMQ message: {{ zmqLastTimeSecond }}s ago</span>
    </span>
  </span>
</template>
