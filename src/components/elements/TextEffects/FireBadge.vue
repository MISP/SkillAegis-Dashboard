<script setup>
const props = defineProps({
    'is_blue': {
        type: Boolean,
        required: false,
        default: false,
    },
})
</script>

<template>
    <span class="inline-flex flex-row flex-nowrap">
        <img v-if="props.is_blue" src="@/assets/fire_blue.gif" alt="Fire badge blue" class="inline-block"
            style="height: 1rem; position:relative; top: -1px;" />
        <img v-else src="@/assets/fire.gif" alt="Fire badge" class="inline-block"
            style="height: 1rem; position:relative; top: -1px;" />
        <slot />
    </span>
</template>
