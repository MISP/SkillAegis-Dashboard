<script setup>
    import { computed } from 'vue';


    const props = defineProps({
        'trophies': { type: Object, required: true },
        'user_id': { type: Number, required: true },
    })

    const trophyCount = computed(() => props.trophies.length)
</script>

<template>
    <span class="flex flex-row flex-nowrap gap-[1px] mr-1">
        <span v-for="trophy in props.trophies" :key="`${props.user_id}-${trophy.id}`" :title="trophy.description">
            <img :src="`/src/${trophy.icon_path}`" class="trophy" />
        </span>
    </span>
</template>

<style scoped>
img.trophy {
    width: 24px;
    max-width: unset;
    height: 24px;
    max-height: unset;
}
</style>