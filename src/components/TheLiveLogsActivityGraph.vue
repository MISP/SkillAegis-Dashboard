<script setup>
  import { ref, watch, computed } from "vue"
  import { notificationHistory, notificationHistoryConfig } from "@/socket";
  import { darkModeEnabled } from "@/settings.js"

  const theChart = ref(null)
  const chartInitSeries = [
    {data: Array.from(Array(12*20)).map(()=> 0)}
  ]
  const hasActivity = computed(() => notificationHistory.value.length > 0)
  const chartSeries = computed(() => {
    return notificationHistory.value ? notificationHistorySeries.value : chartInitSeries.value
  })

  const notificationHistorySeries = computed(() => {
    return [{data: Array.from(notificationHistory.value)}]
  })

  const chartOptions = computed(() => {
    return {
      chart: {
        type: 'bar',
        width: '100%',
        height: 32,
        sparkline: {
          enabled: true
        },
        dropShadow: {
            enabled: true,
            enabledOnSeries: undefined,
            top: 2,
            left: 1,
            blur: 2,
            color: '#000',
            opacity: darkModeEnabled.value ? 0.35 : 0.15
        },
        animations: {
            enabled: false,
            easing: 'easeinout',
            speed: 200,
        },
      },
      colors: [darkModeEnabled.value ? '#008ffb' : '#1f9eff'],
      plotOptions: {
        bar: {
          columnWidth: '80%'
        }
      },
      yaxis: {
        min: 0,
        labels: {
          show: false,
        }
      },
      tooltip: {
        enabled: false,
      },
    }
  })

</script>

<template>
  <div class="my-2 --ml-1 bg-slate-50 dark:bg-slate-600 py-1 pl-1 pr-3 rounded-md relative flex flex-col">
    <div :class="`${!hasActivity ? 'hidden' : 'absolute'} h-10 -mt-1 w-full z-40`">
      <div class="text-xxs flex justify-between h-full items-center text-slate-500 dark:text-slate-300">
        <span class="-rotate-90 w-8 -ml-3">- {{ notificationHistoryConfig.buffer_timestamp_min }}min</span>
        <span class="-rotate-90 w-8 text-xs">–</span>
        <span class="-rotate-90 w-8 text-lg">–</span>
        <span class="-rotate-90 w-8 text-xs">–</span>
        <span class="-rotate-90 w-8 -mr-1.5">- 0min</span>
      </div>
    </div>
    <i :class="['text-center text-slate-600 dark:text-slate-400', hasActivity ? 'hidden' : 'block']">
      - No recorded activity -
    </i>
    <apexchart
        ref="theChart" :class="hasActivity ? 'block' : 'absolute h-8 w-full'" height="32" width="100%"
        :options="chartOptions"
        :series="chartSeries"
    ></apexchart>
  </div>
</template>