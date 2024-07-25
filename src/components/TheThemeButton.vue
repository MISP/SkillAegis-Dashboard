<script setup>
import { ref, watch } from 'vue'
import { faMoon, faSun } from '@fortawesome/free-solid-svg-icons'
import { darkModeOn } from '../settings.js'

const darkMode = ref(darkModeOn.value)

watch(darkMode, (newValue) => {
  darkModeOn.value = newValue
  if (newValue) {
    document.getElementsByTagName('body')[0].classList.add('dark')
  } else {
    document.getElementsByTagName('body')[0].classList.remove('dark')
  }
})
</script>

<template>
  <div class="flex">
    <label class="grid cursor-pointer place-items-center">
      <input
        type="checkbox"
        @click="darkMode = !darkMode"
        :checked="darkMode"
        class="toggle theme-controller bg-slate-500 col-span-2 col-start-1 row-start-1 [--tglbg:#e2e8f0] dark:[--tglbg:#1d232a]"
      />
      <svg
        class="stroke-slate-800 dark:stroke-slate-100 fill-slate-800 dark:fill-slate-100 col-start-1 row-start-1"
        xmlns="http://www.w3.org/2000/svg"
        width="14"
        height="14"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <circle cx="12" cy="12" r="5" />
        <path
          d="M12 1v2M12 21v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M1 12h2M21 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"
        />
      </svg>
      <svg
        class="dark:stroke-slate-800 stroke-slate-700 dark:fill-slate-800 fill-slate-700 col-start-2 row-start-1"
        xmlns="http://www.w3.org/2000/svg"
        width="14"
        height="14"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
      </svg>
    </label>
  </div>
</template>

<style scoped>
.toggle {
  --animation-input: 0.2s;
  --handleoffset: 1.5rem;
  --handleoffsetcalculator: calc(var(--handleoffset) * -1);
  --togglehandleborder: 0 0;
  @apply h-6 w-12 rounded-3xl cursor-pointer appearance-none border border-current bg-current;
  transition:
    background,
    box-shadow var(--animation-input, 0.2s) ease-out;
  box-shadow:
    var(--handleoffsetcalculator) 0 0 2px var(--tglbg) inset,
    0 0 0 2px var(--tglbg) inset,
    var(--togglehandleborder);
  &:focus-visible {
    @apply outline outline-2 outline-offset-2;
  }
  &:hover {
    @apply bg-current;
  }
  &:checked,
  &[aria-checked='true'] {
    background-image: none;
    --handleoffsetcalculator: var(--handleoffset);
  }
  &:indeterminate {
    box-shadow:
      calc(var(--handleoffset) / 2) 0 0 2px var(--tglbg) inset,
      calc(var(--handleoffset) / -2) 0 0 2px var(--tglbg) inset,
      0 0 0 2px var(--tglbg) inset;
  }
  &:disabled {
    @apply cursor-not-allowed bg-transparent opacity-30;
    --togglehandleborder: 0 0 0 3px #000 inset, var(--handleoffsetcalculator) 0 0 3px #000 inset;
  }
}
</style>
