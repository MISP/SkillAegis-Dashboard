<script setup>
import { ref, computed } from 'vue'
import {
    faCloud, faCog, faCircle, faUser, faLink, faBullhorn, faUserNinja,
    faAngleRight,
    faMinus,
} from '@fortawesome/free-solid-svg-icons'
import {
    notifications,
} from '@/socket'
import UsernameFormatter from '@/components/elements/UsernameFormatter.vue'
import RelativeTimeFormatter from '@/components/elements/RelativeTimeFormatter.vue'
import JSONPayload from '@/components/logsViews/JSONPayload.vue'

const tracked_user = ref(null)
const tracked_url = ref(null)

const filtered_notifications = computed(() => {
    let filteredNotif = notifications.value
    if (tracked_user.value !== null && tracked_user.value.length > 0) {
        filteredNotif = filteredNotif.filter((notification) => {
            return notification.user.startsWith(tracked_user.value)
        })
    }
    if (tracked_url.value !== null && tracked_url.value.length > 0) {
        filteredNotif = filteredNotif.filter((notification) => {
            return notification.url.includes(tracked_url.value)
        })
    }
    return filteredNotif
})

function getClassFromResponseCode(response_code) {
    if (String(response_code).startsWith('2') || response_code == 302) {
        return 'text-green-500'
    } else if (String(response_code).startsWith('5')) {
        return 'text-red-600'
    } else if (String(response_code).startsWith('4')) {
        return 'text-amber-600'
    } else {
        return 'text-blue-600'
    }
}

function convertToEpoch(serverTime) {
    let [hours, minutes, seconds] = serverTime.split(":").map(Number);
    let now = new Date();
    let serverDate = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate(), hours, minutes, seconds));
    let localDate = new Date(serverDate);
    return localDate.getTime();
}

function isDisplayablePayload(payload) {
    if (typeof payload === 'string') {
        return true
    }
    if (payload === null || payload === undefined || (typeof payload === 'object' && Object.keys(payload).length === 0)) {
        return false
    }
    return true
}
</script>

