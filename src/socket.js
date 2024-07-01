import { reactive, computed } from "vue";
import { io } from "socket.io-client";

// "undefined" means the URL will be computed from the `window.location` object
const URL = process.env.NODE_ENV === "production" ? undefined : "http://localhost:3000";
const MAX_LIVE_LOG = 30

const initial_state = {
  notificationEvents: [],
  notificationCounter: 0,
  notificationAPICounter: 0,
  exercises: [],
  progresses: {},
}

const state = reactive({ ...initial_state });
const connectionState = reactive({ 
  connected: false
 })

export const exercises = computed(() => state.exercises)
export const progresses = computed(() => state.progresses)
export const notifications = computed(() => state.notificationEvents)
export const notificationCounter = computed(() => state.notificationCounter)
export const notificationAPICounter = computed(() => state.notificationAPICounter)
export const userCount = computed(() => Object.keys(state.progresses).length)
export const socketConnected = computed(() => connectionState.connected)

export function resetState() {
  Object.assign(state, initial_state);
}

export function fullReload() {
  socket.emit("get_exercises", (all_exercises) => {
    state.exercises = all_exercises
  })
  socket.emit("get_notifications", (all_notifications) => {
    state.notificationEvents = all_notifications
  })
  socket.emit("get_progress", (all_progress) => {
    state.progresses = all_progress
  })
}


const socket = io(URL, {
  autoConnect: true
});

socket.on("connect", () => {
  connectionState.connected = true;
});

socket.on("disconnect", () => {
  connectionState.connected = false;
});

socket.on("notification", (message) => {
  state.notificationCounter += 1
  if (message.is_api_request) {
    state.notificationAPICounter += 1
  }
  addLimited(state.notificationEvents, message, MAX_LIVE_LOG)
});

socket.on("new_user", (new_user) => {
  socket.emit("get_progress", (all_progress) => {
    state.progresses = all_progress
  })
});

socket.on("refresh_score", (new_user) => {
  socket.emit("get_progress", (all_progress) => {
    state.progresses = all_progress
  })
});

function addLimited(target, message, maxCount) {
  target.unshift(message)
  if (target.length > maxCount) {
    target.length = maxCount
  }
}