<script setup>
  import { ref, watch, computed } from "vue"
  import { userActivity, userActivityConfig } from "@/socket";
  import { darkModeEnabled } from "@/settings.js"

  const props = defineProps(['user_id'])

  const theChart = ref(null)
  const bufferSize = computed(() => userActivityConfig.value.activity_buffer_size)
  const bufferSizeMin = computed(() => userActivityConfig.value.timestamp_min)
  const chartInitSeries = Array.from(Array(bufferSize.value)).map(() => 0)
  
  const hasActivity = computed(() => userActivity.value.length != 0)
  const chartSeries = computed(() => {
    return !hasActivity.value ? chartInitSeries : activitySeries.value
  })

  const activitySeries = computed(() => {
    const data = userActivity.value[props.user_id] === undefined ? chartInitSeries : userActivity.value[props.user_id]
    return [{data: Array.from(data)}]
  })
  const colorRanges = [1, 3, 5, 7, 9, 1000]

  const chartOptions = computed(() => {
    return {
      chart: {
        height: 20,
        width: 208,
        type: 'heatmap',
        sparkline: {
          enabled: true
        },
        animations: {
            enabled: false,
            easing: 'easeinout',
            speed: 200,
        },
      },
      dataLabels: {
        enabled: false,
        style: {
          fontSize: '10px',
          fontWeight: '400',
        }
      },
      plotOptions: {
        heatmap: {
            radius: 2,
            enableShades: !true,
            shadeIntensity: 0.5,
            reverseNegativeShade: true,
            distributed: false,
            useFillColorAsStroke: false,
            colorScale: {
              ranges: [
                {
                  from: 0,
                  to: colorRanges[0],
                  color: darkModeEnabled.value ? '#172554' : '#bfdbfe',
                },
                {
                  from: colorRanges[0] + 1,
                  to: colorRanges[1],
                  color: darkModeEnabled.value ? '#1e40af' : '#93c5fd',
                },
                {
                  from: colorRanges[1] + 1,
                  to: colorRanges[2],
                  color: darkModeEnabled.value ? '#2563eb' : '#60a5fa',
                },
                {
                  from: colorRanges[2] + 1,
                  to: colorRanges[3],
                  color: darkModeEnabled.value ? '#3b82f6' : '#3b82f6',
                },
                {
                  from: colorRanges[3] + 1,
                  to: colorRanges[4],
                  color: darkModeEnabled.value ? '#60a5fa' : '#2563eb',
                },
                {
                  from: colorRanges[4] + 1,
                  to: colorRanges[5],
                  color: darkModeEnabled.value ? '#93c5fd' : '#1d4ed8',
                },
              ],
              // inverse: false,
              min: 0,
              max: 1000
            },
        },
      },
      states: {
        hover: {
          filter: {
            type: 'none',
          }
        },
        active: {
          filter: {
            type: 'none',
          }
        },
      },
      grid: {
        show: false,
      },
      legend: {
        show: true,
      },
      stroke: {
        width: 0,
      },
      tooltip: {
        enabled: false,
      },
    }
  })

</script>

<template>
  <span
    class="h-3 w-52"
    :title="`Activity over ${bufferSizeMin}min`"
  >
    <apexchart type="heatmap" height="12" width="208" :options="chartOptions" :series="chartSeries"></apexchart>
  </span>
</template>