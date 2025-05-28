<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { darkModeEnabled } from '../settings.js'
import StatPanel from './elements/StatPanel.vue';
import UsernameFormatter from '@/components/elements/UsernameFormatter.vue';
import RotatingList from '@/components/elements/RotatingList.vue';
import { faCheck, faBolt, faFire, faMedal, faTrophy } from '@fortawesome/free-solid-svg-icons';
import TextWithSparkles from '@/components/elements/TextEffects/TextWithSparkles.vue';
import TextWithPulse from '@/components/elements/TextEffects/TextWithPulse.vue';
import FireBadge from '@/components/elements/TextEffects/FireBadge.vue';

import { userStats } from '@/socket.js';
import NumberEffect from './elements/TextEffects/NumberEffect.vue';

const hallOfFame = computed(() => userStats.value?.hall_of_fame || []);
const timeOnFire = computed(() => userStats.value?.time_on_fire || []);
const speedRunner = computed(() => userStats.value?.speed_runner || []);
const trophies = computed(() => userStats.value?.trophies || []);

const test_data = ['admin1@admin.test', 'admin2@admin.test', 'admin3@admin.test', 'admin4@admin.test', 'admin5@admin.test', 'admin6@admin.test']
</script>

<template>
  <div class="flex flex-row gap-2 justify-center">
    <div class="grow-0 inline-flex flex-col justify-center gap-2 dark:text-slate-300 text-slate-700">
      <StatPanel
        title="Hall of Fame"
        info="Top players having the highest score"
        color="#FFD700"
        :icon="faMedal"
      >
        <RotatingList v-slot="{ item, index }" :list="hallOfFame" :limit="3" :pagination_rate_sec="5">
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
      </StatPanel>
      <StatPanel
        title="Time On Fire"
        info="Top players with the most time spent on fire"
        color="#FF5722"
        :icon="faFire"
      >
        <RotatingList v-slot="{ item, index }" :list="timeOnFire" :limit="3" :pagination_rate_sec="5">
          <span class="flex flex-row items-center">
            <FireBadge v-if="index === 0">
              <UsernameFormatter :username="item.email"></UsernameFormatter>
            </FireBadge>
            <UsernameFormatter v-else :username="item.email"></UsernameFormatter>
            <span :style="`color: #FF5722`" class="font-title ml-auto">
              <NumberEffect :value="item.time_on_fire / 60"></NumberEffect>
            </span>
          </span>
        </RotatingList>
      </StatPanel>
      <StatPanel
        title="Speed Runner"
        info="Top players with the fastest time based on tasks completed"
        color="#4287ff"
        :icon="faBolt"
      >
        <RotatingList v-slot="{ item, index }" :list="speedRunner" :limit="3" :pagination_rate_sec="5">
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
      </StatPanel>
    </div>
    <div class="grow flex">
      <StatPanel
        title="Trophies"
        color="#ff40ff"
        :icon="faTrophy"
      >
        <span class="text-center font-retrogaming text-slate-400">There are no trophies for this exercise</span>
      </StatPanel>
    </div>
  </div>
</template>
