<script setup>
import { ref, watch, computed } from 'vue'
import { userActivity, userActivityConfig } from '../socket'
import { darkModeEnabled } from '../settings.js'

const props = defineProps(['user_id', 'compact_view', 'ultra_compact_view', 'no_forced_width'])

const theChart = ref(null)
const bufferSize = computed(() => userActivityConfig.value.activity_buffer_size)
const bufferSizeMin = computed(() => userActivityConfig.value.timestamp_min)
const chartInitSeries = computed(() => Array.from(Array(bufferSize.value)).map(() => 0))

const hasActivity = computed(() => userActivity.value.length != 0)
const chartSeries = computed(() => {
  return !hasActivity.value ? chartInitSeries.value : activitySeries.value
})

const activitySeries = computed(() => {
  const data =
    userActivity.value[props.user_id] === undefined
      ? chartInitSeries.value
      : userActivity.value[props.user_id]
  return data
})

const colorRanges = [0, 1, 2, 3, 4, 5, 1000]
const palleteColor = 'blue'
const colorPalleteIndexDark = ['900', '700', '600', '500', '400', '300', '200']
const colorPalleteIndexLight = ['50', '100', '300', '400', '500', '600', '700']

function getPalleteIndexFromValue(value) {
  for (let palleteIndex = 0; palleteIndex < colorRanges.length; palleteIndex++) {
    const colorRangeValue = colorRanges[palleteIndex]
    if (value <= colorRangeValue) {
      return darkModeEnabled.value
        ? colorPalleteIndexDark[palleteIndex]
        : colorPalleteIndexLight[palleteIndex]
    }
  }
}
</script>

<template>
  <span
    :class="`${props.no_forced_width ? '' : (props.compact_view  ? 'w-[142px]' : 'w-[240px]')} ${props.compact_view ? 'h-1.5 inline-flex' : 'h-3'} whitespace-nowrap`"
    :title="`Activity over ${bufferSizeMin}min`"
  >
    <span
      v-for="(value, i) in chartSeries"
      :key="i"
      :class="[
        `inline-block rounded-[1px] mr-px`,
        props.compact_view ? 'h-1.5' : 'h-3',
        props.ultra_compact_view ? 'rounded-none' : '',
        `bg-${palleteColor}-${getPalleteIndexFromValue(value)}`
      ]"
      :style="`width: ${(((props.ultra_compact_view ? 142 : 240) - chartSeries.length) / chartSeries.length).toFixed(1)}px`"
    ></span>
  </span>
</template>
