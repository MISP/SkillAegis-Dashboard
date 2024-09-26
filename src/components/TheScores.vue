<script setup>
import { ref, computed } from 'vue'
import { active_exercises as exercises, userCount, userActivity, userActivityConfig } from '../socket'
import {
  faGraduationCap,
  faUpRightAndDownLeftFromCenter,
  faDownLeftAndUpRightToCenter,
  faWarning,
  faUsers,
  faUsersSlash
} from '@fortawesome/free-solid-svg-icons'
import TheScoreTable from './scoreViews/TheScoreTable.vue'
import TheFullScreenScoreGrid from './scoreViews/TheFullScreenScoreGrid.vue'
import ThePlayerGrid from './ThePlayerGrid.vue'
import { fullscreenModeOn } from '../settings.js'

const hasExercises = computed(() => exercises.value.length > 0)
const fullscreen_panel = ref(false)
const hide_inactive_users = ref(false)

const bufferSize = computed(() => userActivityConfig.value.activity_buffer_size)
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

function toggleFullScreen(exercise_index) {
  if (fullscreen_panel.value === exercise_index) {
    fullscreen_panel.value = false
    fullscreenModeOn.value = false
  } else {
    fullscreen_panel.value = exercise_index
    fullscreenModeOn.value = true
  }
}
</script>

<template>
  <h3 class="text-2xl mt-6 mb-2 font-bold text-blue-500 dark:text-blue-400 uppercase">
    <FontAwesomeIcon :icon="faGraduationCap"></FontAwesomeIcon>
    Active Exercises
  </h3>

  <div v-if="!hasExercises" class="text-slate-600 dark:text-slate-400 p-3 pl-6">
    <Alert variant="warning">
      <strong class="">No Exercise available.</strong>
      <span class="ml-1">Select an exercise in the <i class="underline">Admin panel</i>.</span>
    </Alert>

    <ThePlayerGrid></ThePlayerGrid>
  </div>

  <div class="mb-2 flex flex-wrap gap-x-3">
    <span
      class="rounded-lg py-1 px-2 dark:bg-sky-700 bg-sky-400 text-slate-800 dark:text-slate-200"
    >
      <span class="mr-1">
        <FontAwesomeIcon :icon="faUsers" size="sm"></FontAwesomeIcon>
        Players:
      </span>
      <span class="font-bold">{{ userCount }}</span>
    </span>

    <span
      class="rounded-lg py-1 px-2 dark:bg-green-700 bg-green-400 text-slate-800 dark:text-slate-200"
    >
      <span class="mr-1">
        <FontAwesomeIcon :icon="faUsers" size="sm"></FontAwesomeIcon>
        Active Players:
      </span>
      <span class="font-bold">{{ userCountActive }}</span>
    </span>

    <label class="mr-1 flex items-center cursor-pointer text-slate-700 dark:text-slate-300">
      <input
        type="checkbox"
        class="toggle toggle-success mr-1"
        :checked="hide_inactive_users"
        @change="hide_inactive_users = !hide_inactive_users"
      />
      <FontAwesomeIcon :icon="faUsersSlash" size="sm" class="mr-1"></FontAwesomeIcon>
      Hide inactive users
    </label>
  </div>

  <template v-for="(exercise, exercise_index) in exercises" :key="exercise.name">
    <div :class="fullscreen_panel === false ? 'relative min-w-fit' : ''">
      <span
        v-show="fullscreen_panel === false || fullscreen_panel === exercise_index"
        :class="[
          'inline-block absolute shadow-lg z-50',
          fullscreen_panel === false ? 'top-0 -right-7' : 'top-2 right-2'
        ]"
      >
        <button
          @click="toggleFullScreen(exercise_index)"
          title="Toggle fullscreen mode"
          :class="`
            w-7 p-1 focus-outline font-semibold
            text-slate-800 bg-slate-100  hover:bg-slate-200  dark:text-slate-200 dark:bg-slate-800  dark:hover:bg-slate-900
            ${fullscreen_panel === false ? 'rounded-r-md' : 'rounded-bl-md'}
          `"
        >
          <FontAwesomeIcon
            :icon="
              fullscreen_panel !== exercise_index
                ? faUpRightAndDownLeftFromCenter
                : faDownLeftAndUpRightToCenter
            "
            fixed-width
          ></FontAwesomeIcon>
        </button>
      </span>
      <KeepAlive>
        <TheScoreTable
          v-show="fullscreen_panel === false"
          :exercise="exercise"
          :exercise_index="exercise_index"
          :hide_inactive_users="hide_inactive_users"
        ></TheScoreTable>
      </KeepAlive>
      <KeepAlive>
        <TheFullScreenScoreGrid
          v-if="fullscreen_panel !== false"
          :exercise="exercises[fullscreen_panel]"
          :exercise_index="exercise_index"
          :hide_inactive_users="hide_inactive_users"
        ></TheFullScreenScoreGrid>
      </KeepAlive>
    </div>
  </template>
</template>
