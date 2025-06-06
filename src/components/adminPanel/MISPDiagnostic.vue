<script setup>
import {
    faHammer,
    faCheck,
} from '@fortawesome/free-solid-svg-icons'
import { ref, computed, onMounted } from 'vue'
import {
    diagnostic,
    debouncedGetDiagnostic,
    remediateSetting,
} from '@/socket'

const clickedButtons = ref([])

const diagnosticLoading = computed(() => Object.keys(diagnostic.value).length == 0)
const isMISPOnline = computed(() => diagnostic.value.version?.version !== undefined)
const isZMQActive = computed(() => diagnostic.value.zmq_message_count > 0)
const ZMQMessageCount = computed(() => diagnostic.value.zmq_message_count)
const isSuricataInstalled = computed(() => diagnostic.value.suricata?.version !== null)
const suricataVersion = computed(() => isSuricataInstalled.value ? diagnostic.value.suricata?.version : 'Not Installed')

onMounted(() => {
    debouncedGetDiagnostic()
    clickedButtons.value = []
})

function settingHandler(setting) {
    remediateSetting(setting)
}
</script>

<template>
    <div>
        <h4 class="font-semibold">
            <div v-if="!diagnosticLoading">
                <table
                    class="mb-2 table-auto bg-white dark:bg-slate-700 dark:text-slate-100 text-slate-700 rounded-lg shadow-xl inline-block">
                    <tr>
                        <td class="px-3 py-1"><strong>MISP URL</strong></td>
                        <td class="px-3 py-1"><a class="text-sm font-mono tracking-tight text-sky-500 hover:underline"
                                target="_blank" :href="diagnostic['MISP']['url']">{{ diagnostic['MISP']['url'] }}</a>
                        </td>
                    </tr>
                    <tr>
                        <td class="px-3 py-1"><strong>API Key</strong></td>
                        <td class="px-3 py-1"><span class="text-sm font-mono tracking-tight">{{ diagnostic['MISP']['apikey']
                                }}</span></td>
                    </tr>
                </table>
            </div>

            <strong>MISP Status:</strong>
            <span class="ml-2">
                <span :class="{
                    'rounded-lg py-1 px-2 inline-flex': true,
                    'dark:bg-neutral-800 bg-neutral-400 text-slate-800 dark:text-slate-200':
                        diagnosticLoading,
                    'dark:bg-green-700 bg-green-500 text-slate-800 dark:text-slate-200':
                        !diagnosticLoading && isMISPOnline,
                    'dark:bg-red-700 bg-red-700 text-slate-200 dark:text-slate-200':
                        !diagnosticLoading && !isMISPOnline
                }">
                    <Loading v-if="diagnosticLoading" class="inline-block text-xl"></Loading>
                    <span v-else class="font-bold">
                        {{ !isMISPOnline ? 'Unreachable' : `Online (${diagnostic['version']['version']})` }}
                    </span>
                </span>
            </span>
        </h4>
        <h4 class="font-semibold my-3">
            <strong>ZMQ Status:</strong>
            <span class="ml-2">
                <span :class="{
                    'rounded-lg py-1 px-2 inline-flex': true,
                    'dark:bg-neutral-800 bg-neutral-400 text-slate-800 dark:text-slate-200':
                        diagnosticLoading,
                    'dark:bg-green-700 bg-green-500 text-slate-800 dark:text-slate-200':
                        !diagnosticLoading && isZMQActive,
                    'dark:bg-red-700 bg-red-700 text-slate-200 dark:text-slate-200':
                        !diagnosticLoading && !isZMQActive
                }">
                    <Loading v-if="diagnosticLoading" class="inline-block text-xl"></Loading>
                    <span v-else class="font-bold">
                        {{
                        !isZMQActive
                        ? 'No message received yet'
                        : `ZMQ Active (${ZMQMessageCount} messages)`
                        }}
                    </span>
                </span>
            </span>
        </h4>

        <template v-if="diagnosticLoading || isMISPOnline">
            <h4 class="font-semibold ml-1"><strong>MISP Settings:</strong></h4>
            <div class="ml-3">
                <div v-if="diagnosticLoading" class="flex justify-center">
                    <Loading class="text-3xl"></Loading>
                </div>
                <table v-else
                    class="bg-white dark:bg-slate-700 dark:text-slate-100 text-slate-700 rounded-lg shadow-xl w-full mt-2">
                    <thead>
                        <tr>
                            <th class="border-b border-slate-200 dark:border-slate-600 p-2 text-left">
                                Setting
                            </th>
                            <th class="border-b border-slate-200 dark:border-slate-600 p-2 text-left">
                                Value
                            </th>
                            <th class="border-b border-slate-200 dark:border-slate-600 p-2 text-left">
                                Expected Value
                            </th>
                            <th class="border-b border-slate-200 dark:border-slate-600 p-2 text-center">
                                Action
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(settingValues, setting) in diagnostic['settings']" :key="setting">
                            <td class="font-mono font-semibold text-base px-2">{{ setting }}</td>
                            <td :class="`font-mono text-base tracking-tight px-2 ${settingValues.expected_value != settingValues.value
                                ? 'text-red-600 dark:text-red-600'
                                : ''
                                }`">
                                <i v-if="settingValues.value === undefined || settingValues.value === null"
                                    class="text-nowrap">- none -</i>
                                {{ settingValues.value }}
                            </td>
                            <td class="font-mono text-base tracking-tight px-2">
                                {{ settingValues.expected_value }}
                            </td>
                            <td class="px-2 text-center">
                                <span v-if="settingValues.error === true" class="text-red-600 dark:text-red-600">Error:
                                    {{ settingValues.errorMessage }}</span>
                                <button v-else-if="settingValues.expected_value != settingValues.value"
                                    @click="clickedButtons.push(setting) && settingHandler(setting)"
                                    :disabled="clickedButtons.includes(setting)"
                                    class="h-8 min-h-8 px-2 font-semibold bg-green-600 text-slate-200 hover:bg-green-700 btn gap-1">
                                    <template v-if="!clickedButtons.includes(setting)">
                                        <FontAwesomeIcon :icon="faHammer" size="sm" fixed-width></FontAwesomeIcon>
                                        Remediate
                                    </template>
                                    <template v-else>
                                        <Loading class="text-xl"></Loading>
                                    </template>
                                </button>
                                <span v-else class="text-base font-bold text-green-600 dark:text-green-600">
                                    <FontAwesomeIcon :icon="faCheck" class=""></FontAwesomeIcon>
                                    OK
                                </span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </template>

        <h4 class="font-semibold ml-1 my-3">
            <div v-if="!diagnosticLoading">
                <strong>Suricata Status:</strong>
                <span class="ml-2">
                    <span :class="{
                        'rounded-lg py-1 px-2 inline-flex': true,
                        'dark:bg-neutral-800 bg-neutral-400 text-slate-800 dark:text-slate-200':
                            diagnosticLoading,
                        'dark:bg-green-700 bg-green-500 text-slate-800 dark:text-slate-200':
                            !diagnosticLoading && isSuricataInstalled,
                        'dark:bg-red-700 bg-red-700 text-slate-200 dark:text-slate-200':
                            !diagnosticLoading && !isSuricataInstalled
                    }">
                        <Loading v-if="diagnosticLoading" class="inline-block text-xl"></Loading>
                        <span v-else class="font-bold">
                            {{ !isSuricataInstalled ? suricataVersion : `Installed (${suricataVersion})` }}
                        </span>
                    </span>
                </span>
            </div>
        </h4>
    </div>
</template>