<script setup>
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
  import { faMoon, faSun } from '@fortawesome/free-solid-svg-icons'
  import { socketConnected } from "@/socket";

</script>

<template>
  <span :class="{
    'px-2 py-1 rounded-md inline-block w-48': true,
    'text-slate-900 dark:text-slate-400': socketConnected,
    'text-slate-50 bg-red-600': !socketConnected,
  }">
    <span class="mr-1">Socket.IO:</span>
    <span v-show="socketConnected" class="font-semibold text-green-600 dark:text-green-400">Connected</span>
    <span v-show="!socketConnected" class="font-semibold text-slate-50">Disconnected</span>
  </span>
</template>