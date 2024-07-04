<script setup>
  import { ref, computed } from "vue";
  import { active_exercises as exercises, progresses, setCompletedState } from "@/socket";
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
  import { faCheck, faTimes, faGraduationCap, faMedal, faHourglassHalf } from '@fortawesome/free-solid-svg-icons'

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

  const hasExercises = computed(() => exercises.value.length > 0)
  const hasProgress = computed(() => Object.keys(progresses.value).length > 0)

</script>

<template>
  <h3 class="text-2xl mt-6 mb-2 font-bold text-blue-500 dark:text-blue-400">
    <FontAwesomeIcon :icon="faGraduationCap"></FontAwesomeIcon>
    Active Exercises
  </h3>

  <div
    v-if="!hasExercises"
    class="text-center text-slate-600 dark:text-slate-400 p-3 pl-6"
  >
    <i>- No Exercise available -</i>
  </div>
  <table
    v-for="(exercise, exercise_index) in exercises"
    :key="exercise.name"
    class="bg-white dark:bg-slate-800 rounded-lg shadow-xl w-full mb-4"
  >
      <thead>
        <tr @click="collapse(exercise_index)" class="cursor-pointer">
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
        <tr :class="`font-medium text-slate-600 dark:text-slate-200 ${collapsed_panels.includes(exercise_index) ? 'hidden' : ''}`">
          <th class="border-b border-slate-100 dark:border-slate-700 p-3 pl-6 text-left">User</th>
          <th
            v-for="(task, task_index) in exercise.tasks"
            :key="task.name"
            class="border-b border-slate-100 dark:border-slate-700 p-3"
            :title="task.description"
          >
            <div class="flex flex-col">
              <span class="text-center font-normal text-sm dark:text-blue-200 text-slate-500">Task {{ task_index + 1 }}</span>
              <i class="text-center">{{ task.name }}</i>
            </div>
          </th>
          <th class="border-b border-slate-100 dark:border-slate-700 p-3 text-left">Progress</th>
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
          <tr v-for="(progress, user_id) in progresses" :key="user_id" class="bg-slate-100 dark:bg-slate-900">
            <td class="border-b border-slate-100 dark:border-slate-700 text-slate-600 dark:text-slate-400 p-3 pl-6">
              <span :title="user_id" class="text-nowrap">
                <FontAwesomeIcon v-if="progress.exercises[exercise.uuid].score / progress.exercises[exercise.uuid].max_score == 1" :icon="faMedal" class="mr-1 text-amber-300"></FontAwesomeIcon>
                <span class="text-lg font-bold font-mono">{{ progress.email.split('@')[0] }}</span>
                <span class="text-xs font-mono">@{{ progress.email.split('@')[1] }}</span>
              </span>
            </td>
            <td
              v-for="(task, task_index) in exercise.tasks"
              :key="task_index"
              class="text-center border-b border-slate-100 dark:border-slate-700 text-slate-500 dark:text-slate-400 p-2"
            >
            <span
              class="select-none cursor-pointer text-nowrap"
              @click="toggleCompleted(progress.exercises[exercise.uuid].tasks_completion[task.uuid], user_id, exercise.uuid, task.uuid)"
            >
              <span class="flex flex-col">
                <span>
                  <FontAwesomeIcon
                    v-if="progress.exercises[exercise.uuid].tasks_completion[task.uuid]"
                    :icon="faCheck"
                    :class="`text-xl ${progress.exercises[exercise.uuid].tasks_completion[task.uuid] ? 'dark:text-green-400 text-green-600' : 'dark:text-slate-500 text-slate-400'}`"
                  />
                  <FontAwesomeIcon
                    v-else-if="task.requirements?.inject_uuid !== undefined && !progress.exercises[exercise.uuid].tasks_completion[task.requirements.inject_uuid]"
                    title="All requirements for that task haven't been fullfilled yet"
                    :icon="faHourglassHalf"
                    :class="`text-lg ${progress.exercises[exercise.uuid].tasks_completion[task.uuid] ? 'dark:text-green-400 text-green-600' : 'dark:text-slate-500 text-slate-400'}`"
                  />
                  <FontAwesomeIcon
                    v-else
                    :icon="faTimes"
                    :class="`text-xl ${progress.exercises[exercise.uuid].tasks_completion[task.uuid] ? 'dark:text-green-400 text-green-600' : 'dark:text-slate-500 text-slate-400'}`"
                  />
                  <small :class="progress.exercises[exercise.uuid].tasks_completion[task.uuid] ? 'dark:text-green-400 text-green-600' : 'dark:text-slate-500 text-slate-400'"> (+{{ task.score }})</small>
                </span>
                <span class="text-sm leading-3">
                  <span
                    v-if="progress.exercises[exercise.uuid].tasks_completion[task.uuid].timestamp"
                    :class="progress.exercises[exercise.uuid].tasks_completion[task.uuid].first_completion ? 'font-bold' : 'font-extralight'"
                  >
                    {{ (new Date(progress.exercises[exercise.uuid].tasks_completion[task.uuid].timestamp * 1000)).toTimeString().split(' ', 1)[0] }}
                  </span>
                  <span v-else></span>
                </span>
              </span>
            </span>
            </td>
            <td class="border-b border-slate-100 dark:border-slate-700 text-slate-500 dark:text-slate-400 p-3">
              <div class="flex w-full h-2 bg-gray-200 rounded-full overflow-hidden dark:bg-neutral-600" role="progressbar" :aria-valuenow="progress.exercises[exercise.uuid].score" :aria-valuemin="0" aria-valuemax="100">
                <div
                  class="flex flex-col justify-center rounded-full overflow-hidden bg-green-600 text-xs text-white text-center whitespace-nowrap transition duration-500 dark:bg-green-500 transition-width transition-slowest ease"
                  :style="`width: ${100 * (progress.exercises[exercise.uuid].score / progress.exercises[exercise.uuid].max_score)}%`"
                ></div>
              </div>
            </td>
          </tr>
        </template>
      </tbody>
    </table>
</template>