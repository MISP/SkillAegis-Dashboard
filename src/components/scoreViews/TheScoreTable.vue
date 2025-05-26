<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { active_exercises as exercises, progresses, userCount, setCompletedState, userTaskCheckInProgress, userActivity, userActivityConfig, } from '../../socket'
import { faCheck, faTimes, faMedal, faHourglassHalf, faUsersSlash, faAngleRight, faCircle, faCaretLeft, faCaretRight, faUsers } from '@fortawesome/free-solid-svg-icons'
import { faCircleCheck, faCircle as faCircleHole } from '@fortawesome/free-regular-svg-icons'
import LiveLogsUserActivityGraph from '../LiveLogsUserActivityGraph.vue'
import UsernameFormatter from '@/components/elements/UsernameFormatter.vue'
import RelativeTimeFormatter from '@/components/elements/RelativeTimeFormatter.vue'
import UserScore from '@/components/elements/UserScore.vue'
import FireBadge from '@/components/elements/FireBadge.vue'
import { registerTimerCallback, unregisterTimerCallback } from '@/utils.js';

const props = defineProps(['exercise', 'exercise_index', 'hide_inactive_users', 'enable_automatic_pagination', 'sort_by_score'])

function toggleCompleted(completed, user_id, exec_uuid, task_uuid) {
  setCompletedState(completed, user_id, exec_uuid, task_uuid)
}

function getCompletetionPercentageForUser(progress, exercise_uuid) {
  return 100 * Object.values(progress.exercises[exercise_uuid].tasks_completion).filter(e => e !== false).length / Object.keys(progress.exercises[exercise_uuid].tasks_completion).length
}

const sortedProgressByScore = computed(() => {
  const allProgress = {}
  for (const exercise of Object.values(exercises.value)) {
    allProgress[exercise.uuid] = []
  }

  for (const { email, exercises: userExercises } of Object.values(progresses.value)) {
    for (const [uuid, progress] of Object.entries(userExercises)) {
      allProgress[uuid]?.push({
        email,
        exercises: { [uuid]: progress }
      })
    }
  }

  for (const [uuid, progresses] of Object.entries(allProgress)) {
    progresses.sort((a, b) => {
      const scoreA = a.exercises[uuid]?.score ?? 0
      const scoreB = b.exercises[uuid]?.score ?? 0
      return scoreA - scoreB
    })
  }

  return allProgress
})

const tbodyRef = ref(null);
const visibleRowCount = ref(17)

const updateVisibleRowCount = () => {
  nextTick(() => {
    if (window.getComputedStyle(tbodyRef.value.parentElement).display === 'none') {
      return
    }
    const tableBodyTop = tbodyRef.value?.getBoundingClientRect().top || 0;
    const windowHeight = window.innerHeight;
    const availableHeight = windowHeight - tableBodyTop;
    const firstRow = tbodyRef.value.children[0];
    if (firstRow) {
      const rowHeight = firstRow.getBoundingClientRect().height;
      visibleRowCount.value = Math.floor(availableHeight / rowHeight);
    }
  });
};

const compactTable = computed(() => {
  return sortedInactiveProgress.value.length > visibleRowCount.value && props.enable_automatic_pagination === false
})
const hasProgress = computed(() => Object.keys(progresses.value).length > 0)
const sortedProgressByEmail = computed(() =>
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
    sortedProgressByEmail.value.filter((progress) => {
      const user_id = progress.user_id
      if (userActivity.value[user_id] !== undefined) {
        
        const lastQuarterUserActivity = userActivity.value[user_id].slice(-parseInt(bufferSize.value/4))
        return lastQuarterUserActivity.some(activity => activity > 0)
      }
      return false
    }) :
    sortedProgressByEmail.value
)

let timerID = null
let visibleRowUpdater = null
const currentPage = ref(0)
const paginatedScoreTable = computed(() => {
  if (props.enable_automatic_pagination === false) {
    return sortedInactiveProgress.value
  } else {
    if (sortedInactiveProgress.value.length > 0) {
      return sortedInactiveProgress.value.slice(currentPage.value * visibleRowCount.value, (currentPage.value + 1) * visibleRowCount.value)
    }
    return []
  }
})
function updatePage() {
  currentPage.value = (currentPage.value + 1) % Math.ceil(sortedInactiveProgress.value.length / visibleRowCount.value)
}
const pageTotal = computed(() => {
  return Math.ceil(sortedInactiveProgress.value.length / visibleRowCount.value)
})

function paginatedScoreTableRouter(exercise_uuid) {
  if (props.sort_by_score === true) {
    return sortedProgressByScore.value[exercise_uuid]
  } else {
    return  paginatedScoreTable.value
  }
}

