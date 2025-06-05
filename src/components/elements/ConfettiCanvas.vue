<template>
    <canvas ref="canvas" class="confetti-canvas"></canvas>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const canvas = ref(null)
let ctx
let particles = []
let animationFrameId

const confettiCount = 200
const duration = 4000 // ms
const gravity = 0.15

function createConfetti(width, height) {
    particles = Array.from({ length: confettiCount }, () => ({
        x: Math.random() * width,
        y: -20,
        size: 5 + Math.random() * 5,
        color: `hsl(${Math.random() * 360}, 90%, 60%)`,
        velocityX: (Math.random() - 0.5) * 6,
        velocityY: Math.random() * -4 - 3,
        rotation: Math.random() * 360,
        rotationSpeed: (Math.random() - 0.5) * 10,
    }))
}

function drawConfetti() {
    ctx.clearRect(0, 0, canvas.value.width, canvas.value.height)

    particles.forEach(p => {
        p.x += p.velocityX
        p.y += p.velocityY
        p.velocityY += gravity
        p.rotation += p.rotationSpeed

        ctx.save()
        ctx.translate(p.x, p.y)
        ctx.rotate((p.rotation * Math.PI) / 180)
        ctx.fillStyle = p.color
        ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size)
        ctx.restore()
    })
}

function animate() {
    drawConfetti()
    if (particles.some(p => p.y < canvas.value.height)) {
        animationFrameId = requestAnimationFrame(animate)
    }
}

onMounted(() => {
    const c = canvas.value
    c.width = window.innerWidth
    c.height = window.innerHeight
    ctx = c.getContext('2d')

    createConfetti(c.width, c.height)
    animate()

    setTimeout(() => {
        cancelAnimationFrame(animationFrameId)
        particles = []
        ctx.clearRect(0, 0, c.width, c.height)
    }, duration)
})

onUnmounted(() => {
    cancelAnimationFrame(animationFrameId)
})
</script>

<style scoped>
.confetti-canvas {
    position: fixed;
    top: 0;
    left: 0;
    pointer-events: none;
    z-index: 9999;
}
</style>
  
