<script setup>
    import { computed } from 'vue';
import TrophyPicture from '@/components/elements/TextEffects/TrophyPicture.vue';

    const props = defineProps({
        'trophies': { type: Object, required: true },
        'user_id': { type: Number, required: true },
    })

    const trophyCount = computed(() => props.trophies.length)
</script>

<template>
    <span class="flex flex-row flex-nowrap gap-[1px] mr-1">
        <span v-for="trophy in props.trophies" :key="`${props.user_id}-${trophy.id}`" :title="trophy.description">
            <TrophyPicture :trophy="trophy"></TrophyPicture>
        </span>
    </span>
</template>

