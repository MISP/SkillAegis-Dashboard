<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { darkModeEnabled } from '../settings.js'
import StatPanel from './elements/StatPanel.vue';
import UsernameFormatter from '@/components/elements/UsernameFormatter.vue';
import RotatingList from '@/components/elements/RotatingList.vue';
import { faCheck, faBolt, faFire, faMedal, faTrophy } from '@fortawesome/free-solid-svg-icons';
import TextWithSparkles from '@/components/elements/TextWithSparkles.vue';
import TextWithPulse from '@/components/elements/TextWithPulse.vue';

</script>

<template>
  <div class="flex flex-row gap-2 justify-center">
    <div class="grow-0 inline-flex flex-col justify-center gap-2 dark:text-slate-300 text-slate-700">
      <StatPanel
        title="Hall of Fame"
        color="#FFD700"
        :icon="faMedal"
      >
        <RotatingList v-slot="{item, index }" :list="['admin1@admin.test', 'admin2@admin.test', 'admin3@admin.test', 'admin4@admin.test', 'admin5@admin.test', 'admin6@admin.test']" :limit="3" :pagination_rate_sec="5">
          <span :style="`color: #FFD700`" class="font-title mr-2">{{ index+1 }}.</span>
          <TextWithSparkles v-if="index === 0" :sparkleCount="5">
            <UsernameFormatter :username="item"></UsernameFormatter>
          </TextWithSparkles>
          <UsernameFormatter v-else :username="item"></UsernameFormatter>
        </RotatingList>
      </StatPanel>
      <StatPanel
        title="Time On Fire"
        color="#FF5722"
        :icon="faFire"
      >
        <RotatingList v-slot="{item, index }" :list="['admin1@admin.test', 'admin2@admin.test', 'admin3@admin.test', 'admin4@admin.test', 'admin5@admin.test', 'admin6@admin.test']" :limit="3" :pagination_rate_sec="5">
          <span :style="`color: #FF5722`" class="font-title mr-2">{{ index+1 }}.</span>
          <img
            v-if="index === 0"
            src="@/assets/fire.gif" alt="User is on fire" class="inline-block" style="height: 1rem; position:relative; top: -3px;" />
          <UsernameFormatter :username="item"></UsernameFormatter>
        </RotatingList>
      </StatPanel>
      <StatPanel
        title="Speed Runner"
        color="#4287ff"
        :icon="faBolt"
      >
        <RotatingList v-slot="{item, index }" :list="['admin1@admin.test', 'admin2@admin.test', 'admin3@admin.test', 'admin4@admin.test', 'admin5@admin.test', 'admin6@admin.test']" :limit="3" :pagination_rate_sec="5">
          <span :style="`color: #4287ff`" class="font-title mr-2">{{ index+1 }}.</span>
          <TextWithPulse v-if="index === 0">
            <UsernameFormatter :username="item"></UsernameFormatter>
          </TextWithPulse>
          <UsernameFormatter v-else :username="item"></UsernameFormatter>
        </RotatingList>
      </StatPanel>
    </div>
    <div class="grow flex">
      <StatPanel
        title="Achievements"
        color="#ff40ff"
        :icon="faTrophy"
      >
        <span class="text-center font-retrogaming">There are no achievements for this exercise</span>
      </StatPanel>
    </div>
  </div>
</template>
