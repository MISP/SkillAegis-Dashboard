<script setup>
import { ref, watch, computed } from 'vue'
import {
  notifications,
  notificationCounter,
  notificationAPICounter,
  toggleVerboseMode,
  toggleApiQueryMode,
  userCount, userActivity,
  userActivityConfig,
  userAuthenticated
} from '../socket'
import {
  faSignal, faCloud, faCog, faUser, 
  faCogs,
  faDisplay,
} from '@fortawesome/free-solid-svg-icons'
import TheLiveLogsActivityGraphVue from './TheLiveLogsActivityGraph.vue'
import TheSocketConnectionState from '@/components/TheSocketConnectionState.vue'
import TheLogsTable from '@/components/logsViews/TheLogsTable.vue'
import Popover from '@/components/elements/Popover.vue'
import { fullscreenModeOn } from '../settings.js'

const verbose = ref(false)
const api_query = ref(false)
const full_screen = ref(false)

const bufferSize = computed(() => userActivityConfig.value.activity_buffer_size)

watch(verbose, (newValue) => {
  toggleVerboseMode(newValue == true)
})

watch(api_query, (newValue) => {
  toggleApiQueryMode(newValue == true)
})

function makeLogsFullScreen() {
  full_screen.value = !full_screen.value
  if (full_screen.value) {
    document.querySelector('.main-grid').classList.remove('default-template')
    document.querySelector('.main-grid').classList.add('logs-fullscreen-template')
  } else {
    document.querySelector('.main-grid').classList.remove('logs-fullscreen-template')
    document.querySelector('.main-grid').classList.add('default-template')
  }
}

</script>

<template>
  <div class="flex flex-col h-full overflow-hidden">
    <h3 class="text-2xl mb-1 font-title text-blue-500 dark:text-blue-400 uppercase inline-flex gap-x-2 items-center">
      <FontAwesomeIcon :icon="faSignal"></FontAwesomeIcon>
      Live Feed
      <TheSocketConnectionState></TheSocketConnectionState>
    </h3>

    <div class="mb-2 flex flex-wrap gap-x-2">
      <span class="rounded-lg py-1 px-2 dark:bg-cyan-800 bg-cyan-400 text-slate-800 dark:text-slate-200 shadow-strong">
        <span class="mr-1 font-title">
          <FontAwesomeIcon :icon="faSignal" size="sm"></FontAwesomeIcon>
          Messages
        </span>
        <span class="font-retrogaming">{{ notificationCounter }}</span>
      </span>
      <span class="rounded-lg py-1 px-2 dark:bg-cyan-800 bg-cyan-400 text-slate-800 dark:text-slate-200 shadow-strong">
        <span class="mr-1 font-title">
          <FontAwesomeIcon :icon="faCog" size="sm" :mask="faCloud" transform="shrink-7 left-1"></FontAwesomeIcon>
          API Messages
        </span>
        <span class="font-retrogaming">{{ notificationAPICounter }}</span>
      </span>
    </div>

    <div class="flex flex-row flex-nowrap gap-2 items-center mb-2">
      <Popover>
        <template #button="{ toggle }">
          <button @click="toggle" class="btn btn-info">
            <FontAwesomeIcon :icon="faCogs"></FontAwesomeIcon>
          </button>
        </template>

        <div class="flex flex-col gap-1">
          <span class="flex items-center">
            <label :class="`mr-1 flex items-center ${userAuthenticated ? 'cursor-pointer' : 'cursor-not-allowed'} text-slate-900 dark:text-slate-300 text-nowrap`">
              <input type="checkbox" class="toggle toggle-warning mr-2" :checked="verbose" :disabled="!userAuthenticated"
                :title="!userAuthenticated ? 'Authentication Required to use this functionality' : ''"
                @change="verbose = !verbose" />
              Verbose Mode
            </label>
          </span>
          <span class="flex items-center">
            <label :class="`mr-1 flex items-center ${userAuthenticated ? 'cursor-pointer' : 'cursor-not-allowed'} text-slate-900 dark:text-slate-300 text-nowrap`">
              <input type="checkbox" class="toggle toggle-success mr-2" :checked="api_query" :disabled="!userAuthenticated"
                :title="!userAuthenticated ? 'Authentication Required to use this functionality' : ''"
                @change="api_query = !api_query" />
              <FontAwesomeIcon :icon="faCog" size="sm" :mask="faCloud" transform="shrink-7 left-1" class="mr-1">
              </FontAwesomeIcon>
              Filter for API Queries
            </label>
          </span>
          <span class="flex items-center">
            <label class="mr-1 flex items-center cursor-pointer text-slate-900 dark:text-slate-300 text-nowrap">
              <input type="checkbox" class="toggle toggle-success mr-2" :checked="full_screen"
                @change="makeLogsFullScreen()" />
              <FontAwesomeIcon :icon="faDisplay" size="sm" class="mr-1">
              </FontAwesomeIcon>
              Fullscreen
            </label>
          </span>
        </div>
      </Popover>
      <div class="grow">
        <TheLiveLogsActivityGraphVue></TheLiveLogsActivityGraphVue>
      </div>
    </div>


    <TheLogsTable></TheLogsTable>
  </div>
</template>
