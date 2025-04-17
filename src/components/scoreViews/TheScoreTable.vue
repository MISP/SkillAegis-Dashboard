<script setup>
import { ref, computed } from 'vue'
import { active_exercises as exercises, progresses, userCount, setCompletedState, userTaskCheckInProgress, userActivity, userActivityConfig } from '../../socket'
import { faCheck, faTimes, faMedal, faHourglassHalf } from '@fortawesome/free-solid-svg-icons'
import { faCircleCheck } from '@fortawesome/free-regular-svg-icons'
import LiveLogsUserActivityGraph from '../LiveLogsUserActivityGraph.vue'

const props = defineProps(['exercise', 'exercise_index', 'hide_inactive_users'])
const collapsed_panels = ref([])

function toggleCompleted(completed, user_id, exec_uuid, task_uuid) {
  setCompletedState(completed, user_id, exec_uuid, task_uuid)
}

function collapse(exercise_index) {
  const index = collapsed_panels.value.indexOf(exercise_index)
  if (index >= 0) {
    collapsed_panels.value.splice(index, 1)
  } else {
    collapsed_panels.value.push(exercise_index)
  }
}

function getCompletetionPercentageForUser(progress, exercise_uuid) {
  return 100 * Object.values(progress.exercises[exercise_uuid].tasks_completion).filter(e => e !== false).length / Object.keys(progress.exercises[exercise_uuid].tasks_completion).length
}

const compactTable = computed(() => {
  return userCount.value > 20
})
const hasProgress = computed(() => Object.keys(progresses.value).length > 0)
const sortedProgress = computed(() =>
  Object.values(progresses.value).sort((a, b) => {
    if (a.email < b.email) {
      return -1
    }
    if (a.email > b.email) {
      return 1
    }
    return 0
  })
)

const bufferSize = computed(() => userActivityConfig.value.activity_buffer_size)
const sortedInactiveProgress = computed(() =>
  props.hide_inactive_users ?
    sortedProgress.value.filter((progress) => {
      const user_id = progress.user_id
      if (userActivity.value[user_id] !== undefined) {
        
        const lastQuarterUserActivity = userActivity.value[user_id].slice(-parseInt(bufferSize.value/4))
        return lastQuarterUserActivity.some(activity => activity > 0)
      }
      return false
    }) :
    sortedProgress.value
)

const taskCompletionPercentages = computed(() => {
  const completions = {}
  Object.values(props.exercise.tasks).forEach((task) => {
    completions[task.uuid] = 0
  })

  sortedProgress.value.forEach((progress) => {
    if (progress.exercises[props.exercise.uuid] !== undefined) {
      for (const [taskUuid, taskCompletion] of Object.entries(
        progress.exercises[props.exercise.uuid].tasks_completion
      )) {
        if (taskCompletion !== false) {
          completions[taskUuid] += 1
        }
      }
    }
  })

  for (const [taskUuid, taskCompletionSum] of Object.entries(completions)) {
    completions[taskUuid] = 100 * (taskCompletionSum / userCount.value)
  }
  return completions
})
</script>

