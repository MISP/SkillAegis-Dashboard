<script setup>
import { ref, watch, computed } from 'vue'
import {
  notifications,
  notificationCounter,
  notificationAPICounter,
  toggleVerboseMode,
  toggleApiQueryMode,
  userCount, userActivity,
  userActivityConfig
} from '../socket'
import {
  faSignal, faCloud, faCog, faUser, faUsers,
} from '@fortawesome/free-solid-svg-icons'
import TheLiveLogsActivityGraphVue from './TheLiveLogsActivityGraph.vue'
import TheSocketConnectionState from '@/components/TheSocketConnectionState.vue'
import TheLogsTable from '@/components/logsViews/TheLogsTable.vue'

const verbose = ref(false)
const api_query = ref(false)

const bufferSize = computed(() => userActivityConfig.value.activity_buffer_size)

watch(verbose, (newValue) => {
  toggleVerboseMode(newValue == true)
})

watch(api_query, (newValue) => {
  toggleApiQueryMode(newValue == true)
})

const userCountActive = computed(() => {
  let activeUserCount = 0
  Object.keys(userActivity.value).forEach(user_id => {
    const lastQuarterUserActivity = userActivity.value[user_id].slice(-parseInt(bufferSize.value/4))
    if (lastQuarterUserActivity.some(activity => activity > 0)) {
      activeUserCount += 1
    }
  });
  return activeUserCount
})
</script>

<template>
  <div class="flex flex-col h-full overflow-hidden">
    <h3 class="text-2xl mb-1 font-title text-blue-500 dark:text-blue-400 uppercase inline-flex gap-x-2 items-center">
      <FontAwesomeIcon :icon="faSignal"></FontAwesomeIcon>
      Live Feed
      <TheSocketConnectionState></TheSocketConnectionState>
    </h3>

    <div class="mb-2">
      <span class="rounded-lg py-1 px-2 dark:bg-cyan-800 bg-cyan-400 text-slate-800 dark:text-slate-200">
        <span class="mr-1 font-title">
          <FontAwesomeIcon :icon="faUsers" size="sm"></FontAwesomeIcon>
          Active Players
        </span>
        <span class="font-retrogaming">
          {{ userCountActive }}
        </span>
        <span class="font-retrogaming text-[0.62rem]"> / {{ userCount }}</span>
      </span>
    </div>

    <div class="mb-2 flex flex-wrap gap-x-2">
      <span class="rounded-lg py-1 px-2 dark:bg-cyan-800 bg-cyan-400 text-slate-800 dark:text-slate-200">
        <span class="mr-1 font-title">
          <FontAwesomeIcon :icon="faSignal" size="sm"></FontAwesomeIcon>
          Messages
        </span>
        <span class="font-retrogaming">{{ notificationCounter }}</span>
      </span>
      <span class="rounded-lg py-1 px-2 dark:bg-cyan-800 bg-cyan-400 text-slate-800 dark:text-slate-200">
        <span class="mr-1 font-title">
          <FontAwesomeIcon :icon="faCog" size="sm" :mask="faCloud" transform="shrink-7 left-1"></FontAwesomeIcon>
          API Messages
        </span>
        <span class="font-retrogaming">{{ notificationAPICounter }}</span>
      </span>
      <span class="flex items-center">
        <label class="mr-1 flex items-center cursor-pointer text-slate-700 dark:text-slate-300">
          <input type="checkbox" class="toggle toggle-warning mr-1" :checked="verbose" @change="verbose = !verbose" />
          Verbose
        </label>
      </span>
      <span class="flex items-center">
        <label class="mr-1 flex items-center cursor-pointer text-slate-700 dark:text-slate-300">
          <input type="checkbox" class="toggle toggle-success mr-1" :checked="api_query"
            @change="api_query = !api_query" />
          <FontAwesomeIcon :icon="faCog" size="sm" :mask="faCloud" transform="shrink-7 left-1" class="mr-1">
          </FontAwesomeIcon>
          API Queries
        </label>
      </span>
    </div>

    <TheLiveLogsActivityGraphVue></TheLiveLogsActivityGraphVue>

    <TheLogsTable></TheLogsTable>
  </div>
</template>
