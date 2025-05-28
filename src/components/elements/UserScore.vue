<script setup>
import { computed, reactive } from 'vue';
import TextWithSparkles from '@/components/elements/TextEffects/TextWithSparkles.vue';
import NumberEffect from '@/components/elements/TextEffects/NumberEffect.vue';

const props = defineProps({
    'score': {
        type: Number,
        required: true,
    },
    'max_score': {
        type: Number,
        required: true,
    },
})

const percentage = computed(() => {
    return props.score / props.max_score
})

const color = computed(() => {
    if (percentage.value == 1) {
        return 'text-yellow-400';
    } else if (percentage.value >= 0.9) {
        return 'text-green-500';
    } else if (percentage.value >= 0.75) {
        return 'text-amber-500';
    } else if (percentage.value >= 0.5) {
        return 'text-orange-500';
    } else if (percentage.value >= 0.3) {
        return 'text-cyan-500';
    } else {
        return '';
    }
})
</script>

<template>
    <span
        v-if="percentage != 1"
        class="font-title"
        :class="color"
    >
    <NumberEffect :value="score"></NumberEffect>
    </span>

    <TextWithSparkles v-else>
        <span class="text-yellow-400">
            <NumberEffect :value="score"></NumberEffect>
        </span>
    </TextWithSparkles>
</template>

<style>
@keyframes twinkle {
  0%, 100% {
    transform: scale(1) rotate(0deg);
    opacity: 0.8;
    filter: drop-shadow(0 0 2px rgba(255, 255, 255, 0.5));
  }
  50% {
    transform: scale(1.4) rotate(60deg);
    opacity: 0.4;
    filter: drop-shadow(0 0 6px rgba(255, 255, 255, 0.8));
  }
}
</style>