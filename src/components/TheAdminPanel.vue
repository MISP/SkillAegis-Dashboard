<script setup>
  import { ref } from 'vue'
  import { exercises, selected_exercises, resetAllExerciseProgress, changeExerciseSelection } from "@/socket";
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
  import { faScrewdriverWrench, faTrash } from '@fortawesome/free-solid-svg-icons'

  const admin_modal = ref(null)

  function changeSelectionState(state_enabled, exec_uuid) {
    changeExerciseSelection(exec_uuid, state_enabled);
  }

</script>

<template>
  <button
    @click="admin_modal.showModal()"
    class="px-2 py-1 rounded-md focus-outline font-semibold bg-blue-600 text-slate-200 hover:bg-blue-700"
  >
    <FontAwesomeIcon :icon="faScrewdriverWrench" class="mr-1"></FontAwesomeIcon>
    Admin panel
  </button>

  <dialog ref="admin_modal" class="modal">
    <div class="modal-box w-11/12 max-w-6xl top-24 absolute bg-slate-200 dark:bg-slate-600 text-slate-700 dark:text-slate-200">
        <h2 class="text-2xl font-bold">
          <FontAwesomeIcon :icon="faScrewdriverWrench" class="mr-1"></FontAwesomeIcon>
          Admin panel
        </h2>
        <div class="modal-action">
          <form method="dialog">
              <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
          </form>
        </div>
        <div>

          <div class="flex mb-5">
            <button
              @click="resetAllExerciseProgress()"
              class="px-2 py-1 rounded-md focus-outline font-semibold bg-red-600 text-slate-200 hover:bg-red-700"
            >
              <FontAwesomeIcon :icon="faTrash" class="mr-1"></FontAwesomeIcon>
              Reset All Exercises
            </button>
          </div>

          <h3 class="text-lg font-semibold">Selected Exercises</h3>
          <div
            v-for="(exercise) in exercises"
            :key="exercise.name"
            class="form-control pl-3"
          >
            <label class="label cursor-pointer justify-start">
              <input
                @change="changeSelectionState($event.target.checked, exercise.uuid)"
                type="checkbox"
                :checked="selected_exercises.includes(exercise.uuid)"
                :value="exercise.uuid"
                :class="`checkbox ${selected_exercises.includes(exercise.uuid) ? 'checkbox-success' : ''}`"
              />
              <span class="font-mono font-semibold text-base ml-3">{{ exercise.name }}</span>
            </label>
          </div>

        </div>
      </div>
      <form method="dialog" class="modal-backdrop">
        <button>close</button>
      </form>
    </dialog>
</template>
