<script setup>
import { computed } from 'vue';

const props = defineProps({
    'username': {
        type: String,
        required: true,
    },
    'short': {
        type: Boolean,
        required: false,
        default: false,
    },
})

const splitUsername = computed(() => {
    return props.username.split('@')
})
</script>

<template>
    <span class="inline-flex flex-nowrap group">
        <span class="inline-block text-xl font-retrogaming leading-4 tracking-tight">{{ splitUsername[0] }}</span>
        <span :class="`ml-[2px] self-end ${props.short ? 'group-hover:inline-block hidden' : 'inline-block'} text-[0.66rem] font-mono leading-[8px] tracking-tight max-w-24 overflow-x-hidden text-ellipsis overflow-hidden`">@{{ splitUsername[1] }}</span>
    </span>
</template>
