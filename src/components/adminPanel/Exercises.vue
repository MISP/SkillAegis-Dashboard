<script setup>
import {
    exercises,
    selected_exercises,
    changeExerciseSelection,
} from '@/socket'
import { faGraduationCap } from '@fortawesome/free-solid-svg-icons';

function changeSelectionState(state_enabled, exec_uuid) {
    changeExerciseSelection(exec_uuid, state_enabled)
}
</script>

<template>
    <div>
        <table class="border border-slate-200">
            <thead class="text-slate-800">
                <tr>
                    <th></th>
                    <th>Name</th>
                    <th>Description</th>
                    <th>Level</th>
                    <th>Task Count</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="exercise in exercises" :key="exercise.name">
                    <td>
                        <input
                            @change="changeSelectionState($event.target.checked, exercise.uuid)"
                            type="checkbox"
                            :checked="selected_exercises.includes(exercise.uuid)"
                            :value="exercise.uuid"
                            class="h-5 w-5 text-blue-600 border-slate-300 rounded focus:ring-blue-500 focus:ring-2"
                        />
                    </td>
                    <td
                    @click="changeSelectionState(!selected_exercises.includes(exercise.uuid), exercise.uuid)"
                    class="font-bold text-lg cursor-pointer select-none"
                    >{{ exercise.name }}</td>
                    <td>{{ exercise.description }}</td>
                    <td>{{ exercise.level }}</td>
                    <td>{{ exercise.tasks.length }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<style scoped>
table thead th {
    @apply px-2 py-1 border-b border-slate-200
}
table tbody td {
    @apply px-2 py-1 border-b border-slate-200
}
</style>