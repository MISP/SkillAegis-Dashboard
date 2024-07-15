<script setup>
  import { ref, computed, onMounted } from 'vue'
  import { exercises, selected_exercises, diagnostic, fullReload, resetAllExerciseProgress, resetAll, resetLiveLogs, changeExerciseSelection, debouncedGetDiangostic, remediateSetting } from "@/socket";
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
  import { faScrewdriverWrench, faTrash, faSuitcaseMedical, faGraduationCap, faBan, faRotate, faHammer, faCheck } from '@fortawesome/free-solid-svg-icons'

  const admin_modal = ref(null)
  const clickedButtons = ref([])

  const diagnosticLoading = computed(() => Object.keys(diagnostic.value).length == 0)
  const isMISPOnline = computed(() => diagnostic.value.version?.version !== undefined)
  const isZMQActive = computed(() => diagnostic.value.zmq_message_count > 0)
  const ZMQMessageCount = computed(() => diagnostic.value.zmq_message_count)

  function changeSelectionState(state_enabled, exec_uuid) {
    changeExerciseSelection(exec_uuid, state_enabled);
  }

  function settingHandler(setting) {
    remediateSetting(setting)
  }

  function showTheModal() {
    admin_modal.value.showModal()
    clickedButtons.value = []
    debouncedGetDiangostic()
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
          <FontAwesomeIcon :icon="faScrewdriverWrench" class=""></FontAwesomeIcon>
          Admin panel
        </h2>
        <div class="modal-action">
          <form method="dialog">
              <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
          </form>
        </div>
        <div>

          <div class="flex mb-5 gap-2">
            <button
              @click="fullReload()"
              class="h-10 min-h-10 px-2 py-1 font-semibold bg-blue-600 text-slate-200 hover:bg-blue-700 btn btn-sm gap-1"
            >
              <FontAwesomeIcon :icon="faRotate" size="lg" fixed-width></FontAwesomeIcon>
              Full refresh
            </button>
            <button
              @click="resetAllExerciseProgress()"
              class="h-10 min-h-10 px-2 py-1 font-semibold bg-red-600 text-slate-200 hover:bg-red-700 btn btn-sm gap-1"
            >
              <FontAwesomeIcon :icon="faTrash" size="lg" fixed-width></FontAwesomeIcon>
              Reset All Exercises
            </button>
            <button
              @click="resetAll()"
              class="h-10 min-h-10 px-2 py-1 font-semibold bg-red-600 text-slate-200 hover:bg-red-700 btn btn-sm gap-1"
            >
              <FontAwesomeIcon :icon="faTrash" size="lg" fixed-width></FontAwesomeIcon>
              Reset All
            </button>
            <button
              @click="resetLiveLogs()"
              class="h-10 min-h-10 px-2 py-1 font-semibold bg-amber-600 text-slate-200 hover:bg-amber-700 btn btn-sm gap-1"
            >
              <FontAwesomeIcon :icon="faBan" size="lg"> fixed-width</FontAwesomeIcon>
              Clear Live Logs
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
          <h4 class="font-semibold ml-1 my-3">
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
          <h4 class="font-semibold ml-1 my-3">
            <strong>ZMQ Status:</strong>
            <span class="ml-2">
              <span :class="{
                'rounded-lg py-1 px-2': true,
                'dark:bg-neutral-800 bg-neutral-400 text-slate-800 dark:text-slate-200': diagnosticLoading,
                'dark:bg-green-700 bg-green-500 text-slate-800 dark:text-slate-200': !diagnosticLoading && isZMQActive,
                'dark:bg-red-700 bg-red-700 text-slate-200 dark:text-slate-200': !diagnosticLoading && !isZMQActive,
              }">
                <span v-if="diagnosticLoading" class="loading loading-dots loading-sm h-4 inline-block align-middle"></span>
                <span v-else class="font-bold">
                  {{ !isZMQActive ? 'No message received yet' : `ZMQ Active (${ZMQMessageCount} messages)` }}
                </span>
              </span>
            </span>
          </h4>

          <template  v-if="diagnosticLoading || isMISPOnline">
            <h4 class="font-semibold ml-1"><strong>MISP Settings:</strong></h4>
            <div class="ml-3">
              <div v-if="diagnosticLoading" class="flex justify-center">
                <span class="loading loading-dots loading-lg"></span>
              </div>
              <table v-else class="bg-white dark:bg-slate-700 rounded-lg shadow-xl w-full mt-2">
                <thead>
                  <tr>
                    <th class="border-b border-slate-200 dark:border-slate-600 p-2 text-left">Setting</th>
                    <th class="border-b border-slate-200 dark:border-slate-600 p-2 text-left">Value</th>
                    <th class="border-b border-slate-200 dark:border-slate-600 p-2 text-left">Expected Value</th>
                    <th class="border-b border-slate-200 dark:border-slate-600 p-2 text-center">Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(settingValues, setting) in diagnostic['settings']"
                    :key="setting"
                  >
                    <td class="font-mono font-semibold text-base px-2">{{ setting }}</td>
                    <td
                      :class="`font-mono text-base tracking-tight px-2 ${settingValues.expected_value != settingValues.value ? 'text-red-600 dark:text-red-600' : ''}`"
                    >
                      <i v-if="settingValues.value === undefined || settingValues.value === null" class="text-nowrap">- none -</i>
                      {{ settingValues.value }}
                    </td>
                    <td class="font-mono text-base tracking-tight px-2">{{ settingValues.expected_value }}</td>
                    <td class="px-2 text-center">
                      <span v-if="settingValues.error === true"
                        class="text-red-600 dark:text-red-600"
                      >Error: {{ settingValues.errorMessage }}</span>
                      <button
                        v-else-if="settingValues.expected_value != settingValues.value"
                        @click="clickedButtons.push(setting) && settingHandler(setting)"
                        :disabled="clickedButtons.includes(setting)"
                        class="h-8 min-h-8 px-2 font-semibold bg-green-600 text-slate-200 hover:bg-green-700 btn gap-1"
                      >
                        <template v-if="!clickedButtons.includes(setting)">
                          <FontAwesomeIcon :icon="faHammer" size="sm" fixed-width></FontAwesomeIcon>
                          Remediate
                        </template>
                        <template v-else>
                          <span class="loading loading-dots loading-sm"></span>
                        </template>
                      </button>
                      <span v-else class="text-base font-bold text-green-600 dark:text-green-600">
                        <FontAwesomeIcon :icon="faCheck" class=""></FontAwesomeIcon>
                        OK
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </template>

        </div>
      </div>
      <form method="dialog" class="modal-backdrop">
        <button>close</button>
      </form>
    </dialog>
</template>
