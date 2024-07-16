<script setup>
  import { ref, computed } from "vue";
  import { progresses, userCount } from "@/socket";
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
  import { faUsers } from '@fortawesome/free-solid-svg-icons'
  import { darkModeEnabled } from "@/settings.js"
  import LiveLogsUserActivityGraph from "./LiveLogsUserActivityGraph.vue"


  const compactGrid = computed(() => { return userCount.value > 70 })
  const sortedProgress = computed(() => Object.values(progresses.value).sort((a, b) => {
    if (a.email < b.email) {
      return -1;
    }
    if (a.email > b.email) {
      return 1;
    }
    return 0;
  }))
</script>

<template>
<div class="
  mt-2 px-2 pt-1 pb-2 rounded border
  bg-slate-100 border-slate-300 dark:bg-slate-600 dark:border-slate-800
">

  <h4 class="text-xl mb-2 font-bold text-blue-500 dark:text-blue-400">
    <FontAwesomeIcon :icon="faUsers"></FontAwesomeIcon>
    Active Players
  </h4>

  <div :class="`flex flex-wrap ${compactGrid ? 'gap-1' : 'gap-2'}`">
    <span
      v-for="(progress) in sortedProgress"
      :key="progress.user_id"
      class="bg-slate-200 dark:bg-slate-900 rounded border drop-shadow-lg border-slate-700"
    >
      <span class="
        flex p-2 mb-1
        text-slate-600 dark:text-slate-400
      ">
        <span :class="`flex flex-col ${compactGrid ? 'w-[120px]' : 'w-60'}`">
          <span :title="progress.user_id" class="text-nowrap inline-block leading-5 truncate">
            <span :class="`${compactGrid ? 'text-base' : 'text-lg'} font-bold font-mono leading-5 tracking-tight`">{{ progress.email.split('@')[0] }}</span>
            <span :class="`${compactGrid ? 'text-xs' : 'text-xs'} font-mono tracking-tight`">@{{ progress.email.split('@')[1] }}</span>
          </span>
          <LiveLogsUserActivityGraph
            :user_id="progress.user_id"
            :compact_view="compactGrid"
            :ultra_compact_view="false"
          ></LiveLogsUserActivityGraph>
        </span>
      </span>
    </span>
  </div>
</div>
</template>