<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { darkModeEnabled } from '../settings.js'
import StatPanel from './elements/StatPanel.vue';
import UsernameFormatter from '@/components/elements/UsernameFormatter.vue';
import RotatingList from '@/components/elements/RotatingList.vue';
import { faCheck, faBolt, faFire, faMedal, faTrophy, faPeopleGroup, faCircleQuestion } from '@fortawesome/free-solid-svg-icons';
import TextWithSparkles from '@/components/elements/TextEffects/TextWithSparkles.vue';
import TextWithPulse from '@/components/elements/TextEffects/TextWithPulse.vue';
import FireBadge from '@/components/elements/TextEffects/FireBadge.vue';
import NumberEffect from '@/components/elements/TextEffects/NumberEffect.vue';
import ProgressBar from '@/components/elements/ProgressBar.vue';

import { userStats, active_exercises as exercises, progresses, shouldHideGamification } from '@/socket.js';
import TrophyDescription from '@/components/elements/TrophyDescription.vue';


const pageCountFame = ref(0)
const currentPageFame = ref(0)
const limitFame = ref(3)
const pageCountFire = ref(0)
const currentPageFire = ref(0)
const limitFire = ref(3)
const pageCountRunner = ref(0)
const currentPageRunner = ref(0)
const limitRunner = ref(3)

const hallOfFame = computed(() => userStats.value?.hall_of_fame || []);
const timeOnFire = computed(() => userStats.value?.time_on_fire || []);
const speedRunner = computed(() => userStats.value?.speed_runner || []);
const trophies = computed(() => userStats.value?.trophies || []);

const trophyList = computed(() => Object.values(trophies.value).map(t => {
  return { ...t.metadata, users: t.users }
}))


const overallProgressForEligiblePlayers = computed(() => {
  let taskCount = 0
  let taskCompletedCount = 0
  let userCount = 0
  for (const exercise of exercises.value) {
    taskCount += exercise.tasks.length
  }
  for (const { email, exercises: userExercises } of Object.values(progresses.value)) {
    const completedTaskCount = getCompletedTaskCount(userExercises)
    taskCompletedCount += completedTaskCount
    userCount += 1
  }
  const completionPercentage = 100 * (taskCompletedCount / (taskCount * userCount))
  if (Number.isNaN(completionPercentage)) {
    return 0
  }
  return completionPercentage


  /**
   * The code below is something that tries to be clever (not entirely working as expected)
   *  and only show progression for users above a specific threshold.
   */ 
  // const completionThreshold = 0.2 * taskCount

  // let taskCompletedCount = 0
  // let taskCompletedCountUnderThreshold = 0
  // let userWithEnoughCompletionCount = 0
  // let userCount = 0

  // for (const { email, exercises: userExercises } of Object.values(progresses.value)) {
  //   const completedTaskCount = getCompletedTaskCount(userExercises)
  //   taskCompletedCount += completedTaskCount
  //   userCount += 1
  //   if (completedTaskCount >= completionThreshold) {
  //     userWithEnoughCompletionCount += 1
  //     taskCompletedCountUnderThreshold += completedTaskCount
  //   }
  // }

  // if (taskCount * userWithEnoughCompletionCount == 0) {
  //   return 0
  // }

  // const completionPercentage = 100 * (taskCompletedCount / (taskCount * userCount))   
  // if (completionPercentage < 10) { // Not enough completion done to show with threshold
  //   return completionPercentage
  // }
  // return 100 * (taskCompletedCountUnderThreshold / (taskCount * userWithEnoughCompletionCount))

})

function getCompletedTaskCount(userExercises) {
  let completedTaskCount = 0
  for (const [uuid, userProgress] of Object.entries(userExercises)) {
    for (const [taskUuid, completionStatus] of Object.entries(userProgress.tasks_completion)) {
      if (completionStatus !== false) {
        completedTaskCount += 1
      }
    }
  }
  return completedTaskCount
}

const collectiveScore = computed(() => {
  let score = 0
  for (const { email, exercises: userExercises } of Object.values(progresses.value)) {
    for (const [uuid, userProgress] of Object.entries(userExercises)) {
      score += userProgress.score
    }
  }
  return score
})

const collectiveTaskDone = computed(() => {
  let taskCompletedCount = 0
  for (const { email, exercises: userExercises } of Object.values(progresses.value)) {
    const completedTaskCount = getCompletedTaskCount(userExercises)
    taskCompletedCount += completedTaskCount
  }
  return taskCompletedCount
})
</script>

