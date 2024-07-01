<script setup>
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
  import { faMoon, faSun } from '@fortawesome/free-solid-svg-icons'
  import { socketConnected } from "@/socket";

</script>

<template>
  <span class="text-slate-900 dark:text-slate-400 shadow-blue-500/50">
    <span class="mr-1">Socket.IO:</span>
    <span v-show="socketConnected" class="font-semibold text-green-600 dark:text-green-400">Connected</span>
    <span v-show="!socketConnected" class="font-semibold text-red-500">Disconnected</span>
  </span>
</template>