<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import debounce from 'lodash.debounce'
import { notificationHistory, notificationHistoryConfig } from '../socket'
import { darkModeEnabled } from '../settings.js'

const hasActivity = computed(() => notificationHistory.value.length > 0)
const rawNotificationHistory = computed(() => Array.from(notificationHistory.value))

const theSvg = ref()
const svgSize = ref(100)
const svgXPadding = 20
const rectWidth = computed(() => {
  return (svgSize.value - svgXPadding) / rawNotificationHistory.value.length
})
onMounted(() => {
    window.addEventListener('resize', () => debouncedSetSVGSize() )
    setSVGSize()
})
onUnmounted(() => {
    window.removeEventListener('resize', () => setSVGSize())
})

const debouncedSetSVGSize = debounce(setSVGSize, 400, { leading: true })
function setSVGSize() {
  if (theSvg.value.width) {
    svgSize.value = theSvg.value.width.baseVal.value
  }
}
</script>

<template>
  <div class="my-2 relative">
    <svg
      ref="theSvg"
      xmlns="http://www.w3.org/2000/svg"
      width="100%"
      height="40px"
      class="bg-slate-50 dark:bg-slate-600 rounded-md relative overflow-hidden"
    >
      <text 
        v-if="!hasActivity"
        :fill="darkModeEnabled ? '#94a3b8' : '#475569'" font-size="1rem" dominant-baseline="central" text-anchor="middle" x="50%" y="50%"
      >
        - No recorded activity -
      </text>
      <g>
        <rect v-for="(value, i) in rawNotificationHistory" :key="i"
          :x="(svgXPadding/2) + rectWidth * i" :y="36 - (Math.min(value, 30)/30) * 32" :width="rectWidth*0.8" :height="(Math.min(value, 30)/30) * 32"
          :fill="darkModeEnabled ? '#008ffb' : '#1f9eff'"
          :style="`filter: drop-shadow(2px 1px 2px rgba(0, 0, 0, ${darkModeEnabled ? 0.35 : 0.15}))`"
        />
      </g>
      <g v-if="hasActivity" style="user-select: none;">
        <text :fill="darkModeEnabled ? '#cbd5e1' : '#64748b'" font-size="0.66rem" text-anchor="middle" transform="translate(12, 20) rotate(-90)">- {{ notificationHistoryConfig.buffer_timestamp_min }}min</text>
        <text :fill="darkModeEnabled ? '#cbd5e1' : '#64748b'" font-size="0.5rem" text-anchor="middle" x="25%" y="40">|</text>
        <text :fill="darkModeEnabled ? '#cbd5e1' : '#64748b'" font-size="0.75rem" text-anchor="middle" x="50%" y="37">|</text>
        <text :fill="darkModeEnabled ? '#cbd5e1' : '#64748b'" font-size="0.5rem" text-anchor="middle" x="75%" y="40">|</text>
        <svg x="100%" style="overflow: visible;">
            <text :fill="darkModeEnabled ? '#cbd5e1' : '#64748b'" font-size="0.66rem" text-anchor="end" x="-7" y="-3" transform="rotate(-90)">- 0min</text>
        </svg>
      </g>
    </svg>
  </div>
</template>
