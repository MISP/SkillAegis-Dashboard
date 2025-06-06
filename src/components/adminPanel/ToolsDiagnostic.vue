<script setup>
import { faSuitcaseMedical } from '@fortawesome/free-solid-svg-icons';
import MISPDiagnostic from './MISPDiagnostic.vue';
import { ref } from 'vue';

const activeTab = ref('MISP')
</script>

<template>
    <div>
        <div class="dark:text-slate-700 text-slate-700">
            <div class="flex flex-col w-full border border-slate-700 rounded-md">
                <div class="inline-flex flex-row bg-slate-300 border-b border-slate-700 p-3 gap-2 rounded-t-md">
                    <button @click="activeTab = 'MISP'" class="text-start btn btn-lg !px-5 !py-3"
                    :class="activeTab === 'MISP' ? 'btn-primary' : '!text-slate-800 !border-0`'">
                    <span>MISP</span>
                </button>
            </div>
            <div class="p-4">
                <div v-if="activeTab === 'MISP'">
                    <MISPDiagnostic></MISPDiagnostic>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
