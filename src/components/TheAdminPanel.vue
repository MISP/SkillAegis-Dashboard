<script setup>
  import { ref, computed, onMounted } from 'vue'
  import { exercises, selected_exercises, diagnostic, resetAllExerciseProgress, changeExerciseSelection, fetchDiagnostic } from "@/socket";
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
  import { faScrewdriverWrench, faTrash, faSuitcaseMedical, faGraduationCap } from '@fortawesome/free-solid-svg-icons'

  const admin_modal = ref(null)

  const diagnosticLoading = computed(() => Object.keys(diagnostic.value).length == 0)
  const isMISPOnline = computed(() => diagnostic.value.version?.version !== undefined)

  function changeSelectionState(state_enabled, exec_uuid) {
    changeExerciseSelection(exec_uuid, state_enabled);
  }

  function showTheModal() {
    admin_modal.value.showModal()
    fetchDiagnostic()
  }
</script>

<template>
  <button
    @click="showTheModal()"
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
              class="h-10 min-h-10 px-2 py-1 font-semibold bg-red-600 text-slate-200 hover:bg-red-700 btn btn-sm"
            >
              <FontAwesomeIcon :icon="faTrash" class="mr-1"></FontAwesomeIcon>
              Reset All Exercises
            </button>
          </div>

          <h3 class="text-lg font-semibold">
            <FontAwesomeIcon :icon="faGraduationCap" class="mr-1"></FontAwesomeIcon>
            Selected Exercises
          </h3>
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
                :class="`checkbox ${selected_exercises.includes(exercise.uuid) ? 'checkbox-success' : ''} [--fallback-bc:#94a3b8]`"
              />
              <span class="font-mono font-semibold text-base ml-3">{{ exercise.name }}</span>
            </label>
          </div>

          <h3 class="text-lg font-semibold mt-4">
            <FontAwesomeIcon :icon="faSuitcaseMedical" class="mr-1"></FontAwesomeIcon>
            Diagnostic
          </h3>
          <h4 class="font-semibold ml-1 my-2">
            <strong>MISP Status:</strong>
            <span class="ml-2">
              <span :class="{
                'rounded-lg py-1 px-2': true,
                'dark:bg-neutral-800 bg-neutral-400 text-slate-800 dark:text-slate-200': diagnosticLoading,
                'dark:bg-green-700 bg-green-500 text-slate-800 dark:text-slate-200': !diagnosticLoading && isMISPOnline,
                'dark:bg-red-700 bg-red-700 text-slate-200 dark:text-slate-200': !diagnosticLoading && !isMISPOnline,
              }">
                <span v-if="diagnosticLoading" class="loading loading-dots loading-sm h-4 inline-block align-middle"></span>
                <span v-else class="font-bold">
                  {{ !isMISPOnline ? 'Unreachable' : `Online (${diagnostic['version']['version']})` }}
                </span>
              </span>
            </span>
          </h4>

          <h4 class="font-semibold ml-1"><strong>MISP Settings:</strong></h4>
          <div class="ml-3">
            <div v-if="diagnosticLoading" class="flex justify-center">
              <span class="loading loading-dots loading-lg"></span>
            </div>
            <div
              v-for="(value, setting) in diagnostic['settings']"
              :key="setting"
            >
              <div>
                <label class="label cursor-pointer justify-start p-0 pt-1">
                  <input
                    type="checkbox"
                    :checked="value"
                    :value="setting"
                    :class="`checkbox ${value ? 'checkbox-success' : 'checkbox-danger'} [--fallback-bc:#cbd5e1]`"
                    disabled
                  />
                  <span class="font-mono font-semibold text-base ml-3">{{ setting }}</span>
                </label>
              </div>
            </div>
          </div>

        </div>
      </div>
      <form method="dialog" class="modal-backdrop">
        <button>close</button>
      </form>
    </dialog>
</template>
