import './assets/main.css'
import VueApexCharts from "vue3-apexcharts";

import { createApp } from 'vue'
import App from './App.vue'

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import Modal from "@/components/elements/Modal.vue"
import Loading from "@/components/elements/Loading.vue"

const app = createApp(App)
app.component('FontAwesomeIcon', FontAwesomeIcon)
app.component('Modal', Modal)
app.component('Loading', Loading)
app.use(VueApexCharts)

app.mount('#app')