<script setup>
</script>


<template>
    <span class="text-cyan-400 font-semibold speed-runner-text">
        <slot />
    </span>
</template>

<style scoped>
@keyframes speedPulse {
  0%, 100% {
    transform: translateX(0) scale(1);
    opacity: 1;
  }
  30% {
    transform: translateX(3px) scale(1.02);
    opacity: 0.8;
  }
  60% {
    transform: translateX(0px) scale(1.02);
    opacity: 0.9;
  }
}
.speed-runner-text {
  display: inline-block;
  animation: speedPulse 0.8s ease-in-out infinite;
  will-change: transform, opacity;
}
</style>