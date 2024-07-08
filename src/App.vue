<script setup>
import { onMounted } from 'vue'
import TheThemeButton from './components/TheThemeButton.vue'
import TheAdminPanel from './components/TheAdminPanel.vue'
import TheSocketConnectionState from './components/TheSocketConnectionState.vue'
import TheDahboard from './TheDahboard.vue'
import { socketConnected } from "@/socket";
import { darkModeEnabled } from "@/settings.js"


onMounted(() => {
  if (darkModeEnabled.value) {
    document.getElementsByTagName('body')[0].classList.add('dark')
  }
})

</script>

<template>
  <main>
    <h1 class="text-2xl text-center text-slate-500 dark:text-slate-400 absolute top-1 left-1">Exercise Dashboard</h1>
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

#app {
  @apply 3xl:container mx-auto;
  @apply mx-auto;
  @apply mt-4;
  @apply 3xl:w-11/12;
  @apply lg:w-5/6;
}

</style>