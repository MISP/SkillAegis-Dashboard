<script setup>
  import { ref, computed } from "vue";
  import { active_exercises as exercises } from "@/socket";
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
  import { faGraduationCap, faUpRightAndDownLeftFromCenter, faDownLeftAndUpRightToCenter, faWarning } from '@fortawesome/free-solid-svg-icons'
  import TheScoreTable from "./scoreViews/TheScoreTable.vue"
  import TheFullScreenScoreGrid from "./scoreViews/TheFullScreenScoreGrid.vue"
  import ThePlayerGrid from "./ThePlayerGrid.vue"
  import { fullscreenModeOn } from "@/settings.js"

  const hasExercises = computed(() => exercises.value.length > 0)
  const fullscreen_panel = ref(false)

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
  <h3 class="text-2xl mt-6 mb-2 font-bold text-blue-500 dark:text-blue-400">
    <FontAwesomeIcon :icon="faGraduationCap"></FontAwesomeIcon>
    Active Exercises
  </h3>

  <div
    v-if="!hasExercises"
    class="text-slate-600 dark:text-slate-400 p-3 pl-6"
  >
    <div class="
      p-2 border-l-4 text-left rounded
      dark:bg-yellow-300 dark:text-slate-900 dark:border-yellow-700 
      bg-yellow-200 text-slate-900 border-yellow-700 
    ">
      <FontAwesomeIcon :icon="faWarning" class="text-yellow-700 text-lg mx-3"></FontAwesomeIcon>
      <strong class="">No Exercise available.</strong>
      <span class="ml-1">Select an exercise in the <i class="underline">Admin panel</i>.</span>
    </div>

    <ThePlayerGrid></ThePlayerGrid>
  </div>

  <template
    v-for="(exercise, exercise_index) in exercises"
    :key="exercise.name"
  >
    <div :class="fullscreen_panel === false ? 'relative min-w-fit' : ''">
      <span
        v-show="fullscreen_panel === false || fullscreen_panel === exercise_index"
        :class="['inline-block absolute shadow-lg z-50', fullscreen_panel === false ? 'top-0 -right-7' : 'top-2 right-2']"
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
          <FontAwesomeIcon :icon="fullscreen_panel !== exercise_index ? faUpRightAndDownLeftFromCenter : faDownLeftAndUpRightToCenter" fixed-width></FontAwesomeIcon>
        </button>
      </span>
      <KeepAlive>
        <TheScoreTable
          v-show="fullscreen_panel === false"
          :exercise="exercise"
          :exercise_index="exercise_index"
        ></TheScoreTable>
      </KeepAlive>
      <KeepAlive>
        <TheFullScreenScoreGrid
          v-if="fullscreen_panel !== false"
          :exercise="exercises[fullscreen_panel]"
          :exercise_index="exercise_index"
        ></TheFullScreenScoreGrid>
      </KeepAlive>
    </div>
  </template>
</template>