const taskCompletionPercentages = computed(() => {
  const completions = {}
  Object.values(props.exercise.tasks).forEach((task) => {
    completions[task.uuid] = 0
  })

  sortedProgressByEmail.value.forEach((progress) => {
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

const userCountActive = computed(() => {
  let activeUserCount = 0
  Object.keys(userActivity.value).forEach(user_id => {
    const lastQuarterUserActivity = userActivity.value[user_id].slice(-parseInt(bufferSize.value / 4))
    if (lastQuarterUserActivity.some(activity => activity > 0)) {
      activeUserCount += 1
    }
  });
  return activeUserCount
})

onMounted(() => {
  updateVisibleRowCount()
  setTimeout(() => {
    updateVisibleRowCount()
  }, 200);
  visibleRowUpdater = setInterval(() => {
    updateVisibleRowCount()
  }, 5000);
  window.addEventListener('resize', updateVisibleRowCount)
  timerID = registerTimerCallback(updatePage)
})
onUnmounted(() => {
  window.removeEventListener('resize', updateVisibleRowCount)
  unregisterTimerCallback(timerID)
  clearInterval(visibleRowUpdater)
})

</script>

<template>
  <table class="shadow-xl w-full mb-1">
    <thead>
      <tr
        class="font-medium text-slate-600 dark:text-slate-200 bg-white/80 dark:bg-slate-800/80"
      >
        <th class="border-b border-slate-100 dark:border-slate-700 p-3 pl-3 text-left">
          <span class="flex flex-col gap-2 items-center">
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
            <span class="flex flex-row flex-nowrap items-center gap-1 text-cyan-600" v-if="props.enable_automatic_pagination">
                <FontAwesomeIcon
                  v-if="pageTotal > 1"
                  @click="currentPage = currentPage - 1 < 0 ? pageTotal - 1 : currentPage - 1"
                  :icon="faCaretLeft"
                  class="cursor-pointer"
                  size="lg"
                ></FontAwesomeIcon>
                <FontAwesomeIcon
                  v-for="i in pageTotal"
                  :key="i"
                  @click="currentPage = i - 1"
                  :icon="i-1 == currentPage ? faCircle : faCircleHole"
                  class="cursor-pointer"
                ></FontAwesomeIcon>
                <FontAwesomeIcon
                  v-if="pageTotal > 1"
                  @click="currentPage = (currentPage + 1) % Math.ceil(sortedInactiveProgress.length / visibleRowCount)"
                  :icon="faCaretRight"
                  class="cursor-pointer"
                  size="lg"
                ></FontAwesomeIcon>
              </span>
            </span>
        </th>
        <th
          v-for="task in exercise.tasks"
          :key="task.name"
          class="border-b border-slate-100 dark:border-slate-700 p-3 align-middle leading-5"
          :title="task.description"
        >
          <span class="text-center font-title select-none inline-block max-h-16 overflow-y-hidden text-ellipsis">{{ task.name }}</span>
        </th>
        <th class="border-b border-slate-100 dark:border-slate-700 p-3 pl-3 text-right"></th>
      </tr>
    </thead>
    <tbody ref="tbodyRef">
      <tr v-if="!hasProgress || sortedInactiveProgress.length == 0">
        <td
          :colspan="2 + exercise.tasks.length"
          class="text-center border-b border-slate-100 dark:border-slate-700 text-slate-600 dark:text-slate-300 p-3 pl-6"
        >
          <Alert v-if="sortedInactiveProgress.length == 0" variant="warning">
            No user with recent activity
          </Alert>
          <Alert v-else variant="warning">No user yet</Alert>
        </td>
      </tr>
      <template v-else>
        <tr
          v-for="progress in paginatedScoreTableRouter(exercise.uuid)"
          :key="progress.user_id"
          class="bg-slate-50/80 dark:bg-slate-900/80"
        >
          <template v-if="progress.exercises[exercise.uuid] !== undefined">
            <td
              class="border-b border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-400 p-0 pl-2 relative max-w-64"
            >
              <span class="flex flex-col max-w-60">
                <span :title="progress.user_id" class="text-nowrap inline-flex flex-row flex-nowrap items-center leading-5 truncate select-none">
                  <FontAwesomeIcon
                    v-if="
                      progress.exercises[exercise.uuid].score / progress.exercises[exercise.uuid].max_score == 1
                    "
                    :icon="faMedal"
                    class="mr-1 text-amber-300"
                  ></FontAwesomeIcon>
                  <FireBadge
                    v-if="progress?.state?.on_fire" class="mr-1"></FireBadge>
                  <UsernameFormatter :username="progress.email" class="text-2xl"></UsernameFormatter>
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
            <td :class="`text-center border-b border-slate-200 dark:border-slate-700 text-slate-500 dark:text-slate-400 ${
                compactTable ? 'p-1' : 'p-2'
              }`">
              <UserScore
                :score="progress.exercises[exercise.uuid].score"
                :max_score="progress.exercises[exercise.uuid].max_score"
              ></UserScore>
            </td>
          </template>
        </tr>
      </template>
    </tbody>
  </table>
</template>
