<script setup>
  import { ref, computed } from "vue";
  import { active_exercises as exercises, progresses, userCount, setCompletedState } from "@/socket";
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
  import { faCheck, faTimes, faMedal, faHourglassHalf } from '@fortawesome/free-solid-svg-icons'
  import { faCircleCheck } from '@fortawesome/free-regular-svg-icons'
  import { darkModeEnabled } from "@/settings.js"
  import LiveLogsUserActivityGraph from "../LiveLogsUserActivityGraph.vue"

  const props = defineProps(['exercise', 'exercise_index'])
  const collapsed_panels = ref([])

  const chartOptions = computed(() => {
    return {
      chart: {
        type: 'radialBar',
        height: 120,
        sparkline: {
          enabled: true
        },
        animations: {
            enabled: false,
            easing: 'easeinout',
            speed: 200,
        },
      },
      colors: [darkModeEnabled.value ? '#008ffb' : '#1f9eff'],
      plotOptions: {
        radialBar: {
          startAngle: -110,
          endAngle: 110,
          hollow: {
            margin: 0,
            size: '30%',
            background: '#64748b',
            position: 'front',
            dropShadow: {
              enabled: true,
              top: 3,
              left: 0,
              blur: 4,
              opacity: 0.24
            }
          },
          track: {
              background: '#475569',
              strokeWidth: '97%',
              margin: 0,
              dropShadow: {
                enabled: true,
                top: 3,
                left: 0,
                blur: 3,
                opacity: 0.35
              }
            },
          dataLabels: {
            show: true,
            name: {
              show: false,
            },
            value: {
              formatter: function(val) {
                return parseInt(val*userCount.value / 100);
              },
              offsetY: 7,
              color: darkModeEnabled.value ? '#cbd5e1' : '#f1f5f9',
              fontSize: '1.25rem',
              show: true,
            }
          }
        }
      },
      stroke: {
        lineCap: 'smooth'
      },
      colors: [darkModeEnabled.value ? '#008ffb' : '#1f9eff'],
      labels: ['Progress'],
      tooltip: {
        enabled: false,
      },
    }
  })

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

  const compactGrid = computed(() => { return userCount.value > 70 })
  const ultraCompactGrid = computed(() => { return userCount.value > 100 })
  const hasProgress = computed(() => Object.keys(progresses.value).length > 0)
  const sortedProgress = computed(() => Object.values(progresses.value).sort((a, b) => {
    if (a.email < b.email) {
      return -1;
    }
    if (a.email > b.email) {
      return 1;
    }
    return 0;
  }))

  const taskCompletionPercentages = computed(() => {
    const completions = {}
    Object.values(props.exercise.tasks).forEach(task => {
      completions[task.uuid] = 0
    })

    sortedProgress.value.forEach(progress => {
      for (const [taskUuid, taskCompletion] of Object.entries(progress.exercises[props.exercise.uuid].tasks_completion)) {
        if (taskCompletion !== false) {
          completions[taskUuid] += 1
        }
      }
    });
  
    for (const [taskUuid, taskCompletionSum] of Object.entries(completions)) {
      completions[taskUuid] = 100 * (taskCompletionSum / userCount.value)
    }
    return completions
  })

</script>

