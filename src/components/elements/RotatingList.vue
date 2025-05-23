<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { registerTimerCallback, unregisterTimerCallback } from '@/utils.js';


const props = defineProps({
    'list': { type: Array, required: false },
    'limit': { type: Number, required: false, default: 3 },
    'outerTag': { type: String, required: false, default: 'ul'}
})

let timerID = null

const currentPage = ref(0)
const rotatingListRef = ref(null)
const firstPageHeight = ref(null)
const currentList = computed(() => {
  if (props.list.length > 0) {
    return props.list.slice(currentPage.value * props.limit, (currentPage.value + 1) * props.limit)
  }
  return []
})

function updatePage() {
    currentPage.value = (currentPage.value + 1) % Math.ceil(props.list.length / props.limit)
}

onMounted(() => {
    timerID = registerTimerCallback(updatePage)
    const rotatingListRefEl = rotatingListRef.value
    firstPageHeight.value = rotatingListRefEl.offsetHeight
})

onUnmounted(() => {
    unregisterTimerCallback(timerID)
})


</script>

<template>
    <div ref="rotatingListRef" :style="{ height: firstPageHeight ? firstPageHeight + 'px' : 'auto' }">
        <TransitionGroup name="slide-up" tag="ul" class="relative overflow-hidden">
            <li v-for="(item, i) in currentList" :key="i+currentPage*props.limit" class="leading-4">
                <slot :item="item" :index="i+currentPage*props.limit"></slot>
            </li>
        </TransitionGroup>
    </div>
</template>

<style scoped>
.slide-up-enter-active {
  transition: opacity 0.2s ease-out, transform 0.2s ease-out;
}

.slide-up-leave-active {
  transition: opacity 0.1s ease-out, transform 0.2s ease-out;
  position: absolute;
}

.slide-up-enter-from {
  opacity: 0;
  transform: translateY(30px);
}

.slide-up-leave-to {
  opacity: 0;
  transform: translateY(-30px);
}
</style>