<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { state as socketState, socket, resetState, connectionState } from "@/socket";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faCheck, faTimes, faSignal, faGraduationCap, faCloud, faCog, faUser, faCircle } from '@fortawesome/free-solid-svg-icons'

const exercises = ref([])

const notifications = computed(() => socketState.notificationEvents)

const progresses = computed(() => socketState.progresses)

const user_count = computed(() => Object.keys(socketState.progresses).length)

function toggle_completed(completed, user_id, exec_uuid, task_uuid) {
  const payload = {
    user_id: user_id,
    exercise_uuid: exec_uuid,
    task_uuid: task_uuid,
  }
  const event_name = !completed ? "mark_task_completed": "mark_task_incomplete"
  socket.emit(event_name, payload, () => {
    socket.emit("get_progress", (all_progress) => {
      socketState.progresses = all_progress
    })
  })
}

function getClassFromResponseCode(response_code) {
  if (String(response_code).startsWith('2')) {
    return 'text-green-500'
  } else if (String(response_code).startsWith('5')) {
    return 'text-red-600'
  } else {
    return 'text-amber-600'
  }
}

function fullReload() {
  socket.emit("get_exercises", (all_exercises) => {
    exercises.value = all_exercises
  })
  socket.emit("get_notifications", (all_notifications) => {
    socketState.notificationEvents = all_notifications
  })
  socket.emit("get_progress", (all_progress) => {
    socketState.progresses = all_progress
  })
}

const socketConnected = computed(() => connectionState.connected)
watch(socketConnected, (isConnected) => {
  if (isConnected) {
    resetState()
    fullReload()
  }
})

onMounted(() => {
  fullReload()
})

</script>

<template>
  <h1 class="text-3xl font-bold text-center text-slate-600 dark:text-slate-300">MISP Exercise Dashboard</h1>

  <h3 class="text-2xl mt-6 mb-2 font-bold text-blue-500 dark:text-blue-400">
    <FontAwesomeIcon :icon="faGraduationCap"></FontAwesomeIcon>
    Active Exercises
  </h3>
  <table
    v-for="(exercise, exercise_index) in exercises"
    :key="exercise.name"
    class="bg-white dark:bg-slate-800 rounded-lg shadow-xl w-full mb-4"
  >
      <thead>
        <tr>
          <th :colspan="2 + exercise.tasks.length" class="rounded-t-lg border-b border-slate-100 dark:border-slate-700 text-md p-3 pl-6 text-center dark:bg-blue-800 bg-blue-500 dark:text-slate-300 text-slate-100">
            <div class="flex justify-between items-center">
              <span class="dark:text-blue-200 text-slate-200 "># {{ exercise_index + 1 }}</span>
              <span class="text-lg">{{ exercise.name }}</span>
              <span class="">
                Level: <span :class="{
                  'rounded-lg px-1 ml-2': true,
                  'dark:bg-sky-400 bg-sky-400 text-neutral-950': exercise.level == 'beginner',
                  'dark:bg-orange-400 bg-orange-400 text-neutral-950': exercise.level == 'advanced',
                  'dark:bg-red-600 bg-red-600 text-neutral-950': exercise.level == 'expert',
                }">{{ exercise.level }}</span>
              </span>
            </div>
          </th>
        </tr>
        <tr class="font-medium text-slate-600 dark:text-slate-200">
          <th class="border-b border-slate-100 dark:border-slate-700 p-3 pl-6 text-left">User</th>
          <th
            v-for="(task, task_index) in exercise.tasks"
            :key="task.name"
            class="border-b border-slate-100 dark:border-slate-700 p-3"
          >
            <div class="flex flex-col">
              <span class="text-center font-normal text-sm dark:text-blue-200 text-slate-500">Task {{ task_index + 1 }}</span>
              <i class="text-center">{{ task.name }}</i>
            </div>
          </th>
          <th class="border-b border-slate-100 dark:border-slate-700 p-3 text-left">Progress</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="Object.keys(progresses).length == 0">
          <td
            :colspan="2 + exercise.tasks.length"
            class="text-center border-b border-slate-100 dark:border-slate-700 text-slate-600 dark:text-slate-400 p-3 pl-6"
          >
            <i>- No user yet -</i>
          </td>
        </tr>
        <template v-else>
          <tr v-for="(progress, user_id) in progresses" :key="user_id">
            <td class="border-b border-slate-100 dark:border-slate-700 text-slate-600 dark:text-slate-400 p-3 pl-6">
              <span :title="user_id">
                <span class="text-lg font-bold font-mono">{{ progress.email.split('@')[0] }}</span>
                <span class="text-xs font-mono">@{{ progress.email.split('@')[1] }}</span>
              </span>
            </td>
            <td
              v-for="(task, task_index) in exercise.tasks"
              :key="task_index"
              class="text-center border-b border-slate-100 dark:border-slate-700 text-slate-500 dark:text-slate-400 p-3"
            >
            <span
              class="select-none cursor-pointer"
              @click="toggle_completed(progress.exercises[exercise.uuid].tasks_completion[task.uuid], user_id, exercise.uuid, task.uuid)"
            >
              <FontAwesomeIcon
                :icon="progress.exercises[exercise.uuid].tasks_completion[task.uuid] ? faCheck : faTimes"
                :class="`text-xl ${progress.exercises[exercise.uuid].tasks_completion[task.uuid] ? 'dark:text-green-400 text-green-600' : 'dark:text-slate-500 text-slate-400'}`"
              />
              <small :class="progress.exercises[exercise.uuid].tasks_completion[task.uuid] ? 'dark:text-green-400 text-green-600' : 'dark:text-slate-500 text-slate-400'"> (+{{ task.score }})</small>
            </span>
            </td>
            <td class="border-b border-slate-100 dark:border-slate-700 text-slate-500 dark:text-slate-400 p-3">
              <div class="flex w-full h-2 bg-gray-200 rounded-full overflow-hidden dark:bg-neutral-600" role="progressbar" :aria-valuenow="progress.exercises[exercise.uuid].percentage" :aria-valuemin="0" aria-valuemax="100">
                <div
                  class="flex flex-col justify-center rounded-full overflow-hidden bg-green-600 text-xs text-white text-center whitespace-nowrap transition duration-500 dark:bg-green-500 transition-width transition-slowest ease"
                  :style="`width: ${progress.exercises[exercise.uuid].score}%`"
                ></div>
              </div>
            </td>
          </tr>
        </template>
      </tbody>
    </table>

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
      <span class="font-bold">{{ user_count }}</span>
    </span>
    <span class="rounded-lg py-1 px-2 dark:bg-sky-700 bg-sky-400 text-slate-800 dark:text-slate-200">
      <span class="mr-1">
        <FontAwesomeIcon :icon="faSignal" size="sm"></FontAwesomeIcon>
        Total Queries:
      </span>
      <span class="font-bold">{{ socketState.notificationCounter }}</span>
    </span>
    <span class="rounded-lg py-1 px-2 dark:bg-sky-700 bg-sky-400 text-slate-800 dark:text-slate-200">
      <span class="mr-1">
        <FontAwesomeIcon :icon="faCog" size="sm" :mask="faCloud" transform="shrink-7 left-1"></FontAwesomeIcon>
        Total API Queries:
      </span>
      <span class="font-bold">{{ socketState.notificationAPICounter }}</span>
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
