<script setup>
import { ref, watch, computed } from 'vue'
import {
  notifications,
  notificationCounter,
  notificationAPICounter,
  toggleVerboseMode,
  toggleApiQueryMode
} from '../socket'
import { faSignal, faCloud, faCog, faCircle, faUser, faLink, faBullhorn, faUserNinja } from '@fortawesome/free-solid-svg-icons'
import TheLiveLogsActivityGraphVue from './TheLiveLogsActivityGraph.vue'

const verbose = ref(false)
const api_query = ref(false)
const tracked_user = ref(null)
const tracked_url = ref(null)

const filtered_notifications = computed(() => {
  let filteredNotif = notifications.value
  if (tracked_user.value !== null && tracked_user.value.length > 0) {
    filteredNotif = filteredNotif.filter((notification) => {
      return notification.user.startsWith(tracked_user.value)
    })
  }
  if (tracked_url.value !== null && tracked_url.value.length > 0) {
    filteredNotif = filteredNotif.filter((notification) => {
      return notification.url.includes(tracked_url.value)
    })
  }
  return filteredNotif
})

watch(verbose, (newValue) => {
  toggleVerboseMode(newValue == true)
})

watch(api_query, (newValue) => {
  toggleApiQueryMode(newValue == true)
})

function getClassFromResponseCode(response_code) {
  if (String(response_code).startsWith('2') || response_code == 302) {
    return 'text-green-500'
  } else if (String(response_code).startsWith('5')) {
    return 'text-red-600'
  } else if (String(response_code).startsWith('4')) {
    return 'text-amber-600'
  } else {
    return 'text-blue-600'
  }
}

function convertToLocalTime(serverTime) {
  let [hours, minutes, seconds] = serverTime.split(":").map(Number);
  let now = new Date();
  let serverDate = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate(), hours, minutes, seconds));
  let localDate = new Date(serverDate);
  return localDate.toLocaleTimeString(undefined, { hour12: false });
}
</script>

