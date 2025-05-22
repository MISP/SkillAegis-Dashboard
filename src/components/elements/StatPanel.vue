<script setup>
import { computed } from 'vue';

const props = defineProps({
    'title': { type: String, required: true },
    'color': { type: String, required: false, default: '#fff' },
    'list': { type: Array, required: false },
    'icon': { type: Object, required: true },
    'enumerate': { type: Boolean, required: false, default: true },
})

const top3Items = computed(() => props.list.slice(0, 3))

</script>

<template>
  <span class="dark:bg-slate-800/80 bg-slate-300/80 px-4 py-2 rounded-md min-w-72 grow shadow-strong">
    <div class="flex flex-col flex-nowrap">
      <span class="font-title text-xl uppercase text-nowrap mb-1" :style="`color: ${props.color}`">
        <FontAwesomeIcon :icon="props.icon" fixed-width style="--fa-fw-width: 1em"></FontAwesomeIcon>
        {{props.title}}
      </span>
      <span v-if="props.list" class="flex flex-row items-center">
        <ul>
          <li v-for="(item, i) in top3Items" :key="i" class="leading-4">
            <span v-if="props.enumerate" :style="`color: ${props.color}`" class="font-title mr-2">{{ i+1 }}.
            </span>
            <span class="font-retrogaming">{{ item }}</span>
          </li>
        </ul>
      </span>
      <slot v-else />
    </div>
  </span>
</template>
