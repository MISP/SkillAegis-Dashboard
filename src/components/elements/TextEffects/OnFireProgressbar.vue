<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue';

const props = defineProps({
    'on_fire_interval': {
        type: Array,
        required: true,
    },
})
const endTimestamp = computed(() => props.on_fire_interval[1]*1000)
const duration = computed(() => props.on_fire_interval[1]*1000 - props.on_fire_interval[0]*1000)

const progress = ref(100)
let intervalId = null

const updateProgress = () => {
    const now = Date.now()
    const elapsed = endTimestamp.value - now
    const percentage = (elapsed / duration.value) * 100
    progress.value = Math.max(0, Math.min(100, percentage))
}

onMounted(() => {
    updateProgress()
    intervalId = setInterval(updateProgress, 1000)
})
onUnmounted(() => {
    clearInterval(intervalId)
})
</script>

<template>
    <span>
        <slot />
        <div class="h-[2px] w-[233px] relative -ml-[7px] bg-slate-500" v-show="progress > 0">
            <div class="h-full bg-amber-500 before:inline-block before:leading-[1px] before:h-[6px] before:w-[2px] before:absolute before:bottom-[1px] before:border-l-[2px] before:border-l-amber-500"
                :style="{ width: progress + '%' }"></div>
        </div>
    </span>
</template>

<style scoped>
</style>