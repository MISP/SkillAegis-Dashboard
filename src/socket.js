import { reactive } from "vue";
import { io } from "socket.io-client";

const initial_state = {
  notificationEvents: [],
  notificationCounter: 0,
  notificationAPICounter: 0,
  progresses: {},
}

export const state = reactive({ ...initial_state });
export const connectionState = reactive({ 
  connected: false
 })

export function resetState() {
  Object.assign(state, initial_state);
}

const MAX_LIVE_LOG = 30

// "undefined" means the URL will be computed from the `window.location` object
const URL = process.env.NODE_ENV === "production" ? undefined : "http://localhost:3000";

export const socket = io(URL, {
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