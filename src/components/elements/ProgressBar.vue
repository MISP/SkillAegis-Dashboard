<script setup>
import { computed } from 'vue';

const props = defineProps({
    'progress': {
        type: Number,
        required: true,
        validator(value) {
            return 0 <= value && value <= 100
        },
    },
    'color': {
        type: String,
        required: false,
        default: '',
    },
    'from_color': {
        type: String,
        required: false,
        default: '',
    },
    'to_color': {
        type: String,
        required: false,
        default: '',
    },
    'color_class': {
        type: String,
        required: false,
        default: 'bg-green-500',
    },
})

const the_color_class = computed(() => {
    return the_color.value ? '' : props.color_class
})

const the_color = computed(() => {
    if (props.from_color && props.to_color) {
        return `linear-gradient(to right, ${props.from_color}, ${props.to_color})`
    }
    return props.color
})

const masked_progress = computed(() => 100 - props.progress)

</script>

<template>
    <div>
        <div class="h-full w-full relative rounded">
            <div class="h-full w-full rounded" :class="the_color_class" :style="{ 'background': the_color }">
                <div class="rounded-r absolute top-0 right-0 bottom-0 bg-slate-500 transition-width duration-300" :style="{ width: masked_progress + '%' }"></div>
            </div>
            <span class="absolute left-1/4 top-0 w-[4px] h-full dark:bg-slate-800/80 bg-slate-300/80 inline-block leading-3"></span>
            <span class="absolute left-1/2 top-0 w-[4px] h-full dark:bg-slate-800/80 bg-slate-300/80 inline-block leading-3"></span>
            <span class="absolute left-3/4 top-0 w-[4px] h-full dark:bg-slate-800/80 bg-slate-300/80 inline-block leading-3"></span>
        </div>
    </div>
</template>