<script setup>
import { onMounted } from 'vue'
import TheThemeButton from './components/TheThemeButton.vue'
import TheAdminPanel from './components/TheAdminPanel.vue'
import TheSocketConnectionState from './components/TheSocketConnectionState.vue'
import TheDahboard from './TheDahboard.vue'
import { socketConnected } from "@/socket";


onMounted(() => {
  document.getElementsByTagName('body')[0].classList.add('dark')
  document.getElementById('app').classList.add('w-5/6')
})

</script>

<template>
  <main>
    <h1 class="text-2xl text-center text-slate-500 dark:text-slate-400 absolute top-1 left-1">MISP Exercise Dashboard</h1>
    <div class="absolute top-1 right-1">
      <div class="flex gap-2">
        <TheThemeButton></TheThemeButton>
        <TheAdminPanel></TheAdminPanel>
        <TheSocketConnectionState></TheSocketConnectionState>
      </div>
    </div>
    <TheDahboard></TheDahboard>
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