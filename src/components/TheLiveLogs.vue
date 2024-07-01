<script setup>
  import { ref, computed, onMounted, watch } from 'vue'
  import { notifications, userCount, notificationCounter, notificationAPICounter } from "@/socket";
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
  import { faSignal, faCloud, faCog, faUser, faCircle } from '@fortawesome/free-solid-svg-icons'


  function getClassFromResponseCode(response_code) {
    if (String(response_code).startsWith('2')) {
      return 'text-green-500'
    } else if (String(response_code).startsWith('5')) {
      return 'text-red-600'
    } else {
      return 'text-amber-600'
    }
  }

</script>

<template>
  <h3 class="text-2xl mt-6 mb-2 font-bold text-blue-500 dark:text-blue-400">
    <FontAwesomeIcon :icon="faSignal"></FontAwesomeIcon>
    Live logs
  </h3>

  <div class="mb-2 flex flex-wrap gap-x-3">
    <span class="rounded-lg py-1 px-2 dark:bg-sky-700 bg-sky-400 text-slate-800 dark:text-slate-200">
      <span class="mr-1">
        <FontAwesomeIcon :icon="faUser" size="sm"></FontAwesomeIcon>
        User online:
      </span>
      <span class="font-bold">{{ userCount }}</span>
    </span>
    <span class="rounded-lg py-1 px-2 dark:bg-sky-700 bg-sky-400 text-slate-800 dark:text-slate-200">
      <span class="mr-1">
        <FontAwesomeIcon :icon="faSignal" size="sm"></FontAwesomeIcon>
        Total Queries:
      </span>
      <span class="font-bold">{{ notificationCounter }}</span>
    </span>
    <span class="rounded-lg py-1 px-2 dark:bg-sky-700 bg-sky-400 text-slate-800 dark:text-slate-200">
      <span class="mr-1">
        <FontAwesomeIcon :icon="faCog" size="sm" :mask="faCloud" transform="shrink-7 left-1"></FontAwesomeIcon>
        Total API Queries:
      </span>
      <span class="font-bold">{{ notificationAPICounter }}</span>
    </span>
  </div>

  <table class="bg-white dark:bg-slate-800 rounded-lg shadow-xl w-full">
      <thead>
        <tr class="font-medium dark:text-slate-200 text-slate-600 ">
          <th class="border-b border-slate-100 dark:border-slate-700 p-3 pl-6 text-left"></th>
          <th class="border-b border-slate-100 dark:border-slate-700 p-3 pl-2 text-left">User</th>
          <th class="border-b border-slate-100 dark:border-slate-700 p-3 text-left">Time</th>
          <th class="border-b border-slate-100 dark:border-slate-700 p-3 text-left">URL</th>
          <th class="border-b border-slate-100 dark:border-slate-700 p-3 text-left">Payload</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="Object.keys(notifications).length == 0">
          <td
            colspan="5"
            class="text-center border-b border-slate-100 dark:border-slate-700 text-slate-600 dark:text-slate-400 p-3 pl-6"
          >
            <i>- No logs yet -</i>
          </td>
        </tr>
        <template v-else>
          <tr v-for="(notification, index) in notifications" :key="index">
            <td
              class="border-b border-slate-100 dark:border-slate-700 text-slate-600 dark:text-slate-400 p-1 pl-2 w-12 whitespace-nowrap"
            >
              <FontAwesomeIcon :icon="faCircle" size="xs"
                :class="getClassFromResponseCode(notification.response_code)"
              ></FontAwesomeIcon>
              <pre class="inline ml-1">{{ notification.response_code }}</pre>
            </td>
            <td
              class="border-b border-slate-100 dark:border-slate-700 text-slate-600 dark:text-slate-400 p-1 pl-2"
              :title="notification.user_id"
            >
              <span class="text-lg font-bold font-mono">{{ notification.user.split('@')[0] }}</span>
              <span class="text-xs font-mono">@{{ notification.user.split('@')[1] }}</span>
            </td>
            <td class="border-b border-slate-100 dark:border-slate-700 text-slate-600 dark:text-slate-400 p-1">{{ notification.time }}</td>
            <td class="border-b border-slate-100 dark:border-slate-700 text-sky-600 dark:text-sky-400 p-1">
              <div class="flex items-center">
                <span v-if="notification.http_method == 'POST'"
                  class="p-1 rounded-md font-bold text-xs mr-2 w-10 inline-block text-center 
                         dark:bg-amber-600 dark:text-neutral-100 bg-amber-600 text-neutral-100"
                >POST</span>
                <span v-else-if="notification.http_method == 'DELETE'"
                  class="p-1 rounded-md font-bold text-xs mr-2 w-10 inline-block text-center 
                         dark:bg-red-600 dark:text-neutral-100 bg-red-600 text-neutral-100"
                >DEL</span>
                <span v-else
                  class="p-1 rounded-md font-bold text-xs mr-2 w-10 inline-block text-center 
                         dark:bg-blue-600 dark:text-neutral-100 bg-blue-600 text-neutral-100"
                >{{ notification.http_method }}</span>
                <FontAwesomeIcon
                  v-if="notification.is_api_request"
                  class="text-slate-800 dark:text-slate-100 mr-1 inline-block"
                  :icon="faCog" :mask="faCloud" transform="shrink-7 left-1"
                ></FontAwesomeIcon>
                <pre class="text-sm inline">{{ notification.url }}</pre>
              </div>
            </td>
            <td class="border-b border-slate-100 dark:border-slate-700 text-slate-600 dark:text-slate-300 p-1">
              <div v-if="notification.http_method == 'POST'"
                class="border border-slate-200 dark:border-slate-600 bg-slate-100 dark:bg-slate-600 rounded-md"
              >
                <pre
                  class="p-1 text-xs"
                >{{ JSON.stringify(notification.payload, null, 2) }}</pre>
              </div>
            </td>
          </tr>
        </template>
      </tbody>
    </table>
</template>