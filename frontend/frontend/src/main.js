import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import PrimeVue from 'primevue/config';
import 'primevue/resources/themes/aura-light-green/theme.css'



axios.defaults.baseURL = "http://127.0.0.1:8000"

const app = createApp(App)

app.use(router)
app.use(PrimeVue);
app.use(store)
app.mount('#app')
