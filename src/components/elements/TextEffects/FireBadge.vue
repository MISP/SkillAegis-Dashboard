<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';

const props = defineProps({
    'is_blue': {
        type: Boolean,
        required: false,
        default: false,
    },
    'on_fire_interval': {
        type: [Array, null],
        required: false,
        default: null,
    },
})

let intervalId = null
const endTimestamp = computed(() => props.on_fire_interval !== null ? (props.on_fire_interval[1] * 1000) : null)
const showBadge = ref(true)

const updateVisibility = () => {
    if (endTimestamp.value === null) {
        showBadge.value = true
    } else {
        const now = Date.now()
        showBadge.value = now <= endTimestamp.value
        
    }
}

onMounted(() => {
    updateVisibility()
    intervalId = setInterval(updateVisibility, 1000)
})
onUnmounted(() => {
    clearInterval(intervalId)
})
</script>

<template>
    <span class="inline-flex flex-row flex-nowrap">
        <template v-if="showBadge">
            <img v-if="props.is_blue" src="/assets/fire_blue.gif" alt="Fire badge blue" class="inline-block"
                style="height: 1rem; position:relative; top: -1px;" />
            <img v-else src="/assets/fire.gif" alt="Fire badge" class="inline-block"
                style="height: 1rem; position:relative; top: -1px;" />
        </template>
        <slot />
    </span>
</template>
