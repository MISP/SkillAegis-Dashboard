<template>
    <div ref="popoverRef" class="relative inline-block">
      <slot name="button" :toggle="toggle">
        <button 
            @click="toggle" 
            class="btn btn-primary"
            aria-haspopup="true"
            :aria-expanded="isOpen.toString()"
        >
            {{ buttonText }}
        </button>
      </slot>
  
      <transition name="fade">
        <div
          v-if="isOpen"
          class="absolute z-10 mt-1 p-2 border dark:bg-slate-700 dark:border-slate-800 bg-slate-300 border-slate-400 rounded shadow-strong"
          role="menu"
        >
          <slot>
            <p class="p-4 dark:text-slate-200 text-slate-700">Popover content goes here.</p>
          </slot>
        </div>
      </transition>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onBeforeUnmount } from 'vue'
  
  const isOpen = ref(false)
  const popoverRef = ref(null)
  
  function toggle() {
    isOpen.value = !isOpen.value
  }
  
  function close() {
    isOpen.value = false
  }
  
  defineProps({
    buttonText: {
      type: String,
      default: 'Toggle Popover',
    },
  })
  
  // Detect clicks outside of popoverRef element
  function onClickOutside(event) {
    if (popoverRef.value && !popoverRef.value.contains(event.target)) {
      close()
    }
  }
  
  onMounted(() => {
    document.addEventListener('click', onClickOutside)
  })
  
  onBeforeUnmount(() => {
    document.removeEventListener('click', onClickOutside)
  })
  </script>
  
  <style>
  .fade-enter-active, .fade-leave-active {
    transition: opacity 0.15s ease;
  }
  .fade-enter-from, .fade-leave-to {
    opacity: 0;
  }
  </style>
  