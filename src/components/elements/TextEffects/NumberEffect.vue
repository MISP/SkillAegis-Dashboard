<script setup>
import { computed } from 'vue';

const props = defineProps({
    'value': {
        type: Number,
        required: true,
    },
})

const isInt = computed(() => props.value % 1 === 0)
</script>

<template>
    <span v-if="isInt" id="number" :style="{ '--int': props.value }"></span>
    <span v-else id="number-floating" :style="{ '--num': props.value }"></span>
</template>

<style scoped>
@property --int {
    syntax: "<integer>";
    initial-value: 0;
    inherits: false;
}

@property --num {
    syntax: "<number>";
    initial-value: 0;
    inherits: false;
}

@property --temp {
    syntax: "<number>";
    initial-value: 0;
    inherits: false;
}

@property --v1 {
    syntax: "<integer>";
    initial-value: 0;
    inherits: false;
}

@property --v2 {
    syntax: "<integer>";
    initial-value: 0;
    inherits: false;
}

#number {
    counter-reset: int var(--int);
    position: relative;
    transition: --int 0.3s ease-in-out;
}

#number::after {
    content: counter(int);
}

#number-floating {
    counter-reset: num var(--num);
    position: relative;
    transition: --num 0.3s ease-in-out;
    --temp: calc(var(--num));
    --v1: max(var(--temp) - 0.5, 0);
    --v2: max((var(--temp) - var(--v1)) * 100 - 0.5, 0);
    counter-reset: v1 var(--v1) v2 var(--v2);
}

#number-floating::after {
    content: counter(v1) "." counter(v2, decimal-leading-zero);
}
</style>