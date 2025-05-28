<script setup>
import { ref, computed } from 'vue'
import { active_exercises as exercises } from '../socket'
import {
  faGraduationCap,
  faUpRightAndDownLeftFromCenter,
  faDownLeftAndUpRightToCenter,
  faWarning,
  faUsersSlash,
  faPause,
  faRankingStar,
} from '@fortawesome/free-solid-svg-icons'
import TheScoreTable from './scoreViews/TheScoreTable.vue'
import TheFullScreenScoreGrid from './scoreViews/TheFullScreenScoreGrid.vue'
import ThePlayerGrid from './ThePlayerGrid.vue'
import { fullscreenModeOn } from '../settings.js'

const hasExercises = computed(() => exercises.value.length > 0)
const fullscreen_panel = ref(false)
const hide_inactive_users = ref(false)
const enable_automatic_pagination = ref(true)
const sort_by_score = ref(false)
const selectectedExercise = ref(0)


function toggleFullScreen(exercise_index) {
  if (fullscreen_panel.value === exercise_index) {
    fullscreen_panel.value = false
    fullscreenModeOn.value = false
  } else {
    fullscreen_panel.value = exercise_index
    fullscreenModeOn.value = true
  }
}

function selectectExercise(exercise_index) {
  selectectedExercise.value = exercise_index
}
</script>

<template>
  <div class="">
    <div v-if="!hasExercises" class="text-slate-600 dark:text-slate-400 p-3 pl-6">
      <Alert variant="warning">
        <strong class="">No Exercise available.</strong>
        <span class="ml-1">Select an exercise in the <i class="underline">Admin panel</i>.</span>
      </Alert>

      <ThePlayerGrid></ThePlayerGrid>
    </div>

    <div class="shadow-lg">

      <div class="bg-slate-400 dark:bg-slate-600 border-slate-600 rounded-t-lg p-2">
        <div class="flex gap-2 flex-row items-center">
          <span v-for="(exercise, exercise_index) in exercises" :key="exercise.name"
            @click="selectectExercise(exercise_index)"
            :class="['px-4 py-1 rounded-md btn btn-lg',
                selectectedExercise == exercise_index ? 'btn-info' : 'btn-outline dark:btn-outline !font-normal'
            ]"
          >
            {{ exercise.name }}
          </span>
          <span class="ml-auto">
            <span class="flex flex-row gap-2">
              <label
                  class="flex items-center cursor-pointer text-slate-700 dark:text-slate-300 font-title"
                  title="Hide users that haven't been active in the past minutes"
                >
                <input type="checkbox" class="toggle toggle-success mr-1" :checked="hide_inactive_users"
                  @change="hide_inactive_users = !hide_inactive_users" />
                <FontAwesomeIcon :icon="faUsersSlash" size="sm" class="mr-1"></FontAwesomeIcon>
                Hide inactive
              </label>
              <label
                  class="flex items-center cursor-pointer text-slate-700 dark:text-slate-300 font-title"
                  title="Disable automatic pagination and allow to scroll the table"
                >
                <input type="checkbox" class="toggle toggle-info mr-1" :checked="enable_automatic_pagination"
                  @change="enable_automatic_pagination = !enable_automatic_pagination" />
                <FontAwesomeIcon :icon="faPause" size="sm" class="mr-1"></FontAwesomeIcon>
                Auto paginate
              </label>
              <label
                  class="flex items-center cursor-pointer text-slate-700 dark:text-slate-300 font-title"
                  title="Sort by Highest score"
                >
                <input type="checkbox" class="toggle toggle-info mr-1" :checked="sort_by_score"
                  @change="sort_by_score = !sort_by_score" />
                <FontAwesomeIcon :icon="faRankingStar" size="sm" class="mr-1"></FontAwesomeIcon>
                Sort by Score
              </label>
            </span>
          </span>
        </div>
      </div>

      <KeepAlive>
        <TheScoreTable v-for="(exercise, exercise_index) in exercises" :key="exercise.name"
          v-show="exercise_index == selectectedExercise"
          :exercise="exercise"
          :exercise_index="exercise_index"
          :hide_inactive_users="hide_inactive_users"
          :enable_automatic_pagination="enable_automatic_pagination"
          :sort_by_score="sort_by_score"
        ></TheScoreTable>
      </KeepAlive>
      <KeepAlive>
        <TheFullScreenScoreGrid v-if="fullscreen_panel !== false" :exercise="exercises[fullscreen_panel]"
          :exercise_index="exercise_index" :hide_inactive_users="hide_inactive_users"></TheFullScreenScoreGrid>
      </KeepAlive>
    </div>

  </div>

</template>