<template>
  <div class="flex flex-col gap-2">
    <div v-if="!shouldHideGamification">
      <div class="flex flex-row gap-2">
        <div class="grow-0 inline-flex flex-col gap-2 dark:text-slate-300 text-slate-700 min-w-72">
          <StatPanel
            title="Hall of Fame"
            info="Top players having the highest score.&#010;Must have aquired at least half the total points."
            color="#FFD700"
            :icon="faMedal"
          >
            <RotatingList
              v-slot="{ item, index }" :list="hallOfFame" :limit="limitFame" :pagination_rate_sec="5"
              @rotating-pageupdate="(currentPage, pageCount) => { currentPageFame = currentPage; pageCountFame = pageCount }"
            >
              <span class="flex flex-row items-center">
                <TextWithSparkles v-if="index === 0" :sparkleCount="5">
                  <UsernameFormatter :username="item.email"></UsernameFormatter>
                </TextWithSparkles>
                <UsernameFormatter v-else :username="item.email"></UsernameFormatter>
                <span :style="`color: #FFD700`" class="font-title ml-auto">
                  <NumberEffect :value="item.score"></NumberEffect>
                </span>
              </span>
            </RotatingList>
            <span class="absolute top-1 bottom-1 -right-[2px] w-1 inline-flex flex-col gap-1">
              <span
                v-for="pageI in pageCountFame"
                :key="pageI"
                class="grow rounded-3xl bg-slate-100 dark:bg-slate-500"
                :style="`background-color: ${currentPageFame == (pageI - 1) ? '#FFD700 !important' : ''}`"
              >
              </span>
            </span>
          </StatPanel>
          <StatPanel
            title="Time On Fire"
            info="Top players with the most time spent on fire."
            color="#FF5722"
            :icon="faFire"
          >
            <RotatingList
              v-slot="{ item, index }" :list="timeOnFire" :limit="limitFire" :pagination_rate_sec="5"
              @rotating-pageupdate="(currentPage, pageCount) => { currentPageFire = currentPage; pageCountFire = pageCount }"
            >
              <span class="flex flex-row items-center">
                <FireBadge v-if="index === 0" :is_blue="true">
                  <UsernameFormatter :username="item.email"></UsernameFormatter>
                </FireBadge>
                <UsernameFormatter v-else :username="item.email"></UsernameFormatter>
                <span :style="`color: #FF5722`" class="font-title ml-auto">
                  <NumberEffect :value="item.time_on_fire / 60"></NumberEffect>
                </span>
              </span>
            </RotatingList>
            <span class="absolute top-1 bottom-1 -right-[2px] w-1 inline-flex flex-col gap-1">
            <span
              v-for="pageI in pageCountFire"
              :key="pageI"
              class="grow rounded-3xl bg-slate-100 dark:bg-slate-500"
              :style="`background-color: ${currentPageFire == (pageI - 1) ? '#FF5722 !important' : ''}`"
            >
            </span>
          </span>
          </StatPanel>
          <StatPanel
            title="Speed Runner"
            info="Top players with the fastest time based on tasks completed.&#010;Must have completed at least 3 tasks."
            color="#4287ff"
            :icon="faBolt"
          >
            <RotatingList
              v-slot="{ item, index }" :list="speedRunner" :limit="limitRunner" :pagination_rate_sec="5"
              @rotating-pageupdate="(currentPage, pageCount) => { currentPageRunner = currentPage; pageCountRunner = pageCount }"
            >
              <span class="flex flex-row items-center">
                <TextWithPulse v-if="index === 0">
                  <UsernameFormatter :username="item.email"></UsernameFormatter>
                </TextWithPulse>
                <UsernameFormatter v-else :username="item.email"></UsernameFormatter>
                <span :style="`color: #4287ff`" class="font-title ml-auto">
                  <NumberEffect :value="item.speedrunner_score"></NumberEffect>
                </span>
              </span>
            </RotatingList>
            <span class="absolute top-1 bottom-1 -right-[2px] w-1 inline-flex flex-col gap-1">
              <span
                v-for="pageI in pageCountRunner"
                :key="pageI"
                class="grow rounded-3xl bg-slate-100 dark:bg-slate-500"
                :style="`background-color: ${currentPageRunner == (pageI - 1) ? '#4287ff !important' : ''}`"
              >
              </span>
            </span>
          </StatPanel>
        </div>
        <div class="grow flex">
          <StatPanel
            title="Trophies"
            color="#ff40ff"
            :icon="faTrophy"
            class="overflow-hidden max-h-[292px]"
          >
          <span v-if="trophyList.length == 0" class="text-center font-retrogaming text-slate-400">There are no trophies for this
            exercise</span>
          <RotatingList v-slot="{ item }" :list="trophyList" :limit="5" :pagination_rate_sec="5">
            <TrophyDescription :trophy="item"></TrophyDescription>
          </RotatingList>

          </StatPanel>
        </div>
      </div>
    </div>
    <div>
      <div class="flex">
        <StatPanel
            title="Global Progress"
            info="Overall progress of all players who have completed at least 20% of the tasks"
            color="#4CAF50"
            :icon="faPeopleGroup"
          >
            <div class="flex flex-col gap-1">
              <ProgressBar :progress="overallProgressForEligiblePlayers" from_color="#FFA500" to_color="#4CAF50" class="h-2"></ProgressBar>
              <span :style="`color: #FFD700`" class="font-title flex leading-4 mt-1">
                <span>Collective Score</span>
                <NumberEffect :value="collectiveScore" class="ml-auto"></NumberEffect>
              </span>
              <span :style="`color: #FFD700`" class="font-title flex leading-4">
                <span>Total Tasks Completed</span>
                <NumberEffect :value="collectiveTaskDone" class="ml-auto"></NumberEffect>
              </span>
            </div>
          </StatPanel>
      </div>
    </div>
  </div>
</template>

<style scoped>
img.trophy {
  width: 32px;
  max-width: unset;
  height: 32px;
  max-height: unset;
}
</style>