<template>
  <div>
    <h3 class="text-2xl mt-6 mb-2 font-bold text-blue-500 dark:text-blue-400 uppercase">
      <FontAwesomeIcon :icon="faSignal"></FontAwesomeIcon>
      Live logs
    </h3>

    <div class="mb-2 flex flex-wrap gap-x-3">
      <span
        class="rounded-lg py-1 px-2 dark:bg-sky-700 bg-sky-400 text-slate-800 dark:text-slate-200"
      >
        <span class="mr-1">
          <FontAwesomeIcon :icon="faSignal" size="sm"></FontAwesomeIcon>
          Total Queries:
        </span>
        <span class="font-bold">{{ notificationCounter }}</span>
      </span>
      <span
        class="rounded-lg py-1 px-2 dark:bg-sky-700 bg-sky-400 text-slate-800 dark:text-slate-200"
      >
        <span class="mr-1">
          <FontAwesomeIcon
            :icon="faCog"
            size="sm"
            :mask="faCloud"
            transform="shrink-7 left-1"
          ></FontAwesomeIcon>
          Total API Queries:
        </span>
        <span class="font-bold">{{ notificationAPICounter }}</span>
      </span>
      <span class="flex items-center">
        <label class="mr-1 flex items-center cursor-pointer text-slate-700 dark:text-slate-300">
          <input
            type="checkbox"
            class="toggle toggle-warning mr-1"
            :checked="verbose"
            @change="verbose = !verbose"
          />
          Verbose
        </label>
      </span>
      <span class="flex items-center">
        <label class="mr-1 flex items-center cursor-pointer text-slate-700 dark:text-slate-300">
          <input
            type="checkbox"
            class="toggle toggle-success mr-1"
            :checked="api_query"
            @change="api_query = !api_query"
          />
          <FontAwesomeIcon
            :icon="faCog"
            size="sm"
            :mask="faCloud"
            transform="shrink-7 left-1"
            class="mr-1"
          ></FontAwesomeIcon>
          API Queries
        </label>
      </span>
    </div>

    <TheLiveLogsActivityGraphVue></TheLiveLogsActivityGraphVue>

    <table class="bg-white dark:bg-slate-800 rounded-lg shadow-xl w-full">
      <thead>
        <tr class="font-medium dark:text-slate-200 text-slate-600">
          <th class="border-b border-slate-100 dark:border-slate-700 p-3 pl-6 text-left"></th>
          <th class="border-b border-slate-100 dark:border-slate-700 p-3 pl-2 text-left">
            User
            <span class="flex items-center">
              <label class="mr-1 relative flex items-center cursor-pointer">
                <FontAwesomeIcon
                  :icon="faUser"
                  size="sm"
                  class="absolute left-2 text-slate-400 dark:text-slate-300"
                ></FontAwesomeIcon>
                <input
                  type="text"
                  class="
                    shadow border font-mono w-full rounded py-1 pl-7 pr-2 leading-tight
                    bg-slate-50 text-slate-700 border-slate-300
                    dark:bg-slate-500 dark:text-slate-200 dark:border-slate-400
                    focus:outline-none focus:border focus:border-slate-300 focus:dark:border-slate-300
                  "
                  placeholder="Track User"
                  v-model="tracked_user"
                />
              </label>
            </span>
          </th>
          <th class="border-b border-slate-100 dark:border-slate-700 p-3 text-left">Time</th>
          <th class="border-b border-slate-100 dark:border-slate-700 p-3 text-left">
            URL
            <span class="flex items-center">
              <label class="mr-1 relative flex items-center cursor-pointer">
                <FontAwesomeIcon
                  :icon="faLink"
                  size="sm"
                  class="absolute left-2 text-slate-400 dark:text-slate-300"
                ></FontAwesomeIcon>
                <input
                  type="text"
                  class="
                    shadow border font-mono w-full rounded py-1 pl-7 pr-2 leading-tight
                    bg-slate-50 text-slate-700 border-slate-300
                    dark:bg-slate-500 dark:text-slate-200 dark:border-slate-400
                    focus:outline-none focus:border focus:border-slate-300 focus:dark:border-slate-300
                  "
                  placeholder="Track URL"
                  v-model="tracked_url"
                />
              </label>
            </span>
          </th>
          <th class="border-b border-slate-100 dark:border-slate-700 p-3 text-left">Payload</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="notifications.length == 0">
          <td
            colspan="5"
            class="text-center border-b border-slate-100 dark:border-slate-700 text-slate-600 dark:text-slate-400 p-3 pl-6"
          >
            <i>- No logs yet -</i>
          </td>
        </tr>
        <template v-else>
          <tr v-for="notification in filtered_notifications" :key="notification.id">
            <td
              class="border-b border-slate-100 dark:border-slate-700 text-slate-600 dark:text-slate-400 p-1 pl-2 w-12 whitespace-nowrap"
            >
              <FontAwesomeIcon
                :icon="faCircle"
                size="xs"
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
            <td
              class="border-b border-slate-100 dark:border-slate-700 text-slate-600 dark:text-slate-400 p-1"
            >
              {{ convertToLocalTime(notification.time) }}
            </td>
            <td
              class="border-b border-slate-100 dark:border-slate-700 text-sky-600 dark:text-sky-400 p-1"
            >
              <div class="flex items-center">
                <template v-if="notification.notification_origin == 'zmq'">
                  <span
                    v-if="notification.http_method == 'POST'"
                    class="p-1 rounded-md font-bold text-xs mr-2 w-10 inline-block text-center dark:bg-amber-600 dark:text-neutral-100 bg-amber-600 text-neutral-100"
                    >POST</span
                  >
                  <span
                    v-else-if="notification.http_method == 'PUT'"
                    class="p-1 rounded-md font-bold text-xs mr-2 w-10 inline-block text-center dark:bg-amber-600 dark:text-neutral-100 bg-amber-600 text-neutral-100"
                    >PUT</span
                  >
                  <span
                    v-else-if="notification.http_method == 'DELETE'"
                    class="p-1 rounded-md font-bold text-xs mr-2 w-10 inline-block text-center dark:bg-red-600 dark:text-neutral-100 bg-red-600 text-neutral-100"
                    >DEL</span
                  >
                  <span
                    v-else
                    class="p-1 rounded-md font-bold text-xs mr-2 w-10 inline-block text-center dark:bg-blue-600 dark:text-neutral-100 bg-blue-600 text-neutral-100"
                    >{{ notification.http_method }}</span
                  >
                  <FontAwesomeIcon
                    v-if="notification.is_api_request"
                    class="text-slate-800 dark:text-slate-100 mr-1 inline-block"
                    :icon="faCog"
                    :mask="faCloud"
                    transform="shrink-7 left-1"
                  ></FontAwesomeIcon>
                  <pre class="text-sm inline max-w-96 overflow-hidden text-ellipsis">{{ notification.url }}</pre>
                </template>
                <template v-else-if="notification.notification_origin == 'webhook'">
                  <FontAwesomeIcon
                    class="text-slate-800 dark:text-slate-100 mr-1 inline-block"
                    :icon="faBullhorn"
                  ></FontAwesomeIcon>
                  <pre class="text-sm inline max-w-96 overflow-hidden text-ellipsis">Webhook for {{ notification.target_tool }}</pre>
                </template>
              </div>
            </td>
            <td
              class="border-b border-slate-100 dark:border-slate-700 text-slate-600 dark:text-slate-300 p-1"
            >
              <div
                v-if="notification.http_method == 'POST' || notification.notification_origin == 'webhook'"
              >
              <!-- FIXME: Make that part more generic -->
              <Alert variant="danger" class="mx-2 mt-2"
                v-if="notification.payload === 'string' && !notification.payload.includes('trying to cheat')"
              >
                <strong>User  {{ notification.user }} is trying to cheat <FontAwesomeIcon :icon="faUserNinja"></FontAwesomeIcon></strong>
                <div class="text-sm"><span class="">User {{ notification.user }} is trying to cheat or hasn't reset their Event before sending it for validation.</span></div>
              </Alert>
                <div
                  class="border border-slate-200 dark:border-slate-600 bg-slate-100 dark:bg-slate-600 rounded-md"
                >
                  <pre
                    class="p-1 text-xs max-w-3xl overflow-hidden text-ellipsis"
                  >{{ typeof(notification.payload) === "string" ? notification.payload : JSON.stringify(notification.payload, null, 2) }}</pre>
                </div>
              </div>
            </td>
          </tr>
        </template>
      </tbody>
    </table>
  </div>
</template>
