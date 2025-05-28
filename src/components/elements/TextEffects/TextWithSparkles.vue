<script setup>
    import { reactive } from 'vue'

    const props = defineProps({
        'sparkleCount': {
            type: Number,
            required: false,
            default: 3
        },
    })

    const sparkleColors = [
        'text-yellow-300',
    ]
    const positions = [
        {x: '75%', y: '10%'},
        {x: '5%', y: '5%'},
        {x: '50%', y: '40%'},
    ]

    if (props.sparkleCount - 3 > 0) {
        for (let i = 0; i < (props.sparkleCount - 3); i++) {
            positions.push({
                x: `${Math.random() * 100}%`,
                y: `${Math.random() * 100}%`
            })
        }
    }


    const sparkles = reactive([])

    for (let i = 0; i < props.sparkleCount; i++) {
        sparkles.push({
            id: i,
            style: {
                top: positions[i].y,
                left: positions[i].x,
                animation: `twinkle 2s ease-in-out infinite`,
                animationDelay: `${Math.random() * 2}s`,
                opacity: 0.8,
                size: (30 + Math.random() * 60) * 0.15,
                pointerEvents: 'none',
                zIndex: 2,
                color: sparkleColors[Math.floor(Math.random() * sparkleColors.length)],
                transitionDelay: `${Math.random() * 200}ms`,
            }
        })
    }
</script>

<template>
    <span
        class="relative inline-block font-title leading-4">
        <slot />
        <svg
            v-for="sparkle in sparkles"
            :key="sparkle.id"
            class="absolute"
            :style="sparkle.style"
            xmlns="http://www.w3.org/2000/svg"
            fill="currentColor"
            viewBox="0 0 160 160"
            :width="`${sparkle.style.size}px`"
            :height="`${sparkle.style.size}px`"
        >
            <path
                d="M80 0C80 0 84.2846 41.2925 101.496 58.504C118.707 75.7154 160 80 160 80C160 80 118.707 84.2846 101.496 101.496C84.2846 118.707 80 160 80 160C80 160 75.7154 118.707 58.504 101.496C41.2925 84.2846 0 80 0 80C0 80 41.2925 75.7154 58.504 58.504C75.7154 41.2925 80 0 80 0Z"
                :class="sparkle.style.color"
            />
        </svg>
    </span>
</template>

<style scoped>
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
