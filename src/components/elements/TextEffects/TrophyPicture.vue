<script setup>
    import { ref, onMounted } from 'vue'

    const props = defineProps({
        'trophy': { type: Object, required: true },
    })

    const show = ref(false)

    onMounted(() => {
        setTimeout(() => {
            show.value = true
        }, 500)
        setInterval(() => {
            // show.value = !show.value
        }, 3000)
    })
</script>

<template>
    <span>
        <transition name="bounce">
            <img v-if="show" :src="`/${props.trophy.icon_path}`" class="trophy" />
        </transition>
        <span v-if="show" class="shine"></span>
    </span>
</template>

<style scoped>
img.trophy {
    width: 24px;
    max-width: unset;
    height: 24px;
    max-height: unset;
}

.bounce-enter-active {
    animation: dropBounce 0.8s ease;
}
.bounce-leave-active {
    animation: fadeOut 0.3s ease;
}
.bounce-leave-to {
    opacity: 0;
}

@keyframes dropBounce {
    0% {
        transform: translateY(-100px) scale(1);
        opacity: 0;
    }

    60% {
        transform: translateY(20px) scale(1.2);
        opacity: 1;
    }

    80% {
        transform: translateY(-10px) scale(0.95);
    }

    100% {
        transform: translateY(0) scale(1);
    }
}

@keyframes fadeOut {
    to {
        opacity: 0;
        transform: translateY(20px);
    }
}

.shine {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 60%;
    height: 100%;
    background: linear-gradient(120deg,
            transparent 0%,
            rgba(173, 216, 230, 0.2) 46%,
            rgba(255, 255, 255, 0.5) 50%,
            rgba(173, 216, 230, 0.2) 54%,
            transparent 100%);
    transform: skewX(-20deg);
    animation: shineSweep 0.8s ease-in forwards;
    pointer-events: none;
    border-radius: 6px;
    filter: blur(0.5px);
}

@keyframes shineSweep {
    0% {
        left: -100%;
        opacity: 1;
    }

    80% {
        opacity: 1;
    }

    100% {
        left: 120%;
        opacity: 0;
    }
}
</style>
