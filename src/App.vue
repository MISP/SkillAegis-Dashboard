<script setup>
import { onMounted } from 'vue'
import TheThemeButton from './components/TheThemeButton.vue'
import TheAdminPanel from './components/TheAdminPanel.vue'
import TheSocketConnectionState from './components/TheSocketConnectionState.vue'
import TheDahboard from './TheDahboard.vue'
import Toaster from '@/components/elements/Toaster.vue'
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
    <h1 class="text-xl text-center text-slate-500 dark:text-slate-400 absolute inset-x-0 top-0">
      <div class="flex flex-col items-center mt-2">
        <span id="logo" class="hover:cursor-pointer"></span>
        <span>SkillAegis</span>
      </div>
    </h1>
    <div class="absolute top-1 right-1">
      <div class="flex gap-2">
        <TheThemeButton></TheThemeButton>
        <TheAdminPanel></TheAdminPanel>
        <TheSocketConnectionState></TheSocketConnectionState>
      </div>
    </div>
    <div class="mt-12">
      <TheDahboard></TheDahboard>
    </div>
    <Toaster></Toaster>
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
  @apply lg:w-11/12;
  @apply 3xl:w-5/6;
}

#logo {
  background-image: url(@/assets/skillaegis-logo.svg);
  width: 64px;
  height: 64px;
  display: block;
  background-size: 64px;
  /* cyan-400 */
  /* filter: invert(71%) sepia(97%) saturate(1333%) hue-rotate(147deg) brightness(95%) contrast(96%); */
}

</style>