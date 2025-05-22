<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { darkModeEnabled } from '../settings.js'
import StatPanel from './elements/StatPanel.vue';
import UsernameFormatter from '@/components/elements/UsernameFormatter.vue';
import { faCheck, faCheckCircle, faGaugeHigh, faMedal, faTrophy } from '@fortawesome/free-solid-svg-icons';


</script>

<template>
  <div class="flex flex-row gap-2 justify-center">
    <div class="grow-0 inline-flex flex-col justify-center gap-2 dark:text-slate-300 text-slate-700">
      <StatPanel
        title="Hall of Fame"
        color="#FFD700"
        :icon="faMedal"
      >
        <ul>
          <li v-for="(item, i) in ['admin1@admin.test', 'admin2@admin.test', 'admin3@admin.test', 'admin4@admin.test', 'admin5@admin.test']" :key="i" class="leading-4">
            <span :style="`color: #FFD700`" class="font-title mr-2">{{ i+1 }}.</span>
            <UsernameFormatter :username="item"></UsernameFormatter>
          </li>
        </ul>
      </StatPanel>
      <StatPanel
        title="Fastest Finisher"
        color="#00CFFF"
        :icon="faGaugeHigh"
      >
        <ul>
          <li v-for="(item, i) in ['admin1@admin.test', 'admin2@admin.test', 'admin3@admin.test']" :key="i" class="leading-4">
            <span :style="`color: #00CFFF`" class="font-title mr-2">{{ i+1 }}.</span>
            <UsernameFormatter :username="item"></UsernameFormatter>
          </li>
        </ul>
      </StatPanel>
      <StatPanel
        title="Recent Completion"
        color="#7041fd"
        :icon="faCheckCircle"
      >
        <ul>
          <li v-for="(item, i) in ['admin1@admin.test', 'admin2@admin.test', 'admin3@admin.test']" :key="i" class="leading-4">
            <UsernameFormatter :username="item"></UsernameFormatter>
          </li>
        </ul>
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
