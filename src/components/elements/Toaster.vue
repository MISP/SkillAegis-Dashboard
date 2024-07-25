<script setup>
import { computed, ref, watch } from 'vue'
import { allToasts, removeToast } from '@/utils.js'
import Toast from '@/components/elements/Toast.vue'

const container = ref()
const toasts = computed(() => allToasts.value)

function remove(toast_id) {
  removeToast(toast_id)
}
</script>

<template>
  <Teleport to="body">
    <div ref="container" class="fixed m-3 top-0 right-0">
      <transition-group name="list" tag="div" class="flex flex-col-reverse gap-2">
        <Toast
          v-for="toast of toasts"
          :key="toast.id"
          :id="toast.id"
          :title="toast.title"
          :message="toast.message"
          :variant="toast.variant"
          :confirm="toast.confirm"
          :confirmCb="toast.confirmCb"
          @close="remove(toast.id)"
        />
      </transition-group>
    </div>
  </Teleport>
</template>

<style>
.list-enter-active,
.list-leave-active {
  transition: all 0.3s ease-out;
}
.list-enter-from {
  opacity: 0;
  transform: translateY(20px);
}
.list-leave-to {
  opacity: 0;
  transform: translateX(10px);
}
</style>
