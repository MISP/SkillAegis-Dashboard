<script setup>
</script>

<template>
     <label class="grid cursor-pointer place-items-center">
      <input
        type="checkbox"
        class="toggle theme-controller bg-slate-500 col-span-2 col-start-1 row-start-1 [--tglbg:#e2e8f0] dark:[--tglbg:#1d232a]" />
    </label>
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
  &[aria-checked="true"] {
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
    --togglehandleborder: 0 0 0 3px #000 inset,
      var(--handleoffsetcalculator) 0 0 3px #000 inset;
  }

  &-success {
    
  }
}

/* backward compatibility */
.toggle-mark {
  @apply hidden;
}
</style>