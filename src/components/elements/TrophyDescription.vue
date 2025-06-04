<script setup>
import { faCircleQuestion } from '@fortawesome/free-solid-svg-icons';

const props = defineProps({
    "trophy": {type: Object, required: true},
})
</script>

<template>
    <div class="flex flex-row flex-nowrap items-center">
        <span class="py-1">
            <img :src="`/src/${props.trophy.icon_path}`" class="trophy" :class="{ 'grayscale': props.trophy.users.length == 0 }" />
        </span>
        <span class="font-retrogaming pl-2">
            {{ props.trophy.name }}
            <sup class="text-2xs -top-2" :title="props.trophy.description">
                <FontAwesomeIcon :icon="faCircleQuestion" fixed-width style="--fa-fw-width: 1em"></FontAwesomeIcon>
            </sup>
        </span>
    </div>
</template>

<style scoped>
img.trophy {
    width: 32px;
    max-width: unset;
    height: 32px;
    max-height: unset;
}
</style>