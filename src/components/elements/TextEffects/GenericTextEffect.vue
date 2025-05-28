<script setup>
    import { computed, h } from 'vue'
    import TextWithSparkles from '@/components/elements/TextEffects/TextWithSparkles.vue';
    import TextWithPulse from '@/components/elements/TextEffects/TextWithPulse.vue';
    import FireBadge from '@/components/elements/TextEffects/FireBadge.vue';

    const props = defineProps({
        'status': {
            type: Object,
            required: true,
        },
    })

    const ConditionalWrapper = (props, { slots }) =>
        props.condition ? props.wrapper(slots.default()) : slots.default();

    const isOnFire = computed(() => {
        return props.status?.is_on_fire || false
    })
    const isOnFireLeaderboard = computed(() => {
        return props.status?.is_on_fire_leaderboard || false
    })
    const isOnHallOfFame = computed(() => {
        return props.status?.is_on_all_house_fame || false
    })
    const isSpeedRunner = computed(() => {
        return props.status?.is_speed_runner || false
    })

</script>

<template>
    <ConditionalWrapper :condition="isOnFire || isOnFireLeaderboard" :wrapper="(c) => h(FireBadge, { is_blue: isOnFire && !isOnFireLeaderboard }, () => c)">
        <ConditionalWrapper :condition="isSpeedRunner" :wrapper="(c) => h(TextWithPulse, null, () => c)">
            <ConditionalWrapper :condition="isOnHallOfFame" :wrapper="(c) => h(TextWithSparkles, null, () => c)">
                <slot />
            </ConditionalWrapper>
        </ConditionalWrapper>
    </ConditionalWrapper>
</template>
