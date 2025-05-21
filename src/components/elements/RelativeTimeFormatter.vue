<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue';

const props = defineProps({
    timestamp: {
        type: Number,
        required: true,
    }
})

const now = ref(Date.now())
const relativeTime = computed(() => getRelativeTime(props.timestamp))
let interval

function getRelativeTime(timestamp) {
    const rtf = new Intl.RelativeTimeFormat('en', { style: 'short' })

    const diff = parseInt(timestamp) - now.value

    const seconds = Math.round(diff / 1000)
    const minutes = Math.round(diff / 60000)
    const hours = Math.round(diff / 3600000)
    const days = Math.round(diff / 86400000)
    const months = Math.round(diff / 2592000000)
    const years = Math.round(diff / 31536000000)

    if (Math.abs(seconds) < 10) return rtf.format(seconds, 'now')
    if (Math.abs(seconds) < 60) return rtf.format(seconds, 'second')
    if (Math.abs(minutes) < 60) return rtf.format(minutes, 'minute')
    if (Math.abs(hours) < 24) return rtf.format(hours, 'hour')
    if (Math.abs(days) < 30) return rtf.format(days, 'day')
    if (Math.abs(months) < 12) return rtf.format(months, 'month')
    return rtf.format(years, 'year')
}


onMounted(() => {
    interval = setInterval(() => {
        now.value = Date.now()
    }, 15000)
})
onUnmounted(() => {
    clearInterval(interval)
})
</script>

<template>
    <span class="text-nowrap">{{ relativeTime }}</span>
</template>