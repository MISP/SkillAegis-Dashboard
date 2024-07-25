<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { removeToast } from '@/utils.js'
import {
  faCancel,
  faCheck,
  faCircleCheck,
  faCircleExclamation,
  faCircleInfo,
  faClose,
  faTriangleExclamation
} from '@fortawesome/free-solid-svg-icons'

const emit = defineEmits(['close'])

const props = defineProps({
  id: Number,
  title: String,
  message: String,
  variant: {
    type: String,
    validator(value, props) {
      return ['success', 'warning', 'danger', 'info'].includes(value)
    },
    default: 'info'
  },
  confirm: Boolean,
  confirmCb: Function
})

const duration = 7000

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

function close() {
  emit('close')
}

function callConfirmCb() {
  props.confirmCb()
  close()
}

onMounted(() => {
  setTimeout(() => {
    removeToast(props.id)
  }, duration)
})
</script>

<template>
  <div :class="`flex flex-col min-w-72 py-2 px-3 rounded bg-${variantClass}-100`">
    <div :class="`text-${variantClass}-800 flex items-center`">
      <FontAwesomeIcon :icon="icon" class="mr-2"></FontAwesomeIcon>
      <span class="font-semibold">{{ props.title }}</span>
      <button class="ml-auto w-6 btn btn-link !p-0">
        <FontAwesomeIcon
          :icon="faClose"
          class="text-gray-500 hover:text-gray-700"
          fixed-width
          @click="close()"
        ></FontAwesomeIcon>
      </button>
    </div>
    <div
      class="text-slate-600 p-1 font-light"
      v-if="props.message !== undefined && props.message.length > 0"
    >
      {{ props.message }}
    </div>
    <div v-if="props.confirm" class="flex gap-1">
      <button class="btn btn-info" @click="callConfirmCb()">
        <FontAwesomeIcon :icon="faCheck" class="fa-fw"></FontAwesomeIcon> Confirm
      </button>
      <button class="btn" @click="close()">
        <FontAwesomeIcon :icon="faCancel" class="fa-fw"></FontAwesomeIcon> Cancel
      </button>
    </div>
  </div>
</template>
