<script setup>
import { ref, computed } from 'vue'
import { active_exercises as exercises, progresses, userCount, setCompletedState, userTaskCheckInProgress, userActivity, userActivityConfig } from '../../socket'
import { faCheck, faTimes, faMedal, faHourglassHalf, faUsersSlash, faAngleRight } from '@fortawesome/free-solid-svg-icons'
import { faCircleCheck } from '@fortawesome/free-regular-svg-icons'
import LiveLogsUserActivityGraph from '../LiveLogsUserActivityGraph.vue'
import UsernameFormatter from '@/components/elements/UsernameFormatter.vue'
import RelativeTimeFormatter from '@/components/elements/RelativeTimeFormatter.vue'

const props = defineProps(['exercise', 'exercise_index', 'hide_inactive_users'])

function toggleCompleted(completed, user_id, exec_uuid, task_uuid) {
  setCompletedState(completed, user_id, exec_uuid, task_uuid)
}

function getCompletetionPercentageForUser(progress, exercise_uuid) {
  return 100 * Object.values(progress.exercises[exercise_uuid].tasks_completion).filter(e => e !== false).length / Object.keys(progress.exercises[exercise_uuid].tasks_completion).length
}

const compactTable = computed(() => {
  return userCount.value > 17
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
  <table class="shadow-xl w-full mb-1">
    <thead>
      <tr
        class="font-medium text-slate-600 dark:text-slate-200 bg-white/80 dark:bg-slate-800/80"
      >
        <th class="border-b border-slate-100 dark:border-slate-700 p-3 pl-6 text-left"></th>
        <th
          v-for="task in exercise.tasks"
          :key="task.name"
          class="border-b border-slate-100 dark:border-slate-700 p-3 align-middle leading-5"
          :title="task.description"
        >
          <span class="text-center font-title">{{ task.name }}</span>
        </th>
      </tr>
    </thead>
    <tbody>
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
          class="bg-slate-50/80 dark:bg-slate-900/80"
        >
          <template v-if="progress.exercises[exercise.uuid] !== undefined">
            <td
              class="border-b border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-400 p-0 pl-2 relative max-w-64"
            >
              <span class="flex flex-col max-w-60">
                <span :title="progress.user_id" class="text-nowrap inline-flex flex-row flex-nowrap items-center leading-5 truncate">
                  <FontAwesomeIcon
                    v-if="
                      progress.exercises[exercise.uuid].score / progress.exercises[exercise.uuid].max_score == 1
                    "
                    :icon="faMedal"
                    class="mr-1 text-amber-300"
                  ></FontAwesomeIcon>
                  <UsernameFormatter :username="progress.email"></UsernameFormatter>
                  <FontAwesomeIcon :icon="faAngleRight" class="ml-2"></FontAwesomeIcon>
                </span>
                <LiveLogsUserActivityGraph
                  v-if="!compactTable"
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
                  </span>
                  <span :class="['leading-3', !compactTable ? 'text-xs' : 'text-[0.65rem]']">
                    <span
                      v-if="progress.exercises[exercise.uuid].tasks_completion[task.uuid].timestamp"
                      :class="
                        progress.exercises[exercise.uuid].tasks_completion[task.uuid].first_completion
                          ? 'font-bold'
                          : 'font-extralight'
                      "
                    >
                      <RelativeTimeFormatter :timestamp="parseInt(progress.exercises[exercise.uuid].tasks_completion[task.uuid].timestamp * 1000)"></RelativeTimeFormatter>
                    </span>
                  </span>
                </span>
              </span>
            </td>
          </template>
        </tr>
      </template>
    </tbody>
  </table>
</template>
