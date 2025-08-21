<script setup>
    import { computed, h } from 'vue'
    import TextWithSparkles from '@/components/elements/TextEffects/TextWithSparkles.vue';
    import TextWithPulse from '@/components/elements/TextEffects/TextWithPulse.vue';
    import FireBadge from '@/components/elements/TextEffects/FireBadge.vue';
    import OnFireProgressbar from '@/components/elements/TextEffects/OnFireProgressbar.vue';

    import { userStats, shouldHideGamification } from '@/socket.js';


    const props = defineProps({
        'status': {
            type: Object,
            required: true,
        },
        'user_id': {
            type: Number,
            required: true,
        }
    })

    const hallOfFame = computed(() => userStats.value?.hall_of_fame || []);
    const timeOnFire = computed(() => userStats.value?.time_on_fire || []);
    const speedRunner = computed(() => userStats.value?.speed_runner || []);

    const hallOfFameIndex = computed(() => hallOfFame.value.findIndex(item => item.user_id === props.user_id))
    const timeOnFireIndex = computed(() => timeOnFire.value.findIndex(item => item.user_id === props.user_id))
    const speedRunnerIndex = computed(() => speedRunner.value.findIndex(item => item.user_id === props.user_id))

    const ConditionalWrapper = (props, { slots }) =>
        props.condition ? props.wrapper(slots.default()) : slots.default();

    const isOnFire = computed(() => {
        return props.status?.is_on_fire || false
    })
    const isOnFireLeaderboard = computed(() => {
        return props.status?.is_on_fire_leaderboard || false
    })
    const showOnFireTimeout = computed(() => {
        return (hasOnFireInterval.value && isOnFire.value && !showOnFireLeaderboardEffect.value) || false
    })
    const hasOnFireInterval = computed(() => {
        return props.status?.on_fire_last_interval ? true : false
    })
    const onFireInterval = computed(() => {
        return hasOnFireInterval.value ? props.status?.on_fire_last_interval : null
    })
    const showOnFireLeaderboardEffect = computed(() => {
        return isOnFireLeaderboard.value && timeOnFireIndex.value === 0
    })
    const isOnHallOfFame = computed(() => {
        return props.status?.is_on_all_house_fame || false
    })
    const showHallOfFameEffect = computed(() => {
        return isOnHallOfFame.value && hallOfFameIndex.value === 0
    })
    const isSpeedRunner = computed(() => {
        return props.status?.is_speed_runner || false
    })
    const showSpeedRunnerEffect = computed(() => {
        return isSpeedRunner.value && speedRunnerIndex.value === 0
    })

</script>

<template>
    <span v-if="shouldHideGamification">
        <ConditionalWrapper :condition="showHallOfFameEffect" :wrapper="(c) => h(TextWithSparkles, null, () => c)">
            <slot />
        </ConditionalWrapper>
    </span>
    <span v-else>
        <ConditionalWrapper :condition="isOnFire || showOnFireLeaderboardEffect" :wrapper="(c) => h(FireBadge, { is_blue: showOnFireLeaderboardEffect, on_fire_interval: onFireInterval }, () => c)">
            <ConditionalWrapper :condition="showOnFireTimeout" :wrapper="(c) => h(OnFireProgressbar, { on_fire_interval: onFireInterval }, () => c)">
                <ConditionalWrapper :condition="showSpeedRunnerEffect" :wrapper="(c) => h(TextWithPulse, null, () => c)">
                    <ConditionalWrapper :condition="showHallOfFameEffect" :wrapper="(c) => h(TextWithSparkles, null, () => c)">
                        <slot />
                    </ConditionalWrapper>
                </ConditionalWrapper>
            </ConditionalWrapper>
        </ConditionalWrapper>
    </span>
</template>
