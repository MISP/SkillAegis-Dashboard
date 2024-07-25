<script setup>
import {
  faCircleCheck,
  faCircleExclamation,
  faCircleInfo,
  faTriangleExclamation
} from '@fortawesome/free-solid-svg-icons'
import { computed } from 'vue'

const props = defineProps({
  title: String,
  message: [Array, String],
  variant: {
    type: String,
    validator(value, props) {
      return ['success', 'warning', 'danger', 'info'].includes(value)
    },
    default: 'info'
  }
})

const icon = computed(() => {
  if (props.variant == 'success') {
    return faCircleCheck
  } else if (props.variant == 'warning') {
    return faCircleExclamation
  } else if (props.variant == 'danger') {
    return faTriangleExclamation
  }
  return faCircleInfo
})

const variantClass = computed(() => {
  if (props.variant == 'success') {
    return 'green'
  } else if (props.variant == 'warning') {
    return 'amber'
  } else if (props.variant == 'danger') {
    return 'red'
  }
  return 'blue'
})

const messages = computed(() => {
  return Array.isArray(props.message)
    ? props.message
    : props.message !== undefined
    ? [props.message]
    : []
})
</script>

<template>
  <div
    :class="`mb-2 p-2 border-l-4 text-left rounded dark:bg-${variantClass}-300 dark:text-slate-900 dark:border-${variantClass}-700 bg-${variantClass}-200 text-slate-900 border-${variantClass}-700`"
  >
    <FontAwesomeIcon
      :icon="icon"
      :class="`text-${variantClass}-700 text-lg mx-3`"
    ></FontAwesomeIcon>
    <strong class="mr-2">{{ props.title }}</strong>
    <p
      class="text-slate-700 p-1 font-light whitespace-pre"
      v-for="(message, i) in messages"
      :key="i"
    >
      {{ message }}
    </p>
  </div>
</template>