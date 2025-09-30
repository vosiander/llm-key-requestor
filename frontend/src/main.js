import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify.js'
import './assets/main.css'

const app = createApp(App)

// Use Vuetify plugin
app.use(vuetify)

// Mount the app
app.mount('#app')