<template>
    <div class="overflow-auto grow">
        <table class="bg-white/80 dark:bg-slate-900/80 rounded-lg shadow-xl w-full table-fixed">
            <thead>
                <tr class="font-medium dark:text-slate-200 text-slate-600">
                    <th class="border-b border-slate-100 dark:border-slate-700 p-3 pl-2 text-left w-3/12">
                        User
                        <span class="flex items-center">
                            <label class="mr-1 relative flex items-center cursor-pointer">
                                <FontAwesomeIcon :icon="faUser" size="sm"
                                    class="absolute left-2 text-slate-400 dark:text-slate-300">
                                </FontAwesomeIcon>
                                <input type="text" class="
                        shadow border font-mono w-full rounded py-1 pl-7 pr-2 leading-tight
                        bg-slate-50 text-slate-700 border-slate-300
                        dark:bg-slate-500 dark:text-slate-200 dark:border-slate-400
                        focus:outline-none focus:border focus:border-slate-300 focus:dark:border-slate-300
                    " placeholder="Find User" v-model="tracked_user" />
                            </label>
                        </span>
                    </th>
                    <th class="border-b border-slate-100 dark:border-slate-700 p-3 text-left">
                        URL
                        <span class="flex items-center">
                            <label class="mr-1 relative flex items-center cursor-pointer">
                                <FontAwesomeIcon :icon="faLink" size="sm"
                                    class="absolute left-2 text-slate-400 dark:text-slate-300">
                                </FontAwesomeIcon>
                                <input type="text" class="
                        shadow border font-mono w-full rounded py-1 pl-7 pr-2 leading-tight
                        bg-slate-50 text-slate-700 border-slate-300
                        dark:bg-slate-500 dark:text-slate-200 dark:border-slate-400
                        focus:outline-none focus:border focus:border-slate-300 focus:dark:border-slate-300
                    " placeholder="Find URL" v-model="tracked_url" />
                            </label>
                        </span>
                    </th>
                    <th class="border-b border-slate-100 dark:border-slate-700 p-3 text-left">Payload</th>
                </tr>
            </thead>
            <tbody>
                <tr v-if="notifications.length == 0">
                    <td colspan="3"
                        class="text-center border-b border-slate-100 dark:border-slate-700 text-slate-600 dark:text-slate-400 p-3 pl-6">
                        <i>- No logs yet -</i>
                    </td>
                </tr>
                <template v-else>
                    <tr v-for="notification in filtered_notifications" :key="notification.id" class="group">
                        <td class="border-b border-slate-100 dark:border-slate-700 text-slate-600 dark:text-slate-400 p-1 pl-2 w-3/12 overflow-hidden"
                            :title="notification.user_id">
                            <span class="inline-block truncate align-middle">
                                <UsernameFormatter :username="notification.user"></UsernameFormatter>
                            </span>
                        </td>
                        <td class="border-b border-slate-100 dark:border-slate-700 p-1" :colspan="isDisplayablePayload(notification.payload) ? 1 : 2">
                            <div class="flex items-center group-hover:hidden inline-block">
                                <template v-if="notification.notification_origin == 'zmq'">
                                    <span v-if="notification.http_method == 'POST'"
                                        class="p-1 rounded-md font-bold text-xs mr-2 inline-block text-center dark:bg-amber-600 dark:text-neutral-100 bg-amber-600 text-neutral-100">POST</span>
                                    <span v-else-if="notification.http_method == 'PUT'"
                                        class="p-1 rounded-md font-bold text-xs mr-2 inline-block text-center dark:bg-amber-600 dark:text-neutral-100 bg-amber-600 text-neutral-100">PUT</span>
                                    <span v-else-if="notification.http_method == 'DELETE'"
                                        class="p-1 rounded-md font-bold text-xs mr-2 inline-block text-center dark:bg-red-600 dark:text-neutral-100 bg-red-600 text-neutral-100">DEL</span>
                                    <span v-else
                                        class="p-1 rounded-md font-bold text-xs mr-2 inline-block text-center dark:bg-blue-600 dark:text-neutral-100 bg-blue-600 text-neutral-100">{{
                                        notification.http_method }}</span>
                                    <FontAwesomeIcon v-if="notification.is_api_request"
                                        class="text-slate-800 dark:text-slate-100 mr-1 inline-block" :icon="faCog"
                                        :mask="faCloud" transform="shrink-7 left-1"></FontAwesomeIcon>
                                    <pre
                                        class="text-sm inline max-w-96 overflow-hidden text-ellipsis text-sky-600 dark:text-sky-400">{{ notification.url }}</pre>
                                </template>
                                <template v-else-if="notification.notification_origin == 'webhook'">
                                    <FontAwesomeIcon class="text-slate-800 dark:text-slate-100 mr-1 inline-block"
                                        :icon="faBullhorn">
                                    </FontAwesomeIcon>
                                    <pre
                                        class="text-sm inline max-w-96 overflow-hidden text-ellipsis">Webhook for {{ notification.target_tool }}</pre>
                                </template>
                            </div>
                            <span class="group-hover:inline-block hidden">
                                <span class="text-center max-h-6">
                                    <FontAwesomeIcon :icon="faCircle" size="xs" class="ml-2"
                                        :class="getClassFromResponseCode(notification.response_code)">
                                    </FontAwesomeIcon>
                                    <span class="font-mono ml-1">{{ notification.response_code }}</span>
                                    <FontAwesomeIcon :icon="faMinus" class="mx-1" size="xs"></FontAwesomeIcon>
                                    <RelativeTimeFormatter :timestamp="convertToEpoch(notification.time)">
                                    </RelativeTimeFormatter>
                                </span>
                            </span>
                        </td>
                        <td
                            v-if="isDisplayablePayload(notification.payload)"
                            class="border-b border-slate-100 dark:border-slate-700 text-slate-600 dark:text-slate-300 p-1">
                            <div
                                v-if="notification.http_method == 'POST' || notification.http_method == 'PUT' || notification.notification_origin == 'webhook'">
                                <!-- FIXME: Make that part more generic -->
                                <Alert variant="danger" class="mx-2 mt-2"
                                    v-if="notification.payload === 'string' && !notification.payload.includes('trying to cheat')">
                                    <strong>User {{ notification.user }} is trying to cheat <FontAwesomeIcon
                                            :icon="faUserNinja">
                                        </FontAwesomeIcon></strong>
                                    <div class="text-sm"><span class="">User {{ notification.user }} is trying to cheat
                                            or
                                            hasn't reset
                                            their Event before sending it for validation.</span></div>
                                </Alert>
                                <JSONPayload :payload="notification.payload"></JSONPayload>
                            </div>
                        </td>
                    </tr>
                </template>
            </tbody>
        </table>
    </div>
</template>