<template>
    <div class="
      fixed inset-2 z-40 h-100 overflow-x-hidden
      rounded-lg bg-slate-300 dark:bg-slate-800 border border-slate-400 dark:border-slate-800
    ">

      <div
        class="
          rounded-t-lg text-md p-3 pl-6 text-center
          dark:bg-blue-800 bg-blue-500 dark:text-slate-300 text-slate-100
        "
      >
        <!-- Modal header -->
        <div class="flex justify-between items-center">
          <span class="text-lg font-semibold">{{ exercise.name }}</span>
          <span class="mr-8">
            Level: <span :class="{
              'rounded-lg px-1 ml-2': true,
              'dark:bg-sky-400 bg-sky-400 text-neutral-950': exercise.level == 'beginner',
              'dark:bg-orange-400 bg-orange-400 text-neutral-950': exercise.level == 'advanced',
              'dark:bg-red-600 bg-red-600 text-neutral-950': exercise.level == 'expert',
            }">{{ exercise.level }}</span>
          </span>
        </div>
      </div>

      <!-- Tasks name and pie charts -->
      <div class="p-2">
        <div class="flex justify-between mb-3">
          <span
            v-for="(task, task_index) in exercise.tasks"
            :key="task.name"
            class="p-1 inline-block"
            :title="task.description"
          >
            <span class="flex flex-col">
              <span class="text-center font-normal text-sm dark:text-blue-200 text-slate-800 text-nowrap">Task {{ task_index + 1 }}</span>
              <i class="text-center leading-4 text-slate-600 dark:text-slate-400">{{ task.name }}</i>
              <span class="inline-block h-18 -mt-4 mx-auto">
                <apexchart
                    ref="theChart" class="" height="120" width="100"
                    :options="chartOptions"
                    :series="[taskCompletionPercentages[task.uuid]]"
                ></apexchart>
              </span>
            </span>
          </span>
        </div>

        <!-- User grid -->
        <div :class="`flex flex-wrap ${compactGrid ? 'gap-1' : 'gap-2'}`">
          <span
            v-for="(progress) in sortedProgress"
            :key="progress.user_id"
            :class="[
              'bg-slate-200 dark:bg-slate-900 rounded border drop-shadow-lg',
              progress.exercises[exercise.uuid].score / progress.exercises[exercise.uuid].max_score == 1 ? 'border-green-700' : 'border-slate-700',
            ]"
          >
            <span class="
              flex p-2 mb-1
              text-slate-600 dark:text-slate-400
            ">
              <span :class="`flex flex-col ${compactGrid ? 'w-[120px]' : 'w-60'} ${compactGrid ? '' : 'mb-1'}`">
                <span :title="progress.user_id" class="text-nowrap inline-block leading-5 truncate mb-1">
                  <FontAwesomeIcon
                    v-if="progress.exercises[exercise.uuid].score / progress.exercises[exercise.uuid].max_score == 1"
                    :icon="faMedal" class="mr-1 text-amber-300"
                  ></FontAwesomeIcon>
                  <span :class="`${compactGrid ? 'text-base' : 'text-lg'} font-bold font-mono leading-5 tracking-tight`">{{ progress.email.split('@')[0] }}</span>
                  <span :class="`${compactGrid ? 'text-xs' : 'text-xs'} font-mono tracking-tight`">@{{ progress.email.split('@')[1] }}</span>
                </span>
                <LiveLogsUserActivityGraph
                  :user_id="progress.user_id"
                  :compact_view="compactGrid"
                  :ultra_compact_view="ultraCompactGrid"
                ></LiveLogsUserActivityGraph>
              </span>
            </span>

            <span class="
              flex flex-row justify-between px-2
              text-slate-500 dark:text-slate-400
            ">
              <span
                v-for="(task, task_index) in exercise.tasks"
                :key="task_index"
                class="select-none cursor-pointer"
                @click="toggleCompleted(progress.exercises[exercise.uuid].tasks_completion[task.uuid], progress.user_id, exercise.uuid, task.uuid)"
                :title="task.name"
              >
                  <span class="text-nowrap">
                    <FontAwesomeIcon
                      v-if="progress.exercises[exercise.uuid].tasks_completion[task.uuid]"
                      :icon="(progress.exercises[exercise.uuid].tasks_completion[task.uuid] && progress.exercises[exercise.uuid].tasks_completion[task.uuid].first_completion) ? faCircleCheck : faCheck"
                      :class="`${compactGrid ? 'text-xs' : 'text-xl'} dark:text-green-400 text-green-600`"
                      fixed-width
                    />
                    <FontAwesomeIcon
                      v-else-if="task.requirements?.inject_uuid !== undefined && !progress.exercises[exercise.uuid].tasks_completion[task.requirements.inject_uuid]"
                      title="All requirements for that task haven't been fullfilled yet"
                      :icon="faHourglassHalf"
                      :class="`${compactGrid ? 'text-xs' : 'text-lg'} dark:text-slate-500 text-slate-400`"
                      fixed-width
                    />
                    <FontAwesomeIcon
                      v-else
                      :icon="faTimes"
                      :class="`${compactGrid ? 'text-xs' : 'text-xl'} dark:text-slate-500 text-slate-400`"
                      fixed-width
                    />
                  </span>
              </span>
            </span>
          </span>
        </div>
      </div>
    </div>
</template>