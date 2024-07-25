<script setup>
import { ref, watch } from "vue";
import { faTimes } from '@fortawesome/free-solid-svg-icons'

const props = defineProps({
    showModal: Boolean,
});

const dialog = ref(null)

const emit = defineEmits(["modal-close"]);

function closeModal() {
    emit('modal-close')
}
</script>

<template>
    <Teleport to="body">
        <div>
      <Transition>
        <div
          v-if="props.showModal"
          class="fixed w-4/6 top-20 left-2/4 -translate-x-1/2 rounded-lg border border-slate-800 shadow-lg z-50"
        >
          <Teleport to="body">
            <div
              @click.stop="closeModal()"
              class="bg-white/30 backdrop-blur-sm fixed top-0 bottom-0 left-0 right-0 z-40 cursor-pointer"
            ></div>
          </Teleport>
          <div class="flex px-4 py-3 bg-slate-700 rounded-t-lg border-b border-slate-800">
            <h2 class="text-white font-semibold text-lg">
              <slot name="header"></slot>
            </h2>
            <span class="ml-auto text-xl">
                <button @click.stop="closeModal()"
                    class="hover:text-slate-200 hover:dark:text-slate-50 hover:bg-slate-200/20 rounded-full p-1"
                >
                    <FontAwesomeIcon :icon="faTimes" class="fa-fw"></FontAwesomeIcon>
                </button>
            </span>
          </div>
          <div class="px-4 py-3 bg-slate-100">
            <slot name="body"></slot>
          </div>
          <div class="px-4 py-3 bg-slate-100 rounded-b-lg">
            <slot name="footer">
                <div class="flex flex-row-reverse">
                  <button class="btn btn-primary btn-lg" @click.stop="closeModal()">Ok</button>
                </div>
            </slot>
          </div>
        </div>
      </Transition>
    </div>
    </Teleport>
</template>

<style scoped>
.v-enter-active {
  @apply transition duration-150 ease-out;
}
.v-leave-active {
  @apply transition duration-150 ease-in;
}
.v-enter-from,
.v-leave-to {
  @apply scale-90;
  @apply opacity-0;
}
</style>