<template>
  <table class="bg-white dark:bg-slate-800 rounded-lg shadow-xl w-full mb-4">
    <thead>
      <tr @click="collapse(exercise_index)" class="cursor-pointer">
        <th
          :colspan="2 + exercise.tasks.length"
          class="rounded-tl-lg border-b border-slate-100 dark:border-slate-700 text-md p-3 pl-6 text-center dark:bg-blue-800 bg-blue-500 dark:text-slate-300 text-slate-100"
        >
          <div class="flex justify-centerx items-center">
            <span
              :class="{
                'rounded-lg px-1': true,
                'dark:bg-sky-400 bg-sky-400 text-neutral-950': exercise.level == 'beginner',
                'dark:bg-orange-400 bg-orange-400 text-neutral-950': exercise.level == 'advanced',
                'dark:bg-red-600 bg-red-600 text-neutral-100': exercise.level == 'expert'
              }"
              >{{ exercise.level }}
            </span>
            <span class="text-lg grow">{{ exercise.name }}</span>
          </div>
        </th>
      </tr>
      <tr
        :class="`font-medium text-slate-600 dark:text-slate-200 ${
          collapsed_panels.includes(exercise_index) ? 'hidden' : ''
        }`"
      >
        <th class="border-b border-slate-100 dark:border-slate-700 p-3 pl-6 text-left">User</th>
        <th
          v-for="(task, task_index) in exercise.tasks"
          :key="task.name"
          class="border-b border-slate-100 dark:border-slate-700 p-3 align-top"
          :title="task.description"
        >
          <div class="flex flex-col">
            <span
              class="text-center font-normal text-sm dark:text-blue-200 text-slate-500 text-nowrap"
              >Task {{ task_index + 1 }}</span
            >
            <i class="text-center">{{ task.name }}</i>
            <div
              role="progressbar"
              class="flex w-full h-1 bg-gray-200 rounded-full overflow-hidden dark:bg-neutral-600"
              :aria-valuenow="taskCompletionPercentages[task.uuid]"
              :aria-valuemin="0"
              aria-valuemax="100"
              :title="`${taskCompletionPercentages[task.uuid].toFixed(0)}%`"
            >
              <div
                class="flex flex-col justify-center rounded-full overflow-hidden bg-blue-600 text-xs text-white text-center whitespace-nowrap transition duration-500 dark:bg-blue-500 transition-width transition-slowest ease"
                :style="`width: ${taskCompletionPercentages[task.uuid]}%`"
              ></div>
            </div>
          </div>
        </th>
        <th style="width: 75px;"></th>
      </tr>
    </thead>
    <tbody :class="`${collapsed_panels.includes(exercise_index) ? 'hidden' : ''}`">
      <tr v-if="!hasProgress">
        <td
          :colspan="2 + exercise.tasks.length"
          class="text-center border-b border-slate-100 dark:border-slate-700 text-slate-600 dark:text-slate-400 p-3 pl-6"
        >
          <i>- No user yet -</i>
        </td>
      </tr>
      <template v-else>
        <tr
          v-for="progress in sortedInactiveProgress"
          :key="progress.user_id"
          class="bg-slate-50 dark:bg-slate-900"
        >
          <template v-if="progress.exercises[exercise.uuid] !== undefined">
            <td
              class="border-b border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-400 p-0 pl-2 relative"
            >
              <span class="flex flex-col max-w-60">
                <span :title="progress.user_id" class="text-nowrap inline-block leading-5 truncate">
                  <FontAwesomeIcon
                    v-if="
                      progress.exercises[exercise.uuid].score / progress.exercises[exercise.uuid].max_score == 1
                    "
                    :icon="faMedal"
                    class="mr-1 text-amber-300"
                  ></FontAwesomeIcon>
                  <span class="text-lg font-bold font-mono leading-5 tracking-tight">{{
                    progress.email.split('@')[0]
                  }}</span>
                  <span class="text-xs font-mono tracking-tight"
                    >@{{ progress.email.split('@')[1] }}</span
                  >
                </span>
                <LiveLogsUserActivityGraph
                  :user_id="progress.user_id"
                  :compact_view="compactTable"
                  :no_forced_width="true"
                ></LiveLogsUserActivityGraph>
              </span>
            </td>
            <td
              v-for="(task, task_index) in exercise.tasks"
              :key="task_index"
              :class="`text-center border-b border-slate-200 dark:border-slate-700 text-slate-500 dark:text-slate-400 ${
                compactTable ? 'p-0' : 'p-2'
              }`"
            >
              <span
                class="select-none cursor-pointer flex justify-center content-center flex-wrap h-9"
                @click="
                  toggleCompleted(
                    progress.exercises[exercise.uuid].tasks_completion[task.uuid],
                    progress.user_id,
                    exercise.uuid,
                    task.uuid
                  )
                "
              >
                <span class="flex flex-col">
                  <span class="text-nowrap">
                    <FontAwesomeIcon
                      v-if="progress.exercises[exercise.uuid].tasks_completion[task.uuid]"
                      :icon="
                        progress.exercises[exercise.uuid].tasks_completion[task.uuid].first_completion
                          ? faCircleCheck
                          : faCheck
                      "
                      :class="`
                        ${
                          progress.exercises[exercise.uuid].tasks_completion[task.uuid]
                            ? 'dark:text-green-400 text-green-600'
                            : 'dark:text-slate-500 text-slate-400'
                        }
                        ${
                          progress.exercises[exercise.uuid].tasks_completion[task.uuid]
                            .first_completion
                            ? 'text-lg'
                            : 'text-xl'
                        }
                      `"
                    />
                    <FontAwesomeIcon
                      v-else-if="
                        task.requirements?.inject_uuid !== undefined &&
                        !progress.exercises[exercise.uuid].tasks_completion[
                          task.requirements.inject_uuid
                        ]
                      "
                      title="All requirements for that task haven't been fullfilled yet"
                      :icon="faTimes"
                      :class="`text-xl ${
                        progress.exercises[exercise.uuid].tasks_completion[task.uuid]
                          ? 'dark:text-green-400 text-green-600'
                          : 'dark:text-slate-500 text-slate-400'
                      }`"
                    />
                    <FontAwesomeIcon
                      v-else
                      title="This task is ready to be fullfilled"
                      :icon="faHourglassHalf"
                      :class="`text-lg ${
                        progress.exercises[exercise.uuid].tasks_completion[task.uuid]
                          ? 'dark:text-green-400 text-green-600'
                          : 'dark:text-slate-500 text-slate-400'
                      }`"
                      :spin="userTaskCheckInProgress[`${progress.user_id}_${task.uuid}`]"
                    />
                    <small
                      :class="
                        progress.exercises[exercise.uuid].tasks_completion[task.uuid]
                          ? 'dark:text-green-400 text-green-600'
                          : 'dark:text-slate-500 text-slate-400'
                      "
                    >
                      (+{{ task.score }})</small
                    >
                  </span>
                  <span :class="['leading-3', !compactTable ? 'text-sm' : 'text-xs']">
                    <span
                      v-if="progress.exercises[exercise.uuid].tasks_completion[task.uuid].timestamp"
                      :class="
                        progress.exercises[exercise.uuid].tasks_completion[task.uuid].first_completion
                          ? 'font-bold'
                          : 'font-extralight'
                      "
                    >
                      {{
                        new Date(
                          progress.exercises[exercise.uuid].tasks_completion[task.uuid].timestamp *
                            1000
                        )
                          .toTimeString()
                          .split(' ', 1)[0]
                      }}
                    </span>
                  </span>
                </span>
              </span>
            </td>
            <td :class="`text-center border-b border-slate-200 dark:border-slate-700 text-slate-500 dark:text-slate-400 ${
                compactTable ? 'p-0' : 'p-2'
              }`">
              <div
                role="progressbar"
                class="flex w-full h-2 bg-gray-200 rounded-full overflow-hidden dark:bg-neutral-600"
                :aria-valuenow="25"
                :aria-valuemin="0"
                aria-valuemax="100"
                :title="`${getCompletetionPercentageForUser(progress, exercise.uuid).toFixed(0)}%`"
              >
                <div
                  class="flex flex-col justify-center rounded-full overflow-hidden bg-green-600 text-xs text-white text-center whitespace-nowrap transition duration-500 dark:bg-green-500 transition-width transition-slowest ease"
                  :style="`width: ${getCompletetionPercentageForUser(progress, exercise.uuid)}%`"
                ></div>
              </div>
            </td>
          </template>
        </tr>
      </template>
    </tbody>
  </table>
</